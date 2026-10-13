"""Public API for the Evolutionary Alpha Miner research toolkit."""

from .core import (
    Candidate,
    Pair,
    Seed,
    build_seed_pool,
    family_hash,
    generate_candidate,
    normalize_expression,
    sample_diverse_pairs,
)
from .evaluation import EvaluationResult, evaluate_candidate
from .search import SearchResult, run_round

__all__ = [
    "Candidate",
    "EvaluationResult",
    "Pair",
    "SearchResult",
    "Seed",
    "build_seed_pool",
    "evaluate_candidate",
    "family_hash",
    "generate_candidate",
    "normalize_expression",
    "run_round",
    "sample_diverse_pairs",
]

__version__ = "0.2.0"
