"""Command-line entry point for ulid-cli."""
from __future__ import annotations

import argparse
import sys

from .core import generate_ulid


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="ulid-cli",
        description="Generate ULIDs (Universally Unique Lexicographically Sortable Identifiers).",
    )
    parser.add_argument("--count", type=int, default=1, help="Number of ULIDs to generate (default: 1)")
    parser.add_argument(
        "--timestamp",
        type=int,
        metavar="UNIX_MS",
        help="Generate for a specific Unix timestamp in milliseconds, instead of now",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.count < 1:
        print("ulid-cli: error: --count must be at least 1", file=sys.stderr)
        return 2

    try:
        for _ in range(args.count):
            print(generate_ulid(timestamp_ms=args.timestamp))
    except ValueError as exc:
        print(f"ulid-cli: error: {exc}", file=sys.stderr)
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
