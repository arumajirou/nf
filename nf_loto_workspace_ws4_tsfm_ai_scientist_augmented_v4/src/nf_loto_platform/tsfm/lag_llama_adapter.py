from __future__ import annotations

from typing import Mapping

import pandas as pd

from .base import BaseTSFMAdapter, ForecastResult, TSFMCapabilities


class LagLlamaAdapter(BaseTSFMAdapter):
    """time-series-foundation-models/Lag-Llama 用アダプタの雛形."""

    def __init__(self, model_id: str = "time-series-foundation-models/Lag-Llama") -> None:
        super().__init__(
            name="Lag-Llama",
            capabilities=TSFMCapabilities(
                provider="tsfm-community",
                model_id=model_id,
                task_types=["forecasting"],
                input_arity="univariate",
                supports_exogenous=False,
                zero_shot=True,
                finetuneable=True,
                max_context_length=None,
                max_horizon=None,
                license="Apache-2.0-or-similar",
                commercial_allowed=True,
                hardware_pref="gpu-recommended",
            ),
        )

    def predict(  # pragma: no cover - 実際の統合は別フェーズ
        self,
        history: pd.DataFrame,
        horizon: int,
        exogenous: Mapping[str, pd.DataFrame] | None = None,
    ) -> ForecastResult:
        raise NotImplementedError(
            "LagLlamaAdapter.predict はまだ実装されていません。"
            "lag-llama リポジトリの実装を参照して統合してください。"
        )
