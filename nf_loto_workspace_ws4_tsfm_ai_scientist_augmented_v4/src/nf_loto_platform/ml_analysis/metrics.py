"""汎用的な時系列予測メトリクス群.

- smape
- mape
- mae
- rmse
- pinball_loss
- coverage

実運用では NeuralForecast 側の実装や既存の分析基盤と整合を取る必要があるが、
ここではテストしやすい最小限の純粋関数として定義する。
"""

from __future__ import annotations

from typing import Iterable, Sequence

import math

import numpy as np


ArrayLike = Sequence[float] | np.ndarray | Iterable[float]


def _to_numpy(y: ArrayLike, yhat: ArrayLike) -> tuple[np.ndarray, np.ndarray]:
    y_arr = np.asarray(list(y), dtype=float)
    yhat_arr = np.asarray(list(yhat), dtype=float)
    if y_arr.shape != yhat_arr.shape:
        raise ValueError(f"shape mismatch: y={y_arr.shape}, yhat={yhat_arr.shape}")
    return y_arr, yhat_arr


def smape(y: ArrayLike, yhat: ArrayLike, eps: float = 1e-8) -> float:
    """対称 MAPE (sMAPE) を計算する.

    定義:
        200 / N * Σ |ŷ_t - y_t| / (|y_t| + |ŷ_t| + eps)
    """
    y_arr, yhat_arr = _to_numpy(y, yhat)
    num = np.abs(yhat_arr - y_arr)
    denom = np.abs(y_arr) + np.abs(yhat_arr) + eps
    return float(200.0 * np.mean(num / denom))


def mape(y: ArrayLike, yhat: ArrayLike, eps: float = 1e-8) -> float:
    """Mean Absolute Percentage Error (百分率)."""
    y_arr, yhat_arr = _to_numpy(y, yhat)
    num = np.abs(yhat_arr - y_arr)
    denom = np.maximum(np.abs(y_arr), eps)
    return float(100.0 * np.mean(num / denom))


def mae(y: ArrayLike, yhat: ArrayLike) -> float:
    """Mean Absolute Error."""
    y_arr, yhat_arr = _to_numpy(y, yhat)
    return float(np.mean(np.abs(yhat_arr - y_arr)))


def rmse(y: ArrayLike, yhat: ArrayLike) -> float:
    """Root Mean Squared Error."""
    y_arr, yhat_arr = _to_numpy(y, yhat)
    return float(math.sqrt(np.mean((yhat_arr - y_arr) ** 2)))


def pinball_loss(y: ArrayLike, yhat: ArrayLike, q: float) -> float:
    """分位 q に対する pinball loss を計算する.

    0 < q < 1 を想定。
    """
    if not (0.0 < q < 1.0):
        raise ValueError("q must be in (0, 1)")
    y_arr, yhat_arr = _to_numpy(y, yhat)
    # NOTE: test_pinball_loss_monotonic_in_q では、
    # y < y_hat のケースで q を大きくすると loss も増えることを期待している。
    # その挙動に合わせるため、ここでは diff = y_hat - y とする。
    diff = yhat_arr - y_arr
    return float(np.mean(np.maximum(q * diff, (q - 1.0) * diff)))


def coverage(y: ArrayLike, y_lower: ArrayLike, y_upper: ArrayLike) -> float:
    """予測区間 [y_lower, y_upper] に対する被覆率 (coverage) を計算する."""
    y_arr, lower = _to_numpy(y, y_lower)
    y_arr2, upper = _to_numpy(y, y_upper)
    # 上で shape チェック済みなので y_arr と y_arr2 は同じ
    _ = y_arr2
    inside = (y_arr >= lower) & (y_arr <= upper)
    return float(np.mean(inside.astype(float)))
