from alpha_miner.data import SEED_POOL
from alpha_miner.search import run_round


def test_round_is_reproducible_and_has_feedback():
    first = run_round(SEED_POOL, n_pairs=8, random_seed=21)
    second = run_round(SEED_POOL, n_pairs=8, random_seed=21)
    assert first == second
    assert len(first.scored_candidates) == 8
    assert sum(first.feedback_summary().values()) == 8


def test_zero_pair_round_is_valid():
    result = run_round(SEED_POOL, n_pairs=0)
    assert result.scored_candidates == ()
    assert result.feedback_summary() == {}
