"""Create, run, combine, and validate specification-defined production grids."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from insurance_sim.production import (
    combine_shards,
    create_manifest_from_spec,
    iter_shard_ids,
    load_manifest,
    pending_shards,
    run_pending_shards,
    run_shard,
    validate_combined_file,
    write_manifest,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    create = subparsers.add_parser("create", help="Create a manifest from a versioned JSON spec")
    create.add_argument("--spec", type=Path, required=True)
    create.add_argument("--output", type=Path, required=True)
    create.add_argument("--run-id", default=None, help="Optional run ID override")

    run_one = subparsers.add_parser("run-shard", help="Run one shard")
    run_one.add_argument("--manifest", type=Path, required=True)
    run_one.add_argument("--shard-id", required=True)
    run_one.add_argument("--force", action="store_true")

    run_pending = subparsers.add_parser("run-pending", help="Run all missing shards")
    run_pending.add_argument("--manifest", type=Path, required=True)
    run_pending.add_argument("--max-shards", type=int, default=None)
    run_pending.add_argument("--jobs", type=int, default=1)
    run_pending.add_argument("--force", action="store_true")

    pending = subparsers.add_parser("pending", help="List pending shard IDs")
    pending.add_argument("--manifest", type=Path, required=True)

    list_shards = subparsers.add_parser("list-shards", help="List all shard IDs")
    list_shards.add_argument("--manifest", type=Path, required=True)

    combine = subparsers.add_parser("combine", help="Combine and validate shard outputs")
    combine.add_argument("--manifest", type=Path, required=True)
    combine.add_argument("--output", type=Path, required=True)
    combine.add_argument("--validation-output", type=Path, default=None)

    validate = subparsers.add_parser("validate", help="Validate a combined output file")
    validate.add_argument("--manifest", type=Path, required=True)
    validate.add_argument("--combined", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.command == "create":
        spec = json.loads(args.spec.read_text(encoding="utf-8"))
        manifest = create_manifest_from_spec(spec, run_id_override=args.run_id)
        write_manifest(manifest, args.output)
        print(
            f"Wrote {args.output} with {manifest['scenario_count']} scenarios, "
            f"{manifest['shard_count']} shards, and {manifest['expected_rows']} expected rows"
        )
        return

    if args.command == "run-shard":
        print(run_shard(args.manifest, args.shard_id, force=args.force))
        return

    if args.command == "run-pending":
        paths = run_pending_shards(
            args.manifest,
            max_shards=args.max_shards,
            force=args.force,
            jobs=args.jobs,
        )
        print(f"Ran {len(paths)} shard(s)")
        return

    if args.command == "pending":
        for shard_id in pending_shards(args.manifest):
            print(shard_id)
        return

    if args.command == "list-shards":
        for shard_id in iter_shard_ids(load_manifest(args.manifest)):
            print(shard_id)
        return

    if args.command == "combine":
        frame = combine_shards(args.manifest, args.output, validation_path=args.validation_output)
        print(f"Wrote {len(frame)} rows to {args.output}")
        return

    if args.command == "validate":
        summary = validate_combined_file(args.manifest, args.combined)
        print(f"Validated {summary['rows']} rows across {summary['scenario_count']} scenarios")
        return

    raise ValueError(f"Unhandled command: {args.command}")


if __name__ == "__main__":
    main()
