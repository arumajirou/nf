import time

import pandas as pd
import numpy as np
import pytest

from nf_loto_platform.ml.model_runner import run_loto_experiment


class _DummyAutoModel:
    """テスト用の極小 AutoModel 代替実装。

    - fit: 入力をそのまま保持するだけ
    - predict: h ステップ先の ds を生成し、0.0 の y_hat を返すだけ
    """

    def __init__(self, h: int) -> None:
        self._h = h
        self._fitted_df = None

    # 実際の AutoModel/NeuralForecast のインターフェースに寄せる
    def fit(
        self,
        df: pd.DataFrame,
        val_size: int | None = None,
        futr_exog_list=None,
        hist_exog_list=None,
        stat_exog_list=None,
    ) -> None:
        self._fitted_df = df.copy()

    def predict(
        self,
        df: pd.DataFrame,
        h: int,
        futr_exog_list=None,
        hist_exog_list=None,
        stat_exog_list=None,
    ) -> pd.DataFrame:
        assert self._fitted_df is not None
        last_ds = self._fitted_df["ds"].max()
        horizon = int(h)
        future_ds = pd.date_range(last_ds, periods=horizon + 1, freq="D")[1:]
        rows = []
        for uid in df["unique_id"].unique():
            for ds in future_ds:
                rows.append({"unique_id": uid, "ds": ds, "y_hat": 0.0})
        return pd.DataFrame(rows)


@pytest.mark.nonfunctional
@pytest.mark.slow
def test_minimal_performance_smoke_with_stubbed_automodel(monkeypatch):
    """run_loto_experiment が小規模設定で一定時間内に完了することをスモーク確認。

    - 実際の NeuralForecast AutoModel は heavy なので、テストでは build_auto_model と
      build_neuralforecast をスタブして高速化している。
    - DB アクセスも避けるため、loto_repository.load_panel_by_loto をスタブして
      100 × 30 日程度の極小パネルを返す。
    """

    from nf_loto_platform.db import loto_repository  # import here for monkeypatch target

    H = 7  # 1 週間先までの予測
    unique_ids = [f"series_{i}" for i in range(10)]
    dates = pd.date_range("2024-01-01", periods=30, freq="D")
    records = []
    for uid in unique_ids:
        y = np.random.randn(len(dates))
        for ds, val in zip(dates, y):
            records.append({"unique_id": uid, "ds": ds, "y": float(val)})
    panel_df = pd.DataFrame.from_records(records)

    # --- DB リポジトリのスタブ ---
    def _fake_load_panel_by_loto(table_name: str, loto: str, unique_ids_param):
        # 引数がちゃんと渡っていることをざっくり確認
        assert table_name == "nf_loto_panel"
        assert set(unique_ids_param) == set(unique_ids)
        return panel_df

    monkeypatch.setattr(
        "nf_loto_platform.db.loto_repository.load_panel_by_loto",
        _fake_load_panel_by_loto,
    )

    # --- AutoModel / NeuralForecast のスタブ ---
    def _fake_build_auto_model(
        model_name: str,
        backend: str,
        h: int,
        loss_name: str,
        num_samples: int,
        search_space=None,
        early_stop=None,
        early_stop_patience_steps: int = 3,
        verbose: bool = True,
    ):
        # 引数がそれなりに渡っていることだけ確認して dummy を返す
        assert h == H
        assert num_samples == 1
        return _DummyAutoModel(h=h)

    def _fake_build_neuralforecast(model, freq: str, local_scaler_type: str | None):
        # 本来は NeuralForecast インスタンスを作るが、ここではそのまま model を返す
        return model

    monkeypatch.setattr(
        "nf_loto_platform.ml.automodel_builder.build_auto_model",
        _fake_build_auto_model,
    )
    monkeypatch.setattr(
        "nf_loto_platform.ml.automodel_builder.build_neuralforecast",
        _fake_build_neuralforecast,
    )

    # --- 実行 & 時間計測 ---
    start = time.perf_counter()
    preds, meta = run_loto_experiment(
        table_name="nf_loto_panel",
        loto="loto6",
        unique_ids=unique_ids,
        model_name="AutoNHITS",
        backend="local",
        horizon=H,
        loss="mae",
        metric="mae",
        num_samples=1,
        cpus=1,
        gpus=0,
        search_space=None,
        freq="D",
        local_scaler_type="robust",
        val_size=7,
        refit_with_val=False,
        use_init_models=False,
        early_stop=True,
        early_stop_patience_steps=1,
    )
    elapsed = time.perf_counter() - start

    # --- 簡易アサーション ---
    assert elapsed < 5.0, f"stubbed run_loto_experiment が遅すぎます: {elapsed:.3f} 秒"
    assert not preds.empty
    assert set(["unique_id", "ds", "y_hat"]).issubset(preds.columns)
    assert meta["loto"] == "loto6"
    assert meta["horizon"] == H
    assert meta["backend"] == "local"
