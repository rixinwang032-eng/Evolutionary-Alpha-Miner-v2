"""Command line interface for the synthetic search demo."""

from __future__ import annotations

import argparse
import json

from .data import SEED_POOL
from .search import run_round


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a reproducible synthetic alpha search round.")
    parser.add_argument("--pairs", type=int, default=12, help="number of parent pairs to sample")
    parser.add_argument("--seed", type=int, default=7, help="random seed")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.pairs < 0:
        raise SystemExit("--pairs must be non-negative")
    result = run_round(SEED_POOL, n_pairs=args.pairs, random_seed=args.seed)
    payload = {
        "seed_count": len(result.seeds),
        "candidate_count": len(result.scored_candidates),
        "passed_count": len(result.passed),
        "feedback": result.feedback_summary(),
    }
    if args.json:
        print(json.dumps(payload, sort_keys=True))
    else:
        print("Evolutionary Alpha Miner synthetic round")
        print(
            f"Seeds: {payload['seed_count']} | Candidates: {payload['candidate_count']} "
            f"| Passed: {payload['passed_count']}"
        )
        for bucket, count in payload["feedback"].items():
            print(f"  {bucket}: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
