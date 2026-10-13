import pytest

from alpha_miner.core import (
    build_seed_pool,
    family_hash,
    normalize_expression,
    sample_diverse_pairs,
)
from alpha_miner.data import SEED_POOL


def test_normalization_collapses_whitespace_and_numbers():
    assert normalize_expression(" Rank( close / 5 ) ") == "rank(close/N)"
    assert family_hash("rank(close / 5)") == family_hash("rank(close / 20)")


def test_seed_pool_is_deterministic_and_deduplicated():
    first = build_seed_pool(SEED_POOL, random_seed=3)
    second = build_seed_pool(SEED_POOL, random_seed=3)
    assert first == second
    assert len({seed.family_hash for seed in first}) == len(first)


def test_pair_sampling_is_deterministic_and_family_aware():
    seeds = build_seed_pool(SEED_POOL)
    first = sample_diverse_pairs(seeds, n_pairs=10, random_seed=12)
    second = sample_diverse_pairs(seeds, n_pairs=10, random_seed=12)
    assert first == second
    assert all(pair.a.family_hash != pair.b.family_hash for pair in first)
    assert len({pair.pair_id for pair in first}) == len(first)


def test_invalid_arguments_are_rejected():
    with pytest.raises(ValueError):
        normalize_expression(" ")
    with pytest.raises(ValueError):
        sample_diverse_pairs([], n_pairs=-1)
