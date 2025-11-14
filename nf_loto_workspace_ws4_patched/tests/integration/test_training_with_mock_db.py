# NOTE: DB をモックして training パイプラインをテストする専用ファイル。
# - nf_loto_platform.db.loto_repository.load_panel_by_loto は
#   model_runner が import 済みのシンボル
#   nf_loto_platform.ml.model_runner.load_panel_by_loto を
#   monkeypatch で差し替える。
# - 本物の DB には接続しない設計とし、DB 契約テストは tests/db/ が担当する。

import numpy as np
import pandas as pd
import pytest

from nf_loto_platform.ml.model_runner import run_loto_experiment


class _DummyAutoModel:
    """training_with_mock_db 用の極小 AutoModel 実装。

    nonfunctional の性能テスト用 dummy とほぼ同じだが、ここでは
    「DB から取ってきたパネルを渡して予測 DataFrame を返す」という
    契約が守られていることを重視する。
    """

    def __init__(self, h: int) -> None:
        self._h = h
        self._fitted_df = None

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
                rows.append({"unique_id": uid, "ds": ds, "y_hat": 1.0})
        return pd.DataFrame(rows)


@pytest.mark.integration
def test_training_pipeline_with_mock_db_and_stubbed_automodel(monkeypatch):
    """DB リポジトリ + model_runner を結合した軽量統合テスト。

    - DB アクセスは loto_repository.load_panel_by_loto をスタブして差し替える
    - NeuralForecast AutoModel は automodel_builder の build_* を dummy に置換
    - run_loto_experiment が end-to-end で preds / meta を返すことを確認
    """

    H = 5
    unique_ids = ["mock_series"]

    dates = pd.date_range("2024-01-01", periods=20, freq="D")
    values = np.linspace(0.0, 1.0, num=len(dates))
    panel_df = pd.DataFrame(
        {
            "unique_id": unique_ids[0],
            "ds": dates,
            "y": values,
        }
    )

    # --- DB リポジトリのスタブ ---
    def _fake_load_panel_by_loto(table_name: str, loto: str, unique_ids_param):
        assert loto == "loto6"
        assert list(unique_ids_param) == unique_ids
        return panel_df

    monkeypatch.setattr(
        "nf_loto_platform.ml.model_runner.load_panel_by_loto",
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
        return _DummyAutoModel(h=h)

    def _fake_build_neuralforecast(model, freq: str, local_scaler_type: str | None):
        return model

    monkeypatch.setattr(
        "nf_loto_platform.ml.automodel_builder.build_auto_model",
        _fake_build_auto_model,
    )
    monkeypatch.setattr(
        "nf_loto_platform.ml.automodel_builder.build_neuralforecast",
        _fake_build_neuralforecast,
    )

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
        val_size=5,
        refit_with_val=False,
        use_init_models=False,
        early_stop=True,
        early_stop_patience_steps=1,
    )

    assert not preds.empty
    assert set(["unique_id", "ds", "y_hat"]).issubset(preds.columns)

    # meta にはコア情報が含まれていること
    for key in ["run_id", "table_name", "loto", "model_name", "backend", "horizon"]:
        assert key in meta
    assert meta["loto"] == "loto6"
    assert meta["backend"] == "local"
    assert meta["horizon"] == H


@pytest.mark.integration
def test_training_pipeline_with_mock_db_and_different_horizon(monkeypatch):
    """別パラメータ (horizon 3) でも end-to-end で動くことを確認する追加ケース。"""
    H = 3
    unique_ids = ["mock_series_2"]

    dates = pd.date_range("2024-02-01", periods=10, freq="D")
    values = np.linspace(100.0, 101.0, num=len(dates))
    panel_df = pd.DataFrame(
        {
            "unique_id": unique_ids[0],
            "ds": dates,
            "y": values,
        }
    )

    def _fake_load_panel_by_loto(table_name: str, loto: str, unique_ids_param):
        assert loto == "loto7"
        assert list(unique_ids_param) == unique_ids
        return panel_df

    monkeypatch.setattr(
        "nf_loto_platform.ml.model_runner.load_panel_by_loto",
        _fake_load_panel_by_loto,
    )

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
        return _DummyAutoModel(h=h)

    def _fake_build_neuralforecast(model, freq: str, local_scaler_type: str | None):
        return model

    monkeypatch.setattr(
        "nf_loto_platform.ml.automodel_builder.build_auto_model",
        _fake_build_auto_model,
    )
    monkeypatch.setattr(
        "nf_loto_platform.ml.automodel_builder.build_neuralforecast",
        _fake_build_neuralforecast,
    )

    preds, meta = run_loto_experiment(
        table_name="nf_loto_panel",
        loto="loto7",
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
        val_size=3,
        refit_with_val=False,
        use_init_models=False,
        early_stop=True,
        early_stop_patience_steps=1,
    )

    assert not preds.empty
    assert set(["unique_id", "ds", "y_hat"]).issubset(preds.columns)
    assert meta["loto"] == "loto7"
    assert meta["horizon"] == H
