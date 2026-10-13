"""Synthetic evaluator and feedback categorization."""

from __future__ import annotations

import random
from dataclasses import dataclass

from .core import Candidate, short_hash


@dataclass(frozen=True, slots=True)
class EvaluationResult:
    sharpe: float
    fitness: float
    turnover: float
    status: str
    failed_checks: tuple[str, ...]

    @property
    def feedback_bucket(self) -> str:
        return "passed" if self.status == "passed" else ";".join(self.failed_checks)


def evaluate_candidate(candidate: Candidate, random_seed_offset: int = 0) -> EvaluationResult:
    """Evaluate a synthetic candidate deterministically.

    Replace this function with an adapter to a permitted simulator in real work.
    """
    seed = int(short_hash(candidate.expression, 12), 16) ^ random_seed_offset
    rng = random.Random(seed)
    base = 0.4
    if candidate.tag_pair in {"price+volume", "volume+price"}:
        base += 0.30
    if "option" in candidate.tag_pair:
        base += 0.25
    if "fundamental" in candidate.tag_pair:
        base += 0.18
    if "news" in candidate.tag_pair or "analyst" in candidate.tag_pair:
        base += 0.12
    if candidate.mutation_mode in {"weak_gate_hybrid", "regime_hybrid"}:
        base += 0.18
    if candidate.mutation_mode == "dataset_substitution":
        base -= 0.05

    sharpe = round(rng.gauss(base, 0.45), 3)
    fitness = round(sharpe * rng.uniform(0.5, 1.8), 3)
    turnover = round(rng.uniform(0.02, 0.65), 3)
    failures: list[str] = []
    if sharpe < 0.75:
        failures.append("LOW_SHARPE")
    if fitness < 0.60:
        failures.append("LOW_FITNESS")
    if turnover > 0.55:
        failures.append("HIGH_TURNOVER")
    if candidate.tag_pair in {"price+volume", "volume+price"} and rng.random() < 0.20:
        failures.append("SELF_CORRELATION")
    return EvaluationResult(
        sharpe,
        fitness,
        turnover,
        "passed" if not failures else "failed",
        tuple(failures),
    )
