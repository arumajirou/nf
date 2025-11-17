from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Mapping, Optional, Sequence


@dataclass
class TimeSeriesTaskSpec:
    """時系列タスクの高レベル仕様.

    エージェント層が、人間の要求や UI 入力を正規化したもの。
    ここではロト用に最低限必要なものだけを持たせている。
    """

    loto_kind: str  # "loto6" / "loto7" / "miniloto" など
    target_horizon: int  # 先何ステップ (週) まで予測したいか
    frequency: str = "W"  # pandas オフセットエイリアス
    objective_metric: str = "mae"
    allow_tsfm: bool = True
    allow_neuralforecast: bool = True
    allow_classical: bool = False
    max_training_time_minutes: Optional[float] = None
    mode: str = "auto"  # "auto" / "suggestion_only" など
    notes: str = ""


@dataclass
class CuratorOutput:
    """CuratorAgent が出力するデータ診断・前処理プラン."""

    recommended_h: int
    recommended_validation_scheme: str
    candidate_feature_sets: List[str]
    data_profile: Mapping[str, Any] = field(default_factory=dict)
    messages: List[str] = field(default_factory=list)


@dataclass
class ExperimentRecipe:
    """PlannerAgent が組み立てる実験レシピ.

    ForecasterAgent から見れば、この情報だけで
    sweep_loto_experiments を呼び出せる。
    """

    models: List[str]
    feature_sets: List[str]
    search_backend: str = "local"  # "local" / "optuna" / "ray"
    num_samples: int = 1
    time_budget_hours: Optional[float] = None
    use_tsfm: bool = True
    use_neuralforecast: bool = True
    use_classical: bool = False
    extra_params: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ExperimentOutcome:
    """ForecasterAgent が返す実験結果の要約."""

    best_model_name: str
    metrics: Mapping[str, float]
    all_model_metrics: Mapping[str, Mapping[str, float]]
    run_ids: Sequence[str]
    meta: Mapping[str, Any] = field(default_factory=dict)


@dataclass
class AgentReport:
    """ReporterAgent が生成したレポート."""

    summary: str
    details_markdown: str
    recommended_actions: List[str] = field(default_factory=list)
    artifacts: Dict[str, str] = field(default_factory=dict)
