from __future__ import annotations

from typing import Mapping

import pandas as pd

from .base import BaseTSFMAdapter, ForecastResult, TSFMCapabilities


class TempoPFNAdapter(BaseTSFMAdapter):
    """AutoML-org/TempoPFN 用アダプタの雛形 (一変量専用)."""

    def __init__(self, model_id: str = "AutoML-org/TempoPFN") -> None:
        super().__init__(
            name="TempoPFN-ZeroShot",
            capabilities=TSFMCapabilities(
                provider="automl-org",
                model_id=model_id,
                task_types=["forecasting"],
                input_arity="univariate",
                supports_exogenous=False,
                zero_shot=True,
                finetuneable=False,
                max_context_length=None,
                max_horizon=None,
                license="MIT-or-similar",
                commercial_allowed=True,
                hardware_pref="cpu-ok",
            ),
        )

    def predict(  # pragma: no cover - 実際の統合は別フェーズ
        self,
        history: pd.DataFrame,
        horizon: int,
        exogenous: Mapping[str, pd.DataFrame] | None = None,
    ) -> ForecastResult:
        raise NotImplementedError(
            "TempoPFNAdapter.predict はまだ実装されていません。"
            "AutoML-org/TempoPFN の推論 API を呼び出すコードを追加してください。"
        )
