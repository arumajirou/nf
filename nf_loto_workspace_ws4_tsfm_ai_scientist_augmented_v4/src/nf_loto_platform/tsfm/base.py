from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Iterable, Mapping, Optional, Sequence

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class TSFMCapabilities:
    """TSFM モデルの能力・制約に関するメタデータ."""

    provider: str
    model_id: str
    task_types: Sequence[str] = field(default_factory=lambda: ["forecasting"])
    input_arity: str = "univariate"  # "univariate" / "multivariate" / "both"
    supports_exogenous: bool = False
    zero_shot: bool = True
    finetuneable: bool = False
    max_context_length: Optional[int] = None
    max_horizon: Optional[int] = None
    license: str = ""
    commercial_allowed: bool = True
    hardware_pref: str = "gpu-recommended"  # "cpu-ok" / "gpu-recommended" / "gpu-required"


@dataclass
class CostEstimate:
    """推論コストのざっくりした見積もり."""

    expected_latency_ms: float
    expected_memory_mb: float
    notes: str = ""


@dataclass
class ForecastResult:
    """TSFMAdapter からの予測結果."""

    yhat: pd.DataFrame  # 必須列: ["unique_id", "ds", "y_hat"]
    raw_output: Any | None = None
    meta: Dict[str, Any] = field(default_factory=dict)


class BaseTSFMAdapter:
    """すべての TSFM アダプタが従う共通インターフェイス."""

    name: str
    capabilities: TSFMCapabilities

    def __init__(self, name: str, capabilities: TSFMCapabilities) -> None:
        self.name = name
        self.capabilities = capabilities

    # --- メインの API -------------------------------------------------

    def supports(
        self,
        horizon: int,
        num_series: int,
        num_features: int,
    ) -> bool:
        """このタスク設定でモデルが利用可能かをざっくり判定する."""
        if self.capabilities.max_horizon is not None and horizon > self.capabilities.max_horizon:
            return False
        # ここでは簡易に univariate/multivariate だけ見る
        if self.capabilities.input_arity == "univariate" and num_series > 1:
            return False
        return True

    def estimate_cost(self, horizon: int, num_series: int) -> CostEstimate:
        """ごく粗い推論コスト見積もりを返す.

        ここでは実装依存のマジックナンバーを避け、モデルサイズに応じた
        大まかな分類を capabilities.hardware_pref から想定する。
        """
        base_latency = 50.0
        if self.capabilities.hardware_pref == "gpu-required":
            base_latency = 200.0
        elif self.capabilities.hardware_pref == "gpu-recommended":
            base_latency = 100.0
        # horizon と series 数に線形比例すると仮定
        expected_latency_ms = base_latency * max(1.0, horizon / 32.0) * max(1.0, num_series / 4.0)
        expected_memory_mb = 512.0
        return CostEstimate(expected_latency_ms=expected_latency_ms, expected_memory_mb=expected_memory_mb)

    # 実際のモデル呼び出しを行うメソッド。
    # 実装クラスでは、必要に応じて Hugging Face / 専用ライブラリを import する。
    def predict(
        self,
        history: pd.DataFrame,
        horizon: int,
        exogenous: Mapping[str, pd.DataFrame] | None = None,
    ) -> ForecastResult:  # pragma: no cover - 具象クラスでテスト
        raise NotImplementedError


class TSFMHub:
    """複数 TSFMAdapter を一括管理するハブクラス."""

    def __init__(self) -> None:
        self._adapters: Dict[str, BaseTSFMAdapter] = {}

    def register(self, adapter: BaseTSFMAdapter) -> None:
        if adapter.name in self._adapters:
            raise ValueError(f"adapter {adapter.name!r} is already registered")
        self._adapters[adapter.name] = adapter

    def get(self, name: str) -> BaseTSFMAdapter:
        try:
            return self._adapters[name]
        except KeyError as exc:  # pragma: no cover - 単純なガード
            raise KeyError(f"TSFM adapter {name!r} is not registered") from exc

    def list_names(self) -> Sequence[str]:
        return sorted(self._adapters.keys())

    def select_supported(
        self,
        horizon: int,
        num_series: int,
        num_features: int,
    ) -> Sequence[BaseTSFMAdapter]:
        """タスク設定に対応可能なアダプタだけをフィルタする."""
        return [
            a
            for a in self._adapters.values()
            if a.supports(horizon=horizon, num_series=num_series, num_features=num_features)
        ]
