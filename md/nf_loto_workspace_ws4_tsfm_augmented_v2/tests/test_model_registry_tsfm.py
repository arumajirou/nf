"""
model_registry.py TSFM統合版のユニットテスト。

テスト対象:
- TSFMモデルがレジストリに正しく登録されている
- AutoModelSpecのフィールドが正しく設定されている
- バリデーション機能が正しく動作する
- 既存のNeuralForecastモデルに影響がない（後方互換性）
"""

import pytest
from nf_loto_platform.ml.model_registry import (
    AUTO_MODEL_REGISTRY,
    get_model_spec,
    list_automodel_names,
    list_tsfm_models,
    list_neuralforecast_models,
    get_models_by_exogenous_support,
    validate_model_spec,
    AutoModelSpec,
    ExogenousSupport,
)


# ============================================================================
# レジストリ基本テスト
# ============================================================================

def test_tsfm_models_in_registry():
    """TSFMモデルがレジストリに登録されている."""
    expected_tsfm = {
        "Chronos2-ZeroShot",
        "TimeGPT-ZeroShot",
        "TempoPFN-ZeroShot",
    }
    all_models = set(list_automodel_names())
    assert expected_tsfm.issubset(all_models), \
        f"Expected TSFM models {expected_tsfm} not found in registry"


def test_neuralforecast_models_still_present():
    """既存のNeuralForecastモデルがレジストリに残っている."""
    expected_nf = {
        "AutoTFT",
        "AutoNHITS",
        "AutoNBEATS",
        "AutoMLP",
        "AutoLSTM",
        "AutoRNN",
        "AutoPatchTST",
        "AutoMLPMultivariate",
        "AutoTimeMixer",
    }
    all_models = set(list_automodel_names())
    assert expected_nf.issubset(all_models), \
        f"Expected NeuralForecast models {expected_nf} not found in registry"


def test_list_tsfm_models():
    """list_tsfm_models() がTSFMのみを返す."""
    tsfm_models = list_tsfm_models()
    assert len(tsfm_models) == 3
    assert "Chronos2-ZeroShot" in tsfm_models
    assert "TimeGPT-ZeroShot" in tsfm_models
    assert "TempoPFN-ZeroShot" in tsfm_models
    # NeuralForecastモデルが含まれていないことを確認
    assert "AutoTFT" not in tsfm_models


def test_list_neuralforecast_models():
    """list_neuralforecast_models() がNeuralForecastのみを返す."""
    nf_models = list_neuralforecast_models()
    assert len(nf_models) == 9
    assert "AutoTFT" in nf_models
    assert "AutoNHITS" in nf_models
    # TSFMモデルが含まれていないことを確認
    assert "Chronos2-ZeroShot" not in nf_models


# ============================================================================
# Chronos2 仕様テスト
# ============================================================================

def test_chronos2_spec_basic_fields():
    """Chronos2の基本フィールドが正しい."""
    spec = get_model_spec("Chronos2-ZeroShot")
    assert spec is not None
    assert spec.name == "Chronos2-ZeroShot"
    assert spec.family == "TSFM"
    assert spec.univariate is True
    assert spec.multivariate is True
    assert spec.forecast_type == "direct"


def test_chronos2_spec_tsfm_fields():
    """Chronos2のTSFM固有フィールドが正しい."""
    spec = get_model_spec("Chronos2-ZeroShot")
    assert spec.engine_kind == "tsfm"
    assert spec.engine_name == "chronos2"
    assert spec.is_zero_shot is True
    assert spec.requires_api_key is False
    assert spec.context_length == 512


def test_chronos2_spec_exogenous():
    """Chronos2の外生変数サポートが正しい."""
    spec = get_model_spec("Chronos2-ZeroShot")
    assert spec.exogenous.futr is False  # 未来既知変数: 非サポート
    assert spec.exogenous.hist is True   # 履歴変数: サポート
    assert spec.exogenous.stat is False  # 静的変数: 非サポート


# ============================================================================
# TimeGPT 仕様テスト
# ============================================================================

def test_timegpt_spec_basic_fields():
    """TimeGPTの基本フィールドが正しい."""
    spec = get_model_spec("TimeGPT-ZeroShot")
    assert spec is not None
    assert spec.name == "TimeGPT-ZeroShot"
    assert spec.family == "TSFM"
    assert spec.univariate is True
    assert spec.multivariate is True
    assert spec.forecast_type == "direct"


def test_timegpt_spec_tsfm_fields():
    """TimeGPTのTSFM固有フィールドが正しい."""
    spec = get_model_spec("TimeGPT-ZeroShot")
    assert spec.engine_kind == "tsfm"
    assert spec.engine_name == "timegpt"
    assert spec.is_zero_shot is True
    assert spec.requires_api_key is True  # ⭐ API キー必須
    assert spec.context_length is None    # API側で管理


def test_timegpt_spec_exogenous():
    """TimeGPTの外生変数サポートが正しい."""
    spec = get_model_spec("TimeGPT-ZeroShot")
    assert spec.exogenous.futr is True   # 未来既知変数: サポート
    assert spec.exogenous.hist is True   # 履歴変数: サポート
    assert spec.exogenous.stat is False  # 静的変数: 非サポート


# ============================================================================
# TempoPFN 仕様テスト
# ============================================================================

def test_tempopfn_spec_basic_fields():
    """TempoPFNの基本フィールドが正しい."""
    spec = get_model_spec("TempoPFN-ZeroShot")
    assert spec is not None
    assert spec.name == "TempoPFN-ZeroShot"
    assert spec.family == "TSFM"
    assert spec.univariate is True
    assert spec.multivariate is True
    assert spec.forecast_type == "direct"


def test_tempopfn_spec_tsfm_fields():
    """TempoPFNのTSFM固有フィールドが正しい."""
    spec = get_model_spec("TempoPFN-ZeroShot")
    assert spec.engine_kind == "tsfm"
    assert spec.engine_name == "tempopfn"
    assert spec.is_zero_shot is True
    assert spec.requires_api_key is False
    assert spec.context_length == 256


def test_tempopfn_spec_exogenous():
    """TempoPFNの外生変数サポートが正しい."""
    spec = get_model_spec("TempoPFN-ZeroShot")
    assert spec.exogenous.futr is False  # 未来既知変数: 非サポート
    assert spec.exogenous.hist is True   # 履歴変数: サポート
    assert spec.exogenous.stat is False  # 静的変数: 非サポート


# ============================================================================
# 後方互換性テスト
# ============================================================================

def test_backward_compatibility_autotft():
    """既存のAutoTFTが影響を受けていない."""
    spec = get_model_spec("AutoTFT")
    assert spec is not None
    # 基本フィールド
    assert spec.name == "AutoTFT"
    assert spec.family == "Transformer"
    # デフォルト値（TSFM統合前と同じ挙動）
    assert spec.engine_kind == "neuralforecast"
    assert spec.engine_name is None
    assert spec.is_zero_shot is False
    assert spec.requires_api_key is False
    assert spec.context_length is None


def test_backward_compatibility_autonhits():
    """既存のAutoNHITSが影響を受けていない."""
    spec = get_model_spec("AutoNHITS")
    assert spec is not None
    assert spec.engine_kind == "neuralforecast"
    assert spec.engine_name is None
    assert spec.is_zero_shot is False


# ============================================================================
# バリデーションテスト
# ============================================================================

def test_validate_tsfm_models_pass():
    """すべてのTSFMモデルがバリデーションをパスする."""
    for model_name in list_tsfm_models():
        spec = get_model_spec(model_name)
        # エラーが発生しないことを確認
        validate_model_spec(spec)


def test_validate_neuralforecast_models_pass():
    """すべてのNeuralForecastモデルがバリデーションをパスする."""
    for model_name in list_neuralforecast_models():
        spec = get_model_spec(model_name)
        # エラーが発生しないことを確認
        validate_model_spec(spec)


def test_validate_invalid_tsfm_missing_engine_name():
    """engine_kind='tsfm'でengine_name=Noneの場合はエラー."""
    invalid_spec = AutoModelSpec(
        name="InvalidTSFM",
        family="TSFM",
        univariate=True,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=False, hist=True, stat=False),
        engine_kind="tsfm",
        engine_name=None,  # ← これがエラー原因
    )
    
    with pytest.raises(ValueError, match="must specify engine_name"):
        validate_model_spec(invalid_spec)


def test_validate_invalid_tsfm_unknown_engine_name():
    """未知のengine_nameの場合はエラー."""
    invalid_spec = AutoModelSpec(
        name="InvalidTSFM",
        family="TSFM",
        univariate=True,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=False, hist=True, stat=False),
        engine_kind="tsfm",
        engine_name="unknown_engine",  # ← 未知のエンジン
    )
    
    with pytest.raises(ValueError, match="Unknown TSFM engine_name"):
        validate_model_spec(invalid_spec)


def test_validate_invalid_neuralforecast_has_engine_name():
    """engine_kind='neuralforecast'でengine_nameが設定されているとエラー."""
    invalid_spec = AutoModelSpec(
        name="InvalidNF",
        family="Transformer",
        univariate=True,
        multivariate=False,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=True, hist=True, stat=True),
        engine_kind="neuralforecast",
        engine_name="chronos2",  # ← これがエラー原因
    )
    
    with pytest.raises(ValueError, match="should not specify engine_name"):
        validate_model_spec(invalid_spec)


def test_validate_invalid_unknown_engine_kind():
    """未知のengine_kindの場合はエラー."""
    invalid_spec = AutoModelSpec(
        name="InvalidModel",
        family="Unknown",
        univariate=True,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=False, hist=True, stat=False),
        engine_kind="unknown_kind",  # ← 未知のengine_kind
    )
    
    with pytest.raises(ValueError, match="Unknown engine_kind"):
        validate_model_spec(invalid_spec)


# ============================================================================
# フィルタリング機能テスト
# ============================================================================

def test_get_models_by_exogenous_support_futr_required():
    """未来既知変数必須のモデルをフィルタリング."""
    models = get_models_by_exogenous_support(futr=True)
    assert "AutoTFT" in models
    assert "AutoNHITS" in models
    assert "TimeGPT-ZeroShot" in models  # TimeGPTはfutr=True
    assert "Chronos2-ZeroShot" not in models  # Chronos2はfutr=False


def test_get_models_by_exogenous_support_no_exogenous():
    """外生変数を一切使わないモデルをフィルタリング."""
    models = get_models_by_exogenous_support(futr=False, hist=False, stat=False)
    assert "AutoNBEATS" in models
    assert "AutoPatchTST" in models
    assert "AutoTimeMixer" in models
    # TSFM は hist=True なので含まれない
    assert "Chronos2-ZeroShot" not in models


def test_get_models_by_exogenous_support_hist_only():
    """履歴変数のみサポートするモデルをフィルタリング."""
    models = get_models_by_exogenous_support(futr=False, hist=True, stat=False)
    assert "Chronos2-ZeroShot" in models
    assert "TempoPFN-ZeroShot" in models
    # TimeGPTはfutr=Trueなので除外される
    assert "TimeGPT-ZeroShot" not in models


# ============================================================================
# エッジケーステスト
# ============================================================================

def test_get_model_spec_nonexistent():
    """存在しないモデル名の場合Noneを返す."""
    spec = get_model_spec("NonExistentModel")
    assert spec is None


def test_list_automodel_names_is_sorted():
    """list_automodel_names()の結果がソートされている."""
    names = list_automodel_names()
    assert names == sorted(names)


def test_list_tsfm_models_is_sorted():
    """list_tsfm_models()の結果がソートされている."""
    names = list_tsfm_models()
    assert names == sorted(names)


def test_list_neuralforecast_models_is_sorted():
    """list_neuralforecast_models()の結果がソートされている."""
    names = list_neuralforecast_models()
    assert names == sorted(names)


# ============================================================================
# レジストリ整合性テスト（モジュールロード時チェックの動作確認）
# ============================================================================

def test_registry_validation_at_module_load():
    """レジストリ全体のバリデーションが成功している（モジュールロード時）."""
    # このテストが実行できている時点で、
    # モジュールロード時のバリデーションが成功していることを意味する
    assert len(AUTO_MODEL_REGISTRY) > 0


# ============================================================================
# パラメトライズドテスト（すべてのTSFMモデルに対して同一のチェック）
# ============================================================================

@pytest.mark.parametrize("model_name", [
    "Chronos2-ZeroShot",
    "TimeGPT-ZeroShot",
    "TempoPFN-ZeroShot",
])
def test_tsfm_common_properties(model_name):
    """すべてのTSFMモデルが共通の性質を持つ."""
    spec = get_model_spec(model_name)
    assert spec is not None
    assert spec.family == "TSFM"
    assert spec.engine_kind == "tsfm"
    assert spec.is_zero_shot is True
    assert spec.forecast_type == "direct"
    # engine_nameはNoneでないこと
    assert spec.engine_name is not None
    assert spec.engine_name in {"chronos2", "timegpt", "tempopfn"}


@pytest.mark.parametrize("model_name", [
    "AutoTFT",
    "AutoNHITS",
    "AutoNBEATS",
    "AutoMLP",
    "AutoLSTM",
    "AutoRNN",
    "AutoPatchTST",
    "AutoMLPMultivariate",
    "AutoTimeMixer",
])
def test_neuralforecast_common_properties(model_name):
    """すべてのNeuralForecastモデルが共通の性質を持つ."""
    spec = get_model_spec(model_name)
    assert spec is not None
    assert spec.engine_kind == "neuralforecast"
    assert spec.engine_name is None
    assert spec.is_zero_shot is False
    assert spec.requires_api_key is False
    assert spec.context_length is None


# ============================================================================
# 実装品質テスト
# ============================================================================

def test_all_models_have_unique_names():
    """すべてのモデルが一意の名前を持つ."""
    names = list_automodel_names()
    assert len(names) == len(set(names)), "Duplicate model names found"


def test_all_specs_are_frozen():
    """すべてのAutoModelSpecがfrozen（不変）である."""
    for name, spec in AUTO_MODEL_REGISTRY.items():
        with pytest.raises(Exception):  # dataclass frozen の場合はattributeエラー
            spec.name = "Modified"


def test_registry_contains_expected_count():
    """レジストリに期待される数のモデルが登録されている."""
    all_models = list_automodel_names()
    # NeuralForecast: 9 + TSFM: 3 = 12
    assert len(all_models) == 12
