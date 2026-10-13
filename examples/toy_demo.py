"""Run the public synthetic demonstration.

The implementation lives in :mod:`alpha_miner`; this wrapper keeps the
original ``python examples/toy_demo.py`` entry point working from a checkout.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from alpha_miner.cli import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
