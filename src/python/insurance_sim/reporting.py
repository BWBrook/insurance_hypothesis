"""Shared reporting helpers for analysis scripts.

These utilities keep CLI scripts thin while preserving the current on-disk
contract for cached summaries, report CSVs, and promoted figure artefacts.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class CachedRunSpec:
    """Description of a cached simulation grid used by analysis scripts."""

    args: tuple[str, ...]
    desc: str
    path: Path


DEFAULT_DATA_RUNS: dict[str, CachedRunSpec] = {
    "run1": CachedRunSpec(
        args=("--reps", "150"),
        desc="Mixed slopes main grid",
        path=Path("data/sim/grid/run1/summaries.parquet"),
    ),
    "pos_full": CachedRunSpec(
        args=("--reps", "100", "--slope-mode", "positive", "--species-list", "4,8"),
        desc="Positive slopes grid",
        path=Path("data/sim/grid/pos_full/summaries.parquet"),
    ),
    "pos_matched": CachedRunSpec(
        args=("--reps", "100", "--slope-mode", "positive_matched", "--species-list", "4,8"),
        desc="Magnitude-matched aligned slopes control",
        path=Path("data/sim/grid/pos_matched/summaries.parquet"),
    ),
    "phi0_reduced": CachedRunSpec(
        args=(
            "--reps",
            "80",
            "--phi",
            "0.0",
            "--sigma-list",
            "0,0.5,1.0",
            "--rho-list=-0.5,0,0.5,0.9,1.0",
            "--species-list",
            "2,4",
            "--steps",
            "400",
            "--burn",
            "200",
        ),
        desc="No persistence sensitivity (phi=0.0)",
        path=Path("data/sim/grid/phi0_reduced/summaries.parquet"),
    ),
    "phi07_reduced": CachedRunSpec(
        args=(
            "--reps",
            "80",
            "--phi",
            "0.7",
            "--sigma-list",
            "0,0.5,1.0",
            "--rho-list=-0.5,0,0.5,0.9,1.0",
            "--species-list",
            "2,4",
            "--steps",
            "400",
            "--burn",
            "200",
        ),
        desc="Persistence sensitivity (phi=0.7)",
        path=Path("data/sim/grid/phi07_reduced/summaries.parquet"),
    ),
    "phi09_reduced": CachedRunSpec(
        args=(
            "--reps",
            "80",
            "--phi",
            "0.9",
            "--sigma-list",
            "0,0.5,1.0",
            "--rho-list=-0.5,0,0.5,0.9,1.0",
            "--species-list",
            "2,4",
            "--steps",
            "400",
            "--burn",
            "200",
        ),
        desc="High persistence sensitivity (phi=0.9)",
        path=Path("data/sim/grid/phi09_reduced/summaries.parquet"),
    ),
    "phi095_reduced": CachedRunSpec(
        args=(
            "--reps",
            "80",
            "--phi",
            "0.95",
            "--sigma-list",
            "0,0.5,1.0",
            "--rho-list=-0.5,0,0.5,0.9,1.0",
            "--species-list",
            "2,4",
            "--steps",
            "400",
            "--burn",
            "200",
        ),
        desc="High persistence sensitivity (phi=0.95)",
        path=Path("data/sim/grid/phi095_reduced/summaries.parquet"),
    ),
}


def load_summary(path: Path) -> pd.DataFrame:
    """Load a cached summary and backfill effective-correlation columns."""
    return ensure_effective_rho(pd.read_parquet(path))


def ensure_effective_rho(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure a summary frame has `rho_eff` and `rho_clipped` columns."""
    if "rho_eff" in df.columns:
        if "rho_clipped" not in df.columns and "rho_env" in df.columns:
            out = df.copy()
            out["rho_clipped"] = (out["rho_eff"] - out["rho_env"]).abs() > 1e-12
            return out
        return df

    if "rho_env" not in df.columns or "n_species" not in df.columns:
        raise ValueError("Cannot reconstruct rho_eff without rho_env and n_species columns.")

    out = df.copy()
    eps = 1e-6
    rho_env = out["rho_env"].to_numpy(dtype=float)
    n_species = out["n_species"].to_numpy(dtype=int)
    rho_eff = rho_env.copy()

    mask = n_species >= 2
    if np.any(mask):
        min_rho = (-1.0 / (n_species[mask] - 1)) + eps
        max_rho = 1.0 - eps
        rho_eff[mask] = np.clip(rho_env[mask], min_rho, max_rho)

    out["rho_eff"] = rho_eff
    out["rho_clipped"] = np.abs(rho_eff - rho_env) > 1e-12
    return out


def sort_by_rho_eff(df: pd.DataFrame) -> pd.DataFrame:
    """Return a copy sorted by `rho_eff` with a clean index."""
    order = np.argsort(np.asarray(df["rho_eff"], dtype=float))
    return df.iloc[order].reset_index(drop=True)


def add_species_cv(df: pd.DataFrame) -> pd.DataFrame:
    """Add approximate mean species-level CV (`cv_sp`) when derivable."""
    if "cv_sp" in df.columns:
        return df
    if "mean_species_var" not in df.columns or "mean_species_mean" not in df.columns:
        return df

    out = df.copy()
    mean_species = np.asarray(out["mean_species_mean"], dtype=float)
    var_species = np.asarray(out["mean_species_var"], dtype=float)
    cv_sp = np.full_like(mean_species, np.nan, dtype=float)
    valid = mean_species > 0
    cv_sp[valid] = np.sqrt(np.maximum(var_species[valid], 0.0)) / mean_species[valid]
    out["cv_sp"] = cv_sp
    return out


def summarize_numerical_guard_csv(in_path: Path) -> pd.DataFrame:
    """Aggregate replicate-level guard diagnostics to scenario summaries."""
    df = pd.read_csv(in_path)
    group_cols = ["scenario", "slope_mode", "n_species", "phi", "sigma_env", "rho_env_requested"]
    summary = (
        df.groupby(group_cols, as_index=False)[
            ["frac_exp_clipped_high", "frac_exp_clipped_low", "frac_floor"]
        ]
        .agg(["mean", "max"])
    )
    summary.columns = [
        "_".join([part for part in col if part]).rstrip("_")
        if isinstance(col, tuple)
        else str(col)
        for col in summary.columns.to_flat_index()
    ]
    return pd.DataFrame(summary).sort_values("scenario").reset_index(drop=True)


def write_guard_summary_markdown(summary: pd.DataFrame, out_path: Path) -> None:
    """Write the markdown companion for summarized numerical guards."""
    md_lines = [
        "# Numerical Guard Diagnostics Summary",
        "",
        "Derived from `analysis/reports/numerical_guard_rates.csv`.",
        "",
        "| scenario | frac_exp_clipped_high_mean | frac_exp_clipped_low_mean | frac_floor_mean | frac_floor_max |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for _, row in summary.iterrows():
        md_lines.append(
            "| {scenario} | {hi:.4f} | {lo:.4f} | {fm:.4f} | {fx:.4f} |".format(
                scenario=row["scenario"],
                hi=float(row["frac_exp_clipped_high_mean"]),
                lo=float(row["frac_exp_clipped_low_mean"]),
                fm=float(row["frac_floor_mean"]),
                fx=float(row["frac_floor_max"]),
            )
        )
    out_path.write_text("\n".join(md_lines) + "\n", encoding="utf-8")


def validate_phi_run_lengths(
    phi_runs: dict[str, pd.DataFrame],
    *,
    expected_steps: int = 400,
    expected_burn: int = 200,
) -> None:
    """Verify cached phi-sensitivity runs match documented time-series lengths."""
    for key, df in phi_runs.items():
        if "n_steps" not in df.columns or "burn_in" not in df.columns:
            print(
                f"{key} is missing n_steps/burn_in columns; "
                f"cannot validate expected {expected_steps}/{expected_burn}."
            )
            continue

        steps = sorted(int(x) for x in np.unique(df["n_steps"]))
        burn = sorted(int(x) for x in np.unique(df["burn_in"]))
        if steps != [expected_steps] or burn != [expected_burn]:
            raise ValueError(
                f"{key} has n_steps={steps}, burn_in={burn}; "
                f"expected {expected_steps}/{expected_burn} for phi-sensitivity grids."
            )


def copy_existing_files(
    paths: Iterable[Path],
    target_dir: Path,
    *,
    logger: Callable[[str], None] = print,
) -> None:
    """Copy existing files into a target directory, skipping missing ones."""
    target_dir.mkdir(parents=True, exist_ok=True)
    for path in paths:
        if path.exists():
            target = target_dir / path.name
            target.write_bytes(path.read_bytes())
            logger(f"Copied {path} -> {target}")
        else:
            logger(f"Warning: missing file {path}")


def remove_existing_files(paths: Iterable[Path], *, logger: Callable[[str], None] = print) -> None:
    """Delete stale files if they exist."""
    for path in paths:
        if path.exists():
            path.unlink()
            logger(f"Removed legacy file {path}")
