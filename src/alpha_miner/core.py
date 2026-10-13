"""Core data structures and deterministic evolutionary search primitives."""

from __future__ import annotations

import hashlib
import random
import re
from dataclasses import dataclass

from .data import TAG_PAIR_TARGETS


@dataclass(frozen=True, slots=True)
class Seed:
    seed_id: str
    tag: str
    expression: str
    family_hash: str
    score: float


@dataclass(frozen=True, slots=True)
class Pair:
    pair_id: str
    a: Seed
    b: Seed
    tag_pair: str


@dataclass(frozen=True, slots=True)
class Candidate:
    candidate_name: str
    pair_id: str
    tag_pair: str
    parent_a: str
    parent_b: str
    mutation_mode: str
    expression: str
    hypothesis: str


def normalize_expression(expr: str) -> str:
    """Normalize whitespace and numeric constants for family comparison."""
    if not isinstance(expr, str) or not expr.strip():
        raise ValueError("expression must be a non-empty string")
    normalized = re.sub(r"\s+", "", expr.lower().strip())
    return re.sub(r"\d+\.\d+|\d+", "N", normalized)


def short_hash(text: str, length: int = 10) -> str:
    if length < 1:
        raise ValueError("length must be positive")
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:length]


def family_hash(expr: str) -> str:
    """Return a stable, non-secret identifier for a normalized expression."""
    return short_hash(normalize_expression(expr))


def build_seed_pool(
    raw_pool: list[tuple[str, str]] | tuple[tuple[str, str], ...], random_seed: int = 7
) -> list[Seed]:
    """Deduplicate seed families and assign reproducible synthetic quality scores."""
    rng = random.Random(random_seed)
    base_scores = {
        "price": 1.00,
        "volume": 0.90,
        "option": 0.75,
        "fundamental": 0.70,
        "analyst": 0.55,
        "news": 0.50,
        "unknown": 0.40,
    }
    seeds: list[Seed] = []
    seen_families: set[str] = set()
    for idx, (tag, expression) in enumerate(raw_pool, start=1):
        fh = family_hash(expression)
        if fh in seen_families:
            continue
        seen_families.add(fh)
        score = base_scores.get(tag, 0.40) + rng.random() * 0.60
        seeds.append(Seed(f"S{idx:03d}", tag, expression, fh, round(score, 4)))
    return seeds


def sample_diverse_pairs(
    seeds: list[Seed], n_pairs: int = 16, random_seed: int = 11, max_attempts: int = 1000
) -> list[Pair]:
    """Sample heterogeneous, non-duplicate A-B pairs with bounded retries."""
    if n_pairs < 0:
        raise ValueError("n_pairs must be non-negative")
    rng = random.Random(random_seed)
    by_tag: dict[str, list[Seed]] = {}
    for seed in seeds:
        by_tag.setdefault(seed.tag, []).append(seed)
    for values in by_tag.values():
        values.sort(key=lambda seed: seed.score, reverse=True)

    pairs: list[Pair] = []
    used_pair_hashes: set[str] = set()
    parent_usage: dict[str, int] = {}

    def pick(tag: str, excluded: set[str]) -> Seed | None:
        candidates = [seed for seed in by_tag.get(tag, []) if seed.family_hash not in excluded]
        if not candidates:
            return None
        weights = [
            max(0.05, seed.score) / (1 + parent_usage.get(seed.family_hash, 0))
            for seed in candidates
        ]
        return rng.choices(candidates, weights=weights, k=1)[0]

    attempts = 0
    while len(pairs) < n_pairs and attempts < max_attempts:
        attempts += 1
        a_tag, b_tag = TAG_PAIR_TARGETS[len(pairs) % len(TAG_PAIR_TARGETS)]
        a = pick(a_tag, set())
        b = pick(b_tag, {a.family_hash}) if a else None
        if a is None or b is None:
            continue
        pair_key = short_hash(f"{a.family_hash}::{b.family_hash}", 12)
        if pair_key in used_pair_hashes:
            continue
        used_pair_hashes.add(pair_key)
        parent_usage[a.family_hash] = parent_usage.get(a.family_hash, 0) + 1
        parent_usage[b.family_hash] = parent_usage.get(b.family_hash, 0) + 1
        pairs.append(Pair(f"P{len(pairs) + 1:04d}_{pair_key}", a, b, f"{a.tag}+{b.tag}"))
    return pairs


def generate_candidate(pair: Pair, random_seed: int | None = None) -> Candidate:
    """Create one constrained hybrid, preserving A as the main signal carrier."""
    rng = random.Random(random_seed) if random_seed is not None else random.Random()
    a, b = pair.a.expression, pair.b.expression
    templates = (
        (
            "weak_gate_hybrid",
            f"trade_when(rank({b}) > 0.55, {a}, -1)",
            "Use B as a weak gate while preserving A.",
        ),
        (
            "regime_hybrid",
            f"if_else(ts_rank({b}, 20) > 0.5, {a}, 0.5 * {a})",
            "Use B as a regime condition.",
        ),
        (
            "mild_corr_breaker",
            f"group_neutralize({a} * (1 + 0.1 * rank({b})), sector)",
            "Use B as a mild modifier.",
        ),
        (
            "dataset_substitution",
            f"rank({a}) + 0.05 * rank({b})",
            "Add a small heterogeneous component from B.",
        ),
    )
    mode, expression, hypothesis = rng.choice(templates)
    return Candidate(
        f"C_{pair.pair_id}",
        pair.pair_id,
        pair.tag_pair,
        pair.a.seed_id,
        pair.b.seed_id,
        mode,
        expression,
        hypothesis,
    )
