import numpy as np

from nf_loto_platform.ml_analysis import metrics


def test_smape_basic_symmetry():
    y = [100, 200, 300]
    yhat = [110, 190, 310]
    v1 = metrics.smape(y, yhat)
    v2 = metrics.smape(yhat, y)
    assert v1 == v2
    assert 0 <= v1 <= 200


def test_mape_zero_guard():
    y = [0.0, 1.0]
    yhat = [0.0, 2.0]
    v = metrics.mape(y, yhat)
    assert v >= 0


def test_mae_and_rmse_on_constant_offset():
    y = np.array([0.0, 1.0, 2.0])
    yhat = y + 1.0
    mae_val = metrics.mae(y, yhat)
    rmse_val = metrics.rmse(y, yhat)
    assert mae_val == 1.0
    assert rmse_val == 1.0


def test_pinball_loss_monotonic_in_q():
    y = [0.0, 1.0, 2.0]
    yhat = [0.5, 1.5, 2.5]
    v_low = metrics.pinball_loss(y, yhat, q=0.1)
    v_mid = metrics.pinball_loss(y, yhat, q=0.5)
    v_high = metrics.pinball_loss(y, yhat, q=0.9)
    assert v_low <= v_mid <= v_high


def test_coverage_basic():
    y = [0.0, 1.0, 2.0, 3.0]
    lower = [-1.0, 0.5, 1.5, 10.0]
    upper = [1.0, 1.5, 2.5, 20.0]
    c = metrics.coverage(y, lower, upper)
    # 3/4 が区間内
    assert abs(c - 0.75) < 1e-9
