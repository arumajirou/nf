import math
import random
from typing import List

import numpy as np
import pytest

try:  # torch はオプション扱い
    import torch
    _TORCH_AVAILABLE = True
except Exception:  # pragma: no cover - 環境依存
    torch = None
    _TORCH_AVAILABLE = False


def _run_numpy_random_pipeline(seed: int) -> float:
    """標準ライブラリ + NumPy の乱数パイプラインを 1 本実行するヘルパー。

    同じ seed を渡したときに完全に同じ結果が返ることを検証対象とする。
    """
    random.seed(seed)
    np.random.seed(seed)

    # Python の random と NumPy の両方を混在させる
    python_samples: List[float] = [random.random() for _ in range(128)]
    numpy_samples = np.random.randn(256).astype("float64")

    combined = numpy_samples * np.mean(python_samples) + np.std(python_samples)
    # 結果を 1 スカラーに集約（安定比較用）
    return float(combined.mean())


@pytest.mark.nonfunctional
def test_reproducibility_seed_numpy_python():
    """Python random + NumPy を同一 seed で 2 回実行すると結果が一致すること。"""
    seed = 12345
    v1 = _run_numpy_random_pipeline(seed)
    v2 = _run_numpy_random_pipeline(seed)

    # 完全一致を要求（CPU/OS 差異の影響を受けない軽量な計算）
    assert v1 == v2


@pytest.mark.nonfunctional
@pytest.mark.skipif(not _TORCH_AVAILABLE, reason="torch がインストールされていない環境ではスキップ")
def test_reproducibility_seed_torch_linear():
    """torch が利用可能な場合、シンプルな線形モデル学習の再現性を確認する。"""
    assert torch is not None  # for type checkers

    seed = 2024

    def run_once() -> torch.Tensor:
        torch.manual_seed(seed)
        # CPU 前提のごく小さな線形回帰を 1 ステップだけ回す
        x = torch.randn(32, 4)
        w = torch.randn(4, 1, requires_grad=True)
        y = x @ w + 0.1 * torch.randn(32, 1)

        optim = torch.optim.SGD([w], lr=0.1)
        loss_fn = torch.nn.MSELoss()

        optim.zero_grad()
        loss = loss_fn(x @ w, y)
        loss.backward()
        optim.step()

        return w.detach().clone()

    w1 = run_once()
    w2 = run_once()

    # 浮動小数のわずかな差分を考慮して allclose で比較
    assert torch.allclose(w1, w2, atol=1e-8, rtol=0.0)
