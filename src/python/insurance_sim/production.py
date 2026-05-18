"""Production-run helpers for shardable insurance-hypothesis simulations."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from concurrent.futures import ProcessPoolExecutor, as_completed
import json
import os
from pathlib import Path
import platform
import subprocess
import tempfile
import time
from typing import Any, Iterable, Sequence

import numpy as np
import pandas as pd

from .model import (
    SimulationConfig,
    effective_rho,
    generate_environment,
    simulate_ricker,
    slopes_for_mode,
    summarise_timeseries,
)


MANIFEST_VERSION = 1

REQUIRED_RESULT_COLUMNS = {
    "run_id",
    "scenario_id",
    "scenario_index",
    "shard_id",
    "replicate",
    "replicate_seed",
    "n_steps",
    "burn_in",
    "mean_total",
    "var_total",
    "cv_total",
    "mean_species_mean",
    "mean_species_var",
    "mean_extinction_freq",
    "phi_ldm",
    "mean_pairwise_corr",
    "rho_eff",
    "rho_clipped",
    "sigma_env",
    "rho_env",
    "n_species",
    "phi",
    "slope_mode",
    "alpha_inter",
}

FINITE_RESULT_COLUMNS = {
    "mean_total",
    "var_total",
    "cv_total",
    "mean_species_mean",
    "mean_species_var",
    "mean_extinction_freq",
}


@dataclass(frozen=True)
class ProductionScenario:
    """One parameter scenario in a production manifest."""

    scenario_id: str
    scenario_index: int
    sigma_env: float
    rho_env: float
    n_species: int
    slope_mode: str
    phi: float
    steps: int
    burn: int
    alpha_inter: float

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProductionScenario:
        return cls(
            scenario_id=str(data["scenario_id"]),
            scenario_index=int(data["scenario_index"]),
            sigma_env=float(data["sigma_env"]),
            rho_env=float(data["rho_env"]),
            n_species=int(data["n_species"]),
            slope_mode=str(data["slope_mode"]),
            phi=float(data["phi"]),
            steps=int(data["steps"]),
            burn=int(data["burn"]),
            alpha_inter=float(data["alpha_inter"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "scenario_id": self.scenario_id,
            "scenario_index": self.scenario_index,
            "sigma_env": self.sigma_env,
            "rho_env": self.rho_env,
            "n_species": self.n_species,
            "slope_mode": self.slope_mode,
            "phi": self.phi,
            "steps": self.steps,
            "burn": self.burn,
            "alpha_inter": self.alpha_inter,
        }

    def config(self) -> SimulationConfig:
        return SimulationConfig(
            n_species=self.n_species,
            n_steps=self.steps,
            burn_in=self.burn,
            sigma_env=self.sigma_env,
            rho_env=self.rho_env,
            phi=self.phi,
            r0=1.0,
            K=100.0,
            b_slopes=slopes_for_mode(self.slope_mode, self.n_species),
            alpha_intra=1.0,
            alpha_inter=self.alpha_inter,
        )


@dataclass(frozen=True)
class ProductionShard:
    """One replicate interval for one scenario."""

    shard_id: str
    scenario_id: str
    replicate_start: int
    replicate_end: int
    path: str
    done_path: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> ProductionShard:
        return cls(
            shard_id=str(data["shard_id"]),
            scenario_id=str(data["scenario_id"]),
            replicate_start=int(data["replicate_start"]),
            replicate_end=int(data["replicate_end"]),
            path=str(data["path"]),
            done_path=str(data["done_path"]),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "shard_id": self.shard_id,
            "scenario_id": self.scenario_id,
            "replicate_start": self.replicate_start,
            "replicate_end": self.replicate_end,
            "expected_reps": self.expected_reps,
            "path": self.path,
            "done_path": self.done_path,
        }

    @property
    def expected_reps(self) -> int:
        return self.replicate_end - self.replicate_start


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def parse_float_list(raw: str) -> list[float]:
    values = [float(item.strip()) for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("Expected at least one float value.")
    return values


def parse_int_list(raw: str) -> list[int]:
    values = [int(item.strip()) for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("Expected at least one integer value.")
    return values


def parse_str_list(raw: str) -> list[str]:
    values = [item.strip() for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError("Expected at least one string value.")
    return values


def build_scenarios(
    *,
    sigma_vals: Sequence[float],
    rho_vals: Sequence[float],
    species_vals: Sequence[int],
    slope_modes: Sequence[str],
    phi: float,
    phi_vals: Sequence[float] | None = None,
    steps: int,
    burn: int,
    alpha_inter: float,
) -> list[ProductionScenario]:
    phis = [float(phi)] if phi_vals is None else [float(value) for value in phi_vals]
    if not phis:
        raise ValueError("Expected at least one phi value.")

    scenarios: list[ProductionScenario] = []
    for slope_mode in slope_modes:
        for n_species in species_vals:
            # Validate the slope mode/species combination early.
            slopes_for_mode(slope_mode, int(n_species))
            for phi_value in phis:
                for sigma_env in sigma_vals:
                    for rho_env in rho_vals:
                        scenario_index = len(scenarios)
                        scenarios.append(
                            ProductionScenario(
                                scenario_id=f"sc{scenario_index:05d}",
                                scenario_index=scenario_index,
                                sigma_env=float(sigma_env),
                                rho_env=float(rho_env),
                                n_species=int(n_species),
                                slope_mode=str(slope_mode),
                                phi=float(phi_value),
                                steps=int(steps),
                                burn=int(burn),
                                alpha_inter=float(alpha_inter),
                            )
                        )
    return scenarios


def build_shards(
    scenarios: Sequence[ProductionScenario],
    *,
    reps_per_scenario: int,
    replicates_per_shard: int,
) -> list[ProductionShard]:
    if reps_per_scenario <= 0:
        raise ValueError("reps_per_scenario must be positive.")
    if replicates_per_shard <= 0:
        raise ValueError("replicates_per_shard must be positive.")

    shards: list[ProductionShard] = []
    for scenario in scenarios:
        for start in range(0, reps_per_scenario, replicates_per_shard):
            end = min(start + replicates_per_shard, reps_per_scenario)
            shard_index = len(shards)
            shard_id = f"shard{shard_index:06d}"
            path = f"shards/{shard_id}.parquet"
            done_path = f"shards/{shard_id}.done.json"
            shards.append(
                ProductionShard(
                    shard_id=shard_id,
                    scenario_id=scenario.scenario_id,
                    replicate_start=start,
                    replicate_end=end,
                    path=path,
                    done_path=done_path,
                )
            )
    return shards


def create_manifest(
    *,
    run_id: str,
    reps_per_scenario: int,
    replicates_per_shard: int,
    sigma_vals: Sequence[float],
    rho_vals: Sequence[float],
    species_vals: Sequence[int],
    slope_modes: Sequence[str],
    phi: float,
    phi_vals: Sequence[float] | None = None,
    steps: int,
    burn: int,
    alpha_inter: float,
    base_seed: int,
) -> dict[str, Any]:
    if not run_id.strip():
        raise ValueError("run_id must be non-empty.")
    if steps <= 0:
        raise ValueError("steps must be positive.")
    if burn < 0 or burn >= steps:
        raise ValueError("burn must satisfy 0 <= burn < steps.")

    scenarios = build_scenarios(
        sigma_vals=sigma_vals,
        rho_vals=rho_vals,
        species_vals=species_vals,
        slope_modes=slope_modes,
        phi=phi,
        phi_vals=phi_vals,
        steps=steps,
        burn=burn,
        alpha_inter=alpha_inter,
    )
    shards = build_shards(
        scenarios,
        reps_per_scenario=reps_per_scenario,
        replicates_per_shard=replicates_per_shard,
    )
    return {
        "manifest_version": MANIFEST_VERSION,
        "run_id": run_id,
        "created_at_utc": utc_now_iso(),
        "base_seed": int(base_seed),
        "reps_per_scenario": int(reps_per_scenario),
        "replicates_per_shard": int(replicates_per_shard),
        "scenario_count": len(scenarios),
        "shard_count": len(shards),
        "expected_rows": len(scenarios) * int(reps_per_scenario),
        "scenario_order": (
            ["slope_mode", "n_species", "phi", "sigma_env", "rho_env"]
            if phi_vals is not None
            else ["slope_mode", "n_species", "sigma_env", "rho_env"]
        ),
        "scenarios": [scenario.to_dict() for scenario in scenarios],
        "shards": [shard.to_dict() for shard in shards],
    }


def create_manifest_from_spec(
    spec: dict[str, Any],
    *,
    run_id_override: str | None = None,
) -> dict[str, Any]:
    """Create a production manifest from a versioned JSON-style spec."""
    if int(spec.get("spec_version", -1)) != 1:
        raise ValueError(f"Unsupported spec_version: {spec.get('spec_version')}")
    manifest_spec = spec["manifest"]
    phi_values = manifest_spec.get("phi_vals")
    phi = float(manifest_spec["phi"] if "phi" in manifest_spec else phi_values[0])
    manifest = create_manifest(
        run_id=str(run_id_override or spec["run_id"]),
        reps_per_scenario=int(manifest_spec["reps_per_scenario"]),
        replicates_per_shard=int(manifest_spec["replicates_per_shard"]),
        sigma_vals=[float(value) for value in manifest_spec["sigma_vals"]],
        rho_vals=[float(value) for value in manifest_spec["rho_vals"]],
        species_vals=[int(value) for value in manifest_spec["species_vals"]],
        slope_modes=[str(value) for value in manifest_spec["slope_modes"]],
        phi=phi,
        phi_vals=None if phi_values is None else [float(value) for value in phi_values],
        steps=int(manifest_spec["steps"]),
        burn=int(manifest_spec["burn"]),
        alpha_inter=float(manifest_spec["alpha_inter"]),
        base_seed=int(manifest_spec["base_seed"]),
    )
    expected = spec.get("expected")
    if expected is not None:
        for key in ("scenario_count", "shard_count", "expected_rows"):
            if int(expected[key]) != int(manifest[key]):
                raise ValueError(
                    f"Spec expected {key}={expected[key]}, but manifest has {manifest[key]}."
                )
    return manifest


def write_manifest(manifest: dict[str, Any], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def load_manifest(path: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if int(manifest.get("manifest_version", -1)) != MANIFEST_VERSION:
        raise ValueError(f"Unsupported manifest_version: {manifest.get('manifest_version')}")
    return manifest


def scenario_map(manifest: dict[str, Any]) -> dict[str, ProductionScenario]:
    return {
        scenario.scenario_id: scenario
        for scenario in (ProductionScenario.from_dict(item) for item in manifest["scenarios"])
    }


def shard_map(manifest: dict[str, Any]) -> dict[str, ProductionShard]:
    return {
        shard.shard_id: shard
        for shard in (ProductionShard.from_dict(item) for item in manifest["shards"])
    }


def seed_for_replicate(base_seed: int, scenario_index: int, replicate: int) -> int:
    """Return a deterministic 32-bit seed for one production replicate."""
    seed_seq = np.random.SeedSequence([int(base_seed), int(scenario_index), int(replicate)])
    return int(seed_seq.generate_state(1, dtype=np.uint32)[0])


def _replicate_record(
    *,
    scenario: ProductionScenario,
    replicate: int,
    replicate_seed: int,
    run_id: str,
    shard_id: str,
) -> dict[str, Any]:
    config = scenario.config()
    env = generate_environment(
        n_steps=config.n_steps,
        n_species=config.n_species,
        phi=config.phi,
        sigma_env=config.sigma_env,
        rho=config.rho_env,
        rng=np.random.default_rng(replicate_seed),
    )
    traj = simulate_ricker(
        env,
        r0=config.r0,
        K=config.K,
        b_slopes=config.b_slopes,
        alpha_intra=config.alpha_intra,
        alpha_inter=config.alpha_inter,
        floor=config.floor,
        max_exp=config.max_exp,
        initial=None,
    )
    stats = summarise_timeseries(traj, burn_in=config.burn_in, floor=config.floor)
    rho_eff = effective_rho(config.rho_env, config.n_species)
    rho_clipped = bool(abs(rho_eff - float(config.rho_env)) > 1e-12)
    return {
        "run_id": run_id,
        "scenario_id": scenario.scenario_id,
        "scenario_index": scenario.scenario_index,
        "shard_id": shard_id,
        "replicate": int(replicate),
        "replicate_seed": int(replicate_seed),
        "n_steps": int(config.n_steps),
        "burn_in": int(config.burn_in),
        "mean_total": stats["mean_total"],
        "var_total": stats["var_total"],
        "cv_total": stats["cv_total"],
        "mean_species_mean": float(np.mean(stats["mean_species"])),
        "mean_species_var": float(np.mean(stats["var_species"])),
        "mean_extinction_freq": float(np.mean(stats["extinction_freq"])),
        "phi_ldm": stats["phi_ldm"],
        "mean_pairwise_corr": stats["mean_pairwise_corr"],
        "rho_eff": rho_eff,
        "rho_clipped": rho_clipped,
        "sigma_env": scenario.sigma_env,
        "rho_env": scenario.rho_env,
        "n_species": scenario.n_species,
        "phi": scenario.phi,
        "slope_mode": scenario.slope_mode,
        "alpha_inter": scenario.alpha_inter,
    }


def run_shard(
    manifest_path: Path,
    shard_id: str,
    *,
    force: bool = False,
) -> Path:
    manifest = load_manifest(manifest_path)
    scenarios = scenario_map(manifest)
    shards = shard_map(manifest)
    if shard_id not in shards:
        raise ValueError(f"Unknown shard_id: {shard_id}")

    shard = shards[shard_id]
    scenario = scenarios[shard.scenario_id]
    out_path = (manifest_path.parent / shard.path).resolve()
    done_path = (manifest_path.parent / shard.done_path).resolve()
    if out_path.exists() and done_path.exists() and not force:
        return out_path

    out_path.parent.mkdir(parents=True, exist_ok=True)
    started_at = utc_now_iso()
    started_monotonic = time.perf_counter()
    records = []
    base_seed = int(manifest["base_seed"])
    run_id = str(manifest["run_id"])
    for replicate in range(shard.replicate_start, shard.replicate_end):
        replicate_seed = seed_for_replicate(base_seed, scenario.scenario_index, replicate)
        records.append(
            _replicate_record(
                scenario=scenario,
                replicate=replicate,
                replicate_seed=replicate_seed,
                run_id=run_id,
                shard_id=shard.shard_id,
            )
        )

    frame = pd.DataFrame.from_records(records)
    _atomic_write_parquet(frame, out_path)
    finished_at = utc_now_iso()
    done_payload = {
        "run_id": run_id,
        "shard_id": shard.shard_id,
        "scenario_id": scenario.scenario_id,
        "replicate_start": shard.replicate_start,
        "replicate_end": shard.replicate_end,
        "rows": int(len(frame)),
        "started_at_utc": started_at,
        "finished_at_utc": finished_at,
        "duration_seconds": round(time.perf_counter() - started_monotonic, 6),
        "host": platform.node(),
        "pid": os.getpid(),
        "git_commit": current_git_commit(Path.cwd()),
    }
    _atomic_write_text(json.dumps(done_payload, indent=2, sort_keys=True) + "\n", done_path)
    return out_path


def run_pending_shards(
    manifest_path: Path,
    *,
    max_shards: int | None = None,
    force: bool = False,
    jobs: int = 1,
) -> list[Path]:
    manifest = load_manifest(manifest_path)
    shard_ids: list[str] = []
    for shard_data in manifest["shards"]:
        shard = ProductionShard.from_dict(shard_data)
        out_path = manifest_path.parent / shard.path
        done_path = manifest_path.parent / shard.done_path
        if out_path.exists() and done_path.exists() and not force:
            continue
        shard_ids.append(shard.shard_id)
        if max_shards is not None and len(shard_ids) >= max_shards:
            break

    if jobs <= 0:
        raise ValueError("jobs must be positive.")
    if jobs == 1 or len(shard_ids) <= 1:
        return [run_shard(manifest_path, shard_id, force=force) for shard_id in shard_ids]

    completed: list[Path] = []
    with ProcessPoolExecutor(max_workers=min(jobs, len(shard_ids))) as executor:
        futures = {
            executor.submit(run_shard, manifest_path, shard_id, force=force): shard_id
            for shard_id in shard_ids
        }
        for future in as_completed(futures):
            completed.append(future.result())
    return completed


def shard_output_paths(manifest_path: Path, manifest: dict[str, Any]) -> list[Path]:
    return [manifest_path.parent / ProductionShard.from_dict(item).path for item in manifest["shards"]]


def combine_shards(
    manifest_path: Path,
    output_path: Path,
    *,
    validation_path: Path | None = None,
) -> pd.DataFrame:
    manifest = load_manifest(manifest_path)
    paths = shard_output_paths(manifest_path, manifest)
    missing = [str(path) for path in paths if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing shard outputs:\n" + "\n".join(missing[:20]))

    frames = [pd.read_parquet(path) for path in paths]
    combined = pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()
    combined = combined.sort_values(["scenario_index", "replicate", "shard_id"]).reset_index(drop=True)
    validate_combined_frame(manifest, combined)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    _atomic_write_parquet(combined, output_path)
    if validation_path is not None:
        write_validation_report(manifest, combined, validation_path)
    return combined


def validate_combined_file(manifest_path: Path, combined_path: Path) -> dict[str, Any]:
    manifest = load_manifest(manifest_path)
    frame = pd.read_parquet(combined_path)
    validate_combined_frame(manifest, frame)
    return validation_summary(manifest, frame)


def validate_combined_frame(manifest: dict[str, Any], frame: pd.DataFrame) -> None:
    missing_cols = sorted(REQUIRED_RESULT_COLUMNS - set(frame.columns))
    if missing_cols:
        raise ValueError(f"Combined output is missing required columns: {missing_cols}")

    expected_rows = int(manifest["expected_rows"])
    if len(frame) != expected_rows:
        raise ValueError(f"Expected {expected_rows} rows, found {len(frame)}.")

    duplicate_mask = frame.duplicated(["scenario_id", "replicate"])
    if duplicate_mask.any():
        examples = frame.loc[duplicate_mask, ["scenario_id", "replicate"]].head().to_dict("records")
        raise ValueError(f"Duplicate scenario/replicate rows found: {examples}")

    for col in FINITE_RESULT_COLUMNS:
        values = frame[col].to_numpy(dtype=float)
        if np.any(~np.isfinite(values)):
            raise ValueError(f"Column {col} contains non-finite values.")

    scenarios = scenario_map(manifest)
    reps_per_scenario = int(manifest["reps_per_scenario"])
    expected_reps = set(range(reps_per_scenario))
    for scenario_id, scenario in scenarios.items():
        rows = pd.DataFrame(frame.loc[frame["scenario_id"] == scenario_id].copy())
        if len(rows) != reps_per_scenario:
            raise ValueError(f"{scenario_id} expected {reps_per_scenario} rows, found {len(rows)}.")
        observed_reps = set(int(rep) for rep in np.asarray(rows["replicate"], dtype=int).tolist())
        if observed_reps != expected_reps:
            missing = sorted(expected_reps - observed_reps)
            extra = sorted(observed_reps - expected_reps)
            raise ValueError(f"{scenario_id} replicate mismatch; missing={missing[:10]}, extra={extra[:10]}")

        _expect_single_value(rows, "sigma_env", scenario.sigma_env)
        _expect_single_value(rows, "rho_env", scenario.rho_env)
        _expect_single_value(rows, "n_species", scenario.n_species)
        _expect_single_value(rows, "phi", scenario.phi)
        _expect_single_value(rows, "slope_mode", scenario.slope_mode)
        _expect_single_value(rows, "alpha_inter", scenario.alpha_inter)
        rho_eff = effective_rho(scenario.rho_env, scenario.n_species)
        _expect_single_value(rows, "rho_eff", rho_eff)
        rho_clipped = bool(abs(rho_eff - scenario.rho_env) > 1e-12)
        _expect_single_value(rows, "rho_clipped", rho_clipped)


def validation_summary(manifest: dict[str, Any], frame: pd.DataFrame) -> dict[str, Any]:
    return {
        "run_id": manifest["run_id"],
        "validated_at_utc": utc_now_iso(),
        "scenario_count": int(manifest["scenario_count"]),
        "shard_count": int(manifest["shard_count"]),
        "rows": int(len(frame)),
        "expected_rows": int(manifest["expected_rows"]),
        "reps_per_scenario": int(manifest["reps_per_scenario"]),
        "cv_total_min": float(frame["cv_total"].min()),
        "cv_total_max": float(frame["cv_total"].max()),
        "mean_extinction_freq_max": float(frame["mean_extinction_freq"].max()),
    }


def write_validation_report(manifest: dict[str, Any], frame: pd.DataFrame, path: Path) -> None:
    validate_combined_frame(manifest, frame)
    _atomic_write_text(json.dumps(validation_summary(manifest, frame), indent=2, sort_keys=True) + "\n", path)


def current_git_commit(cwd: Path) -> str | None:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError:
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def _expect_single_value(rows: pd.DataFrame, col: str, expected: object) -> None:
    observed = rows[col].drop_duplicates().to_list()
    if len(observed) != 1:
        raise ValueError(f"{col} has multiple values for a scenario: {observed[:5]}")
    actual = observed[0]
    if isinstance(expected, float):
        if not np.isclose(float(actual), expected, rtol=0.0, atol=1e-10):
            raise ValueError(f"{col} expected {expected}, found {actual}.")
    else:
        if actual != expected:
            raise ValueError(f"{col} expected {expected}, found {actual}.")


def _atomic_write_parquet(frame: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        delete=False,
    ) as handle:
        tmp_path = Path(handle.name)
    try:
        frame.to_parquet(tmp_path, index=False)
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def _atomic_write_text(text: str, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
        delete=False,
    ) as handle:
        tmp_path = Path(handle.name)
        handle.write(text)
    try:
        os.replace(tmp_path, path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def pending_shards(manifest_path: Path) -> list[str]:
    manifest = load_manifest(manifest_path)
    pending = []
    for item in manifest["shards"]:
        shard = ProductionShard.from_dict(item)
        if not (manifest_path.parent / shard.path).exists() or not (manifest_path.parent / shard.done_path).exists():
            pending.append(shard.shard_id)
    return pending


def iter_shard_ids(manifest: dict[str, Any]) -> Iterable[str]:
    for item in manifest["shards"]:
        yield str(item["shard_id"])
