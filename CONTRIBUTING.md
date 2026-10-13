# Contributing

Contributions are welcome when they improve reproducibility, tests, documentation, or the synthetic research workflow.

Please do not submit private alpha formulas, proprietary datasets, credentials, real platform output, or non-public notebooks. Synthetic examples are preferred.

## Development

```bash
python -m venv .venv
python -m pip install -e ".[dev]"
python -m pytest
alpha-miner --pairs 12 --seed 7
```

Keep changes focused, add a meaningful test for behavior changes, and update the README when the public API changes.
