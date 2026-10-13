"""End-to-end search round orchestration."""

from __future__ import annotations

from dataclasses import dataclass

from .core import Candidate, Seed, build_seed_pool, generate_candidate, sample_diverse_pairs
from .evaluation import EvaluationResult, evaluate_candidate


@dataclass(frozen=True, slots=True)
class ScoredCandidate:
    candidate: Candidate
    result: EvaluationResult


@dataclass(frozen=True, slots=True)
class SearchResult:
    seeds: tuple[Seed, ...]
    scored_candidates: tuple[ScoredCandidate, ...]

    @property
    def passed(self) -> tuple[ScoredCandidate, ...]:
        return tuple(item for item in self.scored_candidates if item.result.status == "passed")

    def feedback_summary(self) -> dict[str, int]:
        summary: dict[str, int] = {}
        for item in self.scored_candidates:
            summary[item.result.feedback_bucket] = summary.get(item.result.feedback_bucket, 0) + 1
        return dict(sorted(summary.items()))


def run_round(
    raw_pool: list[tuple[str, str]] | tuple[tuple[str, str], ...],
    *,
    n_pairs: int = 16,
    random_seed: int = 7,
) -> SearchResult:
    """Build, pair, mutate and evaluate one reproducible search round."""
    seeds = build_seed_pool(raw_pool, random_seed=random_seed)
    pairs = sample_diverse_pairs(seeds, n_pairs=n_pairs, random_seed=random_seed + 4)
    scored_items: list[ScoredCandidate] = []
    for index, pair in enumerate(pairs):
        candidate = generate_candidate(pair, random_seed=random_seed + index)
        scored_items.append(ScoredCandidate(candidate, evaluate_candidate(candidate, random_seed)))
    scored = tuple(scored_items)
    return SearchResult(tuple(seeds), scored)
