"""
NeuralForecast AutoModel のレジストリ（TSFM統合版）。
モデルごとの外生変数サポート (F/H/S) をここで定義しておき、
UI からの選択や自動検証で利用できるようにする。

TSFM統合により以下を拡張:
- AutoModelSpec に engine_kind, engine_name, is_zero_shot 等のフィールド追加
- Chronos2-ZeroShot, TimeGPT-ZeroShot, TempoPFN-ZeroShot エントリ追加
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass(frozen=True)
class ExogenousSupport:
    """外生変数サポート定義."""
    futr: bool  # F: futr_exog_list（未来既知変数）
    hist: bool  # H: hist_exog_list（履歴変数）
    stat: bool  # S: stat_exog_list（静的変数）


@dataclass(frozen=True)
class AutoModelSpec:
    """AutoModel / TSFM の統一仕様定義.
    
    TSFM統合により以下のフィールドを追加:
    - engine_kind: モデル実行エンジンの種類
    - engine_name: 具体的なTSFM名
    - is_zero_shot: ゼロショット予測モデルか
    - requires_api_key: API キーが必要か
    - context_length: コンテキスト長（TSFM用）
    """
    name: str                # "AutoTFT" / "Chronos2-ZeroShot" など
    family: str              # "Transformer" / "MLP" / "TSFM" など
    univariate: bool         # 単変量予測対応
    multivariate: bool       # 多変量予測対応
    forecast_type: str       # "direct" / "recursive" / "both"
    exogenous: ExogenousSupport
    
    # ⭐ TSFM統合による新規フィールド（デフォルト値で既存コードとの互換性を保つ）
    engine_kind: str = "neuralforecast"  # "neuralforecast" | "tsfm"
    engine_name: Optional[str] = None    # "chronos2" | "timegpt" | "tempopfn"
    is_zero_shot: bool = False           # ゼロショット予測モデルか
    requires_api_key: bool = False       # API キーが必要か（TimeGPT等）
    context_length: Optional[int] = None # コンテキスト長（TSFMで使用）


# ============================================================================
# AutoModel レジストリ
# ============================================================================

AUTO_MODEL_REGISTRY: Dict[str, AutoModelSpec] = {
    # ========================================================================
    # NeuralForecast AutoModels（既存）
    # ========================================================================
    
    "AutoTFT": AutoModelSpec(
        name="AutoTFT",
        family="Transformer",
        univariate=True,
        multivariate=False,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=True, hist=True, stat=True),
    ),
    
    "AutoNHITS": AutoModelSpec(
        name="AutoNHITS",
        family="MLP",
        univariate=True,
        multivariate=False,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=True, hist=True, stat=True),
    ),
    
    "AutoNBEATS": AutoModelSpec(
        name="AutoNBEATS",
        family="MLP",
        univariate=True,
        multivariate=False,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=False, hist=False, stat=False),
    ),
    
    "AutoMLP": AutoModelSpec(
        name="AutoMLP",
        family="MLP",
        univariate=True,
        multivariate=False,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=True, hist=True, stat=True),
    ),
    
    "AutoLSTM": AutoModelSpec(
        name="AutoLSTM",
        family="RNN",
        univariate=True,
        multivariate=False,
        forecast_type="both",
        exogenous=ExogenousSupport(futr=True, hist=True, stat=True),
    ),
    
    "AutoRNN": AutoModelSpec(
        name="AutoRNN",
        family="RNN",
        univariate=True,
        multivariate=False,
        forecast_type="both",
        exogenous=ExogenousSupport(futr=True, hist=True, stat=True),
    ),
    
    "AutoPatchTST": AutoModelSpec(
        name="AutoPatchTST",
        family="Transformer",
        univariate=True,
        multivariate=False,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=False, hist=False, stat=False),
    ),
    
    "AutoMLPMultivariate": AutoModelSpec(
        name="AutoMLPMultivariate",
        family="MLP",
        univariate=False,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=True, hist=True, stat=True),
    ),
    
    "AutoTimeMixer": AutoModelSpec(
        name="AutoTimeMixer",
        family="MLP",
        univariate=False,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(futr=False, hist=False, stat=False),
    ),
    
    # ========================================================================
    # TSFM Models（新規追加）
    # ========================================================================
    
    "Chronos2-ZeroShot": AutoModelSpec(
        name="Chronos2-ZeroShot",
        family="TSFM",
        univariate=True,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(
            futr=False,  # Chronos2は基本的に外生変数サポートなし
            hist=True,   # 履歴データは使用
            stat=False,
        ),
        engine_kind="tsfm",
        engine_name="chronos2",
        is_zero_shot=True,
        requires_api_key=False,
        context_length=512,  # Chronos2のデフォルトコンテキスト長
    ),
    
    "TimeGPT-ZeroShot": AutoModelSpec(
        name="TimeGPT-ZeroShot",
        family="TSFM",
        univariate=True,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(
            futr=True,   # TimeGPTは外生変数サポート
            hist=True,
            stat=False,
        ),
        engine_kind="tsfm",
        engine_name="timegpt",
        is_zero_shot=True,
        requires_api_key=True,  # ⭐ API キー必須
        context_length=None,    # API側で自動管理
    ),
    
    "TempoPFN-ZeroShot": AutoModelSpec(
        name="TempoPFN-ZeroShot",
        family="TSFM",
        univariate=True,
        multivariate=True,
        forecast_type="direct",
        exogenous=ExogenousSupport(
            futr=False,
            hist=True,
            stat=False,
        ),
        engine_kind="tsfm",
        engine_name="tempopfn",
        is_zero_shot=True,
        requires_api_key=False,
        context_length=256,  # TempoPFNのデフォルトコンテキスト長
    ),
}


# ============================================================================
# ヘルパー関数
# ============================================================================

def list_automodel_names() -> List[str]:
    """UI 用のモデル名一覧を返す（ソート済み）.
    
    TSFM統合後も既存のコードとの互換性を保つため、
    この関数は既存どおりレジストリのキーをソートして返す。
    
    Returns:
        モデル名のリスト（例: ["AutoTFT", "Chronos2-ZeroShot", ...]）
    """
    return sorted(AUTO_MODEL_REGISTRY.keys())


def get_model_spec(model_name: str) -> Optional[AutoModelSpec]:
    """指定されたモデル名のAutoModelSpecを取得する.
    
    Args:
        model_name: モデル名（例: "AutoTFT", "Chronos2-ZeroShot"）
    
    Returns:
        AutoModelSpecインスタンス、存在しない場合はNone
    """
    return AUTO_MODEL_REGISTRY.get(model_name)


def validate_model_spec(spec: AutoModelSpec) -> None:
    """AutoModelSpecの整合性を検証する.
    
    Args:
        spec: 検証対象のAutoModelSpec
    
    Raises:
        ValueError: 不正な組み合わせが検出された場合
    
    Examples:
        >>> spec = get_model_spec("Chronos2-ZeroShot")
        >>> validate_model_spec(spec)  # エラーなし
        
        >>> bad_spec = AutoModelSpec(
        ...     name="BadModel",
        ...     family="TSFM",
        ...     engine_kind="tsfm",
        ...     engine_name=None,  # ← エラー
        ...     # ... その他のフィールド ...
        ... )
        >>> validate_model_spec(bad_spec)  # ValueError発生
    """
    if spec.engine_kind == "tsfm":
        # TSFM の場合、engine_name は必須
        if spec.engine_name is None:
            raise ValueError(
                f"TSFM model '{spec.name}' must specify engine_name. "
                f"Valid values: chronos2, timegpt, tempopfn"
            )
        
        # engine_name の値チェック
        valid_engines = {"chronos2", "timegpt", "tempopfn"}
        if spec.engine_name not in valid_engines:
            # テストでは "Invalid engine_name for TSFM model" という文言をチェックしている。
            # 既存の詳細情報も維持しつつ、プレフィックスとしてこのフレーズを含める。
            raise ValueError(
                "Invalid engine_name for TSFM model: "
                f"Unknown TSFM engine_name: '{spec.engine_name}' for model '{spec.name}'. "
                f"Valid values: {valid_engines}"
            )
        
        # API キー要求の整合性チェック
        if spec.requires_api_key and spec.engine_name not in {"timegpt"}:
            raise ValueError(
                f"Model '{spec.name}' requires API key, but engine '{spec.engine_name}' "
                f"does not support API keys. Only 'timegpt' requires API keys."
            )
    
    elif spec.engine_kind == "neuralforecast":
        # NeuralForecas�� の場合、engine_name は None であるべき
        if spec.engine_name is not None:
            raise ValueError(
                f"NeuralForecast model '{spec.name}' should not specify engine_name. "
                f"Got: {spec.engine_name}"
            )
    
    else:
        raise ValueError(
            f"Unknown engine_kind: '{spec.engine_kind}' for model '{spec.name}'. "
            f"Valid values: neuralforecast, tsfm"
        )


def list_tsfm_models() -> List[str]:
    """TSFMモデルのみのリストを返す（ソート済み）.
    
    Returns:
        TSFMモデル名のリスト（例: ["Chronos2-ZeroShot", "TimeGPT-ZeroShot", ...]）
    """
    return sorted([
        name for name, spec in AUTO_MODEL_REGISTRY.items()
        if spec.engine_kind == "tsfm"
    ])


def list_neuralforecast_models() -> List[str]:
    """NeuralForecast AutoModelのみのリストを返す（ソート済み）.
    
    Returns:
        NeuralForecastモデル名のリスト（例: ["AutoTFT", "AutoNHITS", ...]）
    """
    return sorted([
        name for name, spec in AUTO_MODEL_REGISTRY.items()
        if spec.engine_kind == "neuralforecast"
    ])


def get_models_by_exogenous_support(
    futr: Optional[bool] = None,
    hist: Optional[bool] = None,
    stat: Optional[bool] = None,
) -> List[str]:
    """外生変数サポート条件でモデルをフィルタリング.
    
    Args:
        futr: 未来既知変数のサポート（True: 必要, False: 不要, None: 問わない）
        hist: 履歴変数のサポート（True: 必要, False: 不要, None: 問わない）
        stat: 静的変数のサポート（True: 必要, False: 不要, None: 問わない）
    
    Returns:
        条件に合致するモデル名のリスト
    
    Examples:
        >>> # 未来既知変数をサポートするモデルのみ
        >>> models = get_models_by_exogenous_support(futr=True)
        
        >>> # 外生変数を一切使わないモデルのみ
        >>> models = get_models_by_exogenous_support(futr=False, hist=False, stat=False)
    """
    results = []
    
    for name, spec in AUTO_MODEL_REGISTRY.items():
        if futr is not None and spec.exogenous.futr != futr:
            continue
        if hist is not None and spec.exogenous.hist != hist:
            continue
        if stat is not None and spec.exogenous.stat != stat:
            continue
        results.append(name)
    
    return sorted(results)


# ============================================================================
# レジストリ整合性チェック（モジュールロード時に実行）
# ============================================================================

def _validate_registry_at_module_load() -> None:
    """モジュールロード時にレジストリ全体の整合性をチェック.
    
    不正なエントリがあればValueErrorを発生させる。
    """
    for name, spec in AUTO_MODEL_REGISTRY.items():
        try:
            validate_model_spec(spec)
        except ValueError as e:
            raise ValueError(
                f"Invalid registry entry for model '{name}': {e}"
            ) from e


# モジュールロード時にバリデーション実行
_validate_registry_at_module_load()
