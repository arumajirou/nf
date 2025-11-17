from __future__ import annotations

from typing import Mapping

import pandas as pd

from .base import BaseTSFMAdapter, ForecastResult, TSFMCapabilities


class TimesFMAdapter(BaseTSFMAdapter):
    """google/timesfm 系列向けのアダプタの雛形."""

    def __init__(self, model_id: str = "google/timesfm-2.5-200m-pytorch") -> None:
        super().__init__(
            name="TimesFM-2.5-200m",
            capabilities=TSFMCapabilities(
                provider="google",
                model_id=model_id,
                task_types=["forecasting"],
                input_arity="multivariate",
                supports_exogenous=True,
                zero_shot=True,
                finetuneable=True,
                max_context_length=16_384,
                max_horizon=1_000,
                license="Apache-2.0",
                commercial_allowed=True,
                hardware_pref="gpu-required",
            ),
        )

    def predict(  # pragma: no cover - 実際の統合は別フェーズ
        self,
        history: pd.DataFrame,
        horizon: int,
        exogenous: Mapping[str, pd.DataFrame] | None = None,
    ) -> ForecastResult:
        raise NotImplementedError(
            "TimesFMAdapter.predict はまだ実装されていません。"
            "google-research/timesfm の実装を参照して統合してください。"
        )
