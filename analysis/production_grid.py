"""Shardable production runner for insurance-hypothesis simulation grids."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from insurance_sim.production import (
    combine_shards,
    create_manifest,
    create_manifest_from_spec,
    iter_shard_ids,
    load_manifest,
    parse_float_list,
    parse_int_list,
    parse_str_list,
    pending_shards,
    run_pending_shards,
    run_shard,
    validate_combined_file,
    write_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Create and run production simulation grids")
    subparsers = parser.add_subparsers(dest="command", required=True)

    manifest = subparsers.add_parser("create-manifest", help="Write a production grid manifest")
    manifest.add_argument("--output", type=Path, required=True, help="Path to manifest JSON")
    manifest.add_argument("--run-id", required=True, help="Stable run identifier")
    manifest.add_argument("--reps", type=int, default=1000, help="Replicates per scenario")
    manifest.add_argument("--replicates-per-shard", type=int, default=100, help="Replicates per shard")
    manifest.add_argument("--steps", type=int, default=600, help="Total time steps")
    manifest.add_argument("--burn", type=int, default=300, help="Burn-in steps")
    manifest.add_argument("--phi", type=float, default=0.4, help="AR(1) persistence")
    manifest.add_argument("--alpha-inter", type=float, default=0.3, help="Interspecific competition coefficient")
    manifest.add_argument("--base-seed", type=int, default=12345, help="Base seed for deterministic replicate seeds")
    manifest.add_argument(
        "--sigma-list",
        default="0,0.2,0.5,1.0,1.5",
        help="Comma-separated sigma_env values",
    )
    manifest.add_argument(
        "--rho-list",
        default="-0.5,0,0.5,0.9,1.0",
        help="Comma-separated rho_env values",
    )
    manifest.add_argument("--species-list", default="4", help="Comma-separated species richness values")
    manifest.add_argument(
        "--slope-modes",
        default="mixed,positive",
        help="Comma-separated slope modes",
    )

    manifest_spec = subparsers.add_parser(
        "create-manifest-from-spec",
        help="Write a production grid manifest from a JSON spec",
    )
    manifest_spec.add_argument("--spec", type=Path, required=True, help="Path to production spec JSON")
    manifest_spec.add_argument("--output", type=Path, required=True, help="Path to manifest JSON")
    manifest_spec.add_argument("--run-id", default=None, help="Optional run ID override")

    run_one = subparsers.add_parser("run-shard", help="Run one shard from an existing manifest")
    run_one.add_argument("--manifest", type=Path, required=True)
    run_one.add_argument("--shard-id", required=True)
    run_one.add_argument("--force", action="store_true", help="Overwrite existing shard output")

    run_pending = subparsers.add_parser("run-pending", help="Run missing shards sequentially")
    run_pending.add_argument("--manifest", type=Path, required=True)
    run_pending.add_argument("--max-shards", type=int, default=None, help="Optional cap for smoke runs")
    run_pending.add_argument("--jobs", type=int, default=1, help="Number of shard workers")
    run_pending.add_argument("--force", action="store_true", help="Overwrite existing shard outputs")

    pending = subparsers.add_parser("pending", help="List pending shard IDs")
    pending.add_argument("--manifest", type=Path, required=True)

    list_shards = subparsers.add_parser("list-shards", help="List all shard IDs")
    list_shards.add_argument("--manifest", type=Path, required=True)

    combine = subparsers.add_parser("combine", help="Combine and validate all shard outputs")
    combine.add_argument("--manifest", type=Path, required=True)
    combine.add_argument("--output", type=Path, required=True)
    combine.add_argument("--validation-output", type=Path, default=None)

    validate = subparsers.add_parser("validate", help="Validate a combined output file")
    validate.add_argument("--manifest", type=Path, required=True)
    validate.add_argument("--combined", type=Path, required=True)

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if args.command == "create-manifest":
        manifest = create_manifest(
            run_id=args.run_id,
            reps_per_scenario=args.reps,
            replicates_per_shard=args.replicates_per_shard,
            sigma_vals=parse_float_list(args.sigma_list),
            rho_vals=parse_float_list(args.rho_list),
            species_vals=parse_int_list(args.species_list),
            slope_modes=parse_str_list(args.slope_modes),
            phi=args.phi,
            steps=args.steps,
            burn=args.burn,
            alpha_inter=args.alpha_inter,
            base_seed=args.base_seed,
        )
        write_manifest(manifest, args.output)
        print(
            "Wrote {path} with {scenarios} scenarios, {shards} shards, {rows} expected rows".format(
                path=args.output,
                scenarios=manifest["scenario_count"],
                shards=manifest["shard_count"],
                rows=manifest["expected_rows"],
            )
        )
        return

    if args.command == "create-manifest-from-spec":
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        manifest = create_manifest_from_spec(spec, run_id_override=args.run_id)
        write_manifest(manifest, args.output)
        print(
            "Wrote {path} with {scenarios} scenarios, {shards} shards, {rows} expected rows".format(
                path=args.output,
                scenarios=manifest["scenario_count"],
                shards=manifest["shard_count"],
                rows=manifest["expected_rows"],
            )
        )
        return

    if args.command == "run-shard":
        out_path = run_shard(args.manifest, args.shard_id, force=args.force)
        print(f"Wrote {out_path}")
        return

    if args.command == "run-pending":
        paths = run_pending_shards(
            args.manifest,
            max_shards=args.max_shards,
            force=args.force,
            jobs=args.jobs,
        )
        print(f"Ran {len(paths)} shard(s)")
        for path in paths:
            print(path)
        return

    if args.command == "pending":
        for shard_id in pending_shards(args.manifest):
            print(shard_id)
        return

    if args.command == "list-shards":
        manifest = load_manifest(args.manifest)
        for shard_id in iter_shard_ids(manifest):
            print(shard_id)
        return

    if args.command == "combine":
        frame = combine_shards(args.manifest, args.output, validation_path=args.validation_output)
        print(f"Wrote {len(frame)} rows to {args.output}")
        if args.validation_output is not None:
            print(f"Wrote validation report to {args.validation_output}")
        return

    if args.command == "validate":
        summary = validate_combined_file(args.manifest, args.combined)
        print(
            "Validated {rows} rows across {scenarios} scenarios".format(
                rows=summary["rows"],
                scenarios=summary["scenario_count"],
            )
        )
        return

    raise ValueError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    main()
