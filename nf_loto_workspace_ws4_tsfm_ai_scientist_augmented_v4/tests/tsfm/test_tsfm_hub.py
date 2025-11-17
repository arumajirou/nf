"""TSFMHub と BaseTSFMAdapter の最小テスト."""

from __future__ import annotations

import pandas as pd

from nf_loto_platform.tsfm.base import (
    TSFMCapabilities,
    TSFMHub,
    BaseTSFMAdapter,
)


class _DummyAdapter(BaseTSFMAdapter):
    def predict(self, history: pd.DataFrame, horizon: int, exogenous=None):
        raise NotImplementedError  # 実装はテストでは不要


def test_tsfmhub_register_and_select():
    hub = TSFMHub()

    cap_uni = TSFMCapabilities(
        provider="test",
        model_id="uni",
        input_arity="univariate",
        max_horizon=10,
    )
    cap_multi = TSFMCapabilities(
        provider="test",
        model_id="multi",
        input_arity="multivariate",
        max_horizon=None,
    )

    a1 = _DummyAdapter(name="uni_model", capabilities=cap_uni)
    a2 = _DummyAdapter(name="multi_model", capabilities=cap_multi)

    hub.register(a1)
    hub.register(a2)

    assert set(hub.list_names()) == {"multi_model", "uni_model"}

    # horizon=5, series=1 → 両方サポート可
    selected = hub.select_supported(horizon=5, num_series=1, num_features=1)
    assert {a.name for a in selected} == {"uni_model", "multi_model"}

    # horizon=20 → max_horizon=10 の方は外れる
    selected2 = hub.select_supported(horizon=20, num_series=1, num_features=1)
    assert {a.name for a in selected2} == {"multi_model"}

    # multivariate だが adapter が univariate 限定の場合は除外される
    selected3 = hub.select_supported(horizon=5, num_series=3, num_features=2)
    assert {a.name for a in selected3} == {"multi_model"}
