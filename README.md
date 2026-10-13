# Evolutionary Alpha Miner

![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![CI](https://github.com/rixinwang032-eng/Evolutionary-Alpha-Miner-v2/actions/workflows/ci.yml/badge.svg)

Evolutionary Alpha Miner is a reproducible research toolkit for family-aware symbolic alpha discovery. It keeps the original research idea intact: normalize seed expressions, avoid duplicate families, sample diverse A-B parents, generate constrained hybrids, and feed evaluation results back into the search loop.

The public repository uses synthetic expressions and a deterministic fake evaluator. It contains no credentials, private formulas, proprietary datasets, or real simulation output.

## Why this version

The original prototype was a single demonstration script. This version makes the workflow importable and testable:

- deterministic random streams instead of global random state
- immutable, typed data models for seeds, pairs, candidates, and results
- bounded parent sampling with explicit validation
- a reusable `run_round` orchestration API
- a small CLI with human-readable and JSON output
- unit tests and a Python 3.10-3.12 GitHub Actions matrix
- no runtime dependencies; development tools are optional

## Quickstart

```bash
git clone https://github.com/rixinwang032-eng/Evolutionary-Alpha-Miner-v2.git
cd Evolutionary-Alpha-Miner-v2
python -m venv .venv
# macOS/Linux: source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -e .
alpha-miner --pairs 18 --seed 7
```

For machine-readable output:

```bash
alpha-miner --pairs 18 --seed 7 --json
```

The original checkout-friendly demo entry point remains available:

```bash
python examples/toy_demo.py --pairs 18 --seed 7
```

## Python API

```python
from alpha_miner import run_round
from alpha_miner.data import SEED_POOL

result = run_round(SEED_POOL, n_pairs=12, random_seed=7)
print(result.feedback_summary())
for item in result.passed:
    print(item.candidate.expression, item.result.fitness)
```

## Development

```bash
python -m pip install -e ".[dev]"
python -m pytest
python -m alpha_miner.cli --pairs 4 --seed 11 --json
```

The evaluator in `src/alpha_miner/evaluation.py` is deliberately synthetic. A real research integration should replace it with an explicitly permitted simulator adapter while keeping the same result contract.

## Repository layout

```text
src/alpha_miner/   reusable search primitives and CLI
examples/          public synthetic demo
tests/             deterministic behavior and API tests
.github/workflows/ continuous integration
```

## Scope and disclaimer

This project is for research and educational purposes only. It does not provide financial advice, investment advice, trading signals, or proprietary alpha formulas. Any included expression is synthetic.

Contributions should preserve the sanitized public scope. See [CONTRIBUTING.md](CONTRIBUTING.md) and [ROADMAP.md](ROADMAP.md).
