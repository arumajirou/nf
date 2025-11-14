import os
import sys
from pathlib import Path

# Ensure the project src/ is importable regardless of the current working directory.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = PROJECT_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

import numpy as np
import pandas as pd

from nf_analysis import model_stats


def test_diebold_mariano_identical_errors_yields_nan_or_large_p():
    e = pd.Series(np.ones(50))
    res = model_stats.diebold_mariano(e, e.copy(), h=1, loss="mse")
    # Depending on numerical path this may end up with var_d ≈ 0
    # in which case we expect NaNs; otherwise p-value should be near 1.
    if not np.isnan(res["p_value"]):
        assert res["p_value"] > 0.5


def test_diebold_mariano_detects_difference_in_mse():
    rng = np.random.RandomState(0)
    true = rng.normal(size=200)
    # Model 1 is relatively accurate, model 2 is noisy.
    e1 = true + rng.normal(scale=0.1, size=200)
    e2 = true + rng.normal(scale=1.0, size=200)

    res = model_stats.diebold_mariano(pd.Series(e1), pd.Series(e2), h=1, loss="mse")
    assert not np.isnan(res["stat"])
    assert res["p_value"] < 0.1
