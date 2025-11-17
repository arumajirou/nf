"""
model_registry.py TSFM統合版のユニットテスト（拡張版）.

目的:
- TSFMモデルが正しくレジストリ登録されていることを定量的に検証する
- AutoModelSpec / ExogenousSupport のフィールド設定を網羅的に確認する
- ヘルパー関数群 (list_*, get_model_spec, get_models_by_exogenous_support, validate_model_spec)
  の境界条件をテストする
"""

import pytest

from nf_loto_platform.ml.model_registry import (
    AUTO_MODEL_REGISTRY,
    AutoModelSpec,
    ExogenousSupport,
    get_model_spec,
    get_models_by_exogenous_support,
    list_automodel_names,
    list_neuralforecast_models,
    list_tsfm_models,
    validate_model_spec,
    _validate_registry_at_module_load,
)


TSFM_NAMES = {"Chronos2-ZeroShot", "TimeGPT-ZeroShot", "TempoPFN-ZeroShot"}


def test_registry_contains_expected_models():
    """NeuralForecast + TSFM を合わせたモデル名が期待どおりであることを確認する."""
    all_names = set(list_automodel_names())
    # AUTO_MODEL_REGISTRY のキーと完全一致しているはず
    assert all_names == set(AUTO_MODEL_REGISTRY.keys())

    # TSFM モデル 3 つが必ず含まれている
    assert TSFM_NAMES.issubset(all_names)


def test_list_tsfm_and_neuralforecast_are_disjoint_and_sorted():
    """TSFM/NeuralForecast のリストが互いに排他的かつソートされていることを確認する."""
    tsfm_list = list_tsfm_models()
    nf_list = list_neuralforecast_models()

    # 排他的
    assert set(tsfm_list).isdisjoint(set(nf_list))
    # TSFM 名は想定どおり
    assert set(tsfm_list) == TSFM_NAMES

    # ソート済みになっていること（辞書順）
    assert tsfm_list == sorted(tsfm_list)
    assert nf_list == sorted(nf_list)


def test_tsfm_specs_core_fields():
    """TSFM 各モデルの AutoModelSpec フィールドを詳細に検証する."""
    spec_chronos = get_model_spec("Chronos2-ZeroShot")
    spec_timegpt = get_model_spec("TimeGPT-ZeroShot")
    spec_tempopfn = get_model_spec("TempoPFN-ZeroShot")

    # すべて family=TSFM / engine_kind=tsfm / is_zero_shot=True であること
    for spec in (spec_chronos, spec_timegpt, spec_tempopfn):
        assert spec is not None
        assert spec.family == "TSFM"
        assert spec.engine_kind == "tsfm"
        assert spec.is_zero_shot is True

    # Chronos2
    assert spec_chronos.engine_name == "chronos2"
    assert spec_chronos.requires_api_key is False
    assert spec_chronos.context_length == 512
    assert spec_chronos.exogenous.futr is False
    assert spec_chronos.exogenous.hist is True
    assert spec_chronos.exogenous.stat is False

    # TimeGPT
    assert spec_timegpt.engine_name == "timegpt"
    assert spec_timegpt.requires_api_key is True
    assert spec_timegpt.context_length is None
    assert spec_timegpt.exogenous.futr is True
    assert spec_timegpt.exogenous.hist is True
    assert spec_timegpt.exogenous.stat is False

    # TempoPFN
    assert spec_tempopfn.engine_name == "tempopfn"
    assert spec_tempopfn.requires_api_key is False
    assert spec_tempopfn.context_length == 256
    assert spec_tempopfn.exogenous.futr is False
    assert spec_tempopfn.exogenous.hist is True
    assert spec_tempopfn.exogenous.stat is False


def test_get_models_by_exogenous_support_future_known():
    """未来既知変数 (futr=True, hist=True, stat=True) をサポートするモデルのみを取得する."""
    models = set(get_models_by_exogenous_support(futr=True, hist=True, stat=True))

    # AutoTFT / AutoNHITS / AutoMLP / AutoLSTM / AutoRNN / AutoMLPMultivariate が対象
    expected = {
        "AutoTFT",
        "AutoNHITS",
        "AutoMLP",
        "AutoLSTM",
        "AutoRNN",
        "AutoMLPMultivariate",
    }
    assert models == expected


def test_get_models_by_exogenous_support_no_exogenous():
    """外生変数を一切使わないモデル (F/H/S すべて False) を取得する."""
    models = set(get_models_by_exogenous_support(futr=False, hist=False, stat=False))
    expected = {"AutoNBEATS", "AutoPatchTST", "AutoTimeMixer"}
    assert models == expected


def test_get_models_by_exogenous_support_hist_only_tsfm():
    """TSFMのうち hist のみを使うモデルをフィルタリングできることを確認する."""
    models = set(get_models_by_exogenous_support(futr=False, hist=True, stat=False))
    # Chronos2 / TempoPFN は hist=True, futr=False, stat=False
    expected = {"Chronos2-ZeroShot", "TempoPFN-ZeroShot", "AutoNBEATS", "AutoPatchTST", "AutoTimeMixer"}
    # 上記のうち hist=True,futr=False,stat=False の組合せのみを再フィルタ
    filtered = {
        name
        for name in expected
        if AUTO_MODEL_REGISTRY[name].exogenous.futr is False
        and AUTO_MODEL_REGISTRY[name].exogenous.hist is True
        and AUTO_MODEL_REGISTRY[name].exogenous.stat is False
    }
    # get_models_by_exogenous_support の結果も同じになるはず
    assert models == filtered
    # TSFM モデル 2 つが含まれていることも明示的に確認
    assert {"Chronos2-ZeroShot", "TempoPFN-ZeroShot"}.issubset(models)


def test_validate_model_spec_rejects_invalid_tsfm_missing_engine_name():
    """TSFM なのに engine_name が指定されていない場合は ValueError.【回帰防止】"""
    bad_spec = AutoModelSpec(
        name="BrokenTSFM",
        family="TSFM",
        univariate=True,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=False, hist=True, stat=False),
        engine_kind="tsfm",
        engine_name=None,
        is_zero_shot=True,
        requires_api_key=False,
        context_length=128,
    )
    with pytest.raises(ValueError) as excinfo:
        validate_model_spec(bad_spec)
    msg = str(excinfo.value)
    assert "must specify engine_name" in msg


def test_validate_model_spec_rejects_invalid_engine_name():
    """存在しない engine_name の場合も ValueError になる."""
    bad_spec = AutoModelSpec(
        name="BrokenTSFM2",
        family="TSFM",
        univariate=True,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=False, hist=True, stat=False),
        engine_kind="tsfm",
        engine_name="unknown_engine",
        is_zero_shot=True,
        requires_api_key=False,
        context_length=128,
    )
    with pytest.raises(ValueError) as excinfo:
        validate_model_spec(bad_spec)
    msg = str(excinfo.value)
    assert "Invalid engine_name for TSFM model" in msg


def test_validate_model_spec_rejects_invalid_engine_kind():
    """engine_kind が未知の値の場合もエラーになる."""
    bad_spec = AutoModelSpec(
        name="BrokenEngineKind",
        family="TSFM",
        univariate=True,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=False, hist=True, stat=False),
        engine_kind="unknown_kind",
        engine_name="chronos2",
        is_zero_shot=True,
        requires_api_key=False,
        context_length=128,
    )
    with pytest.raises(ValueError) as excinfo:
        validate_model_spec(bad_spec)
    msg = str(excinfo.value)
    assert "Unknown engine_kind" in msg


def test_validate_registry_at_module_load_is_idempotent():
    """_validate_registry_at_module_load は何度呼んでも成功する（副作用なし）."""
    # 例外が出なければ OK
    _validate_registry_at_module_load()


def test_get_model_spec_returns_none_for_unknown_model():
    """存在しないモデル名に対しては None を返す."""
    assert get_model_spec("non_existing_model") is None
