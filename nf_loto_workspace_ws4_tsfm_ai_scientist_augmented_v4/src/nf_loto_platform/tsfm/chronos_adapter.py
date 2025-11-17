from __future__ import annotations

from typing import Mapping

import pandas as pd

from .base import BaseTSFMAdapter, ForecastResult, TSFMCapabilities


class ChronosAdapter(BaseTSFMAdapter):
    """amazon/chronos-2 ファミリ向けのアダプタ.

    この実装はあくまで nf_loto_platform 側のインターフェイスを提供するものであり、
    実際のモデルロードや推論処理は別途 amazon/chronos-2 ライブラリをインストールして
    実装する必要がある。
    """

    def __init__(self, model_id: str = "amazon/chronos-2") -> None:
        super().__init__(
            name="Chronos2-ZeroShot",
            capabilities=TSFMCapabilities(
                provider="amazon",
                model_id=model_id,
                task_types=["forecasting"],
                input_arity="both",
                supports_exogenous=True,
                zero_shot=True,
                finetuneable=False,
                max_context_length=512,
                max_horizon=None,
                license="Apache-2.0",
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
            "ChronosAdapter.predict はまだ実装されていません。"
            "amazon/chronos-2 をインストールし、実際の推論コードを追加してください。"
        )
