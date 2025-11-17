from __future__ import annotations

from typing import Dict, Iterable, List, Mapping

from nf_loto_platform.ml.model_registry import AUTO_MODEL_REGISTRY

from .domain import CuratorOutput, ExperimentRecipe, TimeSeriesTaskSpec


class PlannerAgent:
    """モデル/特徴量の組合せから実験レシピを構築するエージェント."""

    def __init__(self, registry: Mapping[str, object] | None = None) -> None:
        # AUTO_MODEL_REGISTRY は {name: AutoModelSpec}
        self._registry = registry or AUTO_MODEL_REGISTRY

    def _select_models(self, task: TimeSeriesTaskSpec) -> List[str]:
        names: List[str] = []
        for name, spec in self._registry.items():  # type: ignore[assignment]
            family = getattr(spec, "family", "")
            engine_kind = getattr(spec, "engine_kind", "")  # tsfm / neuralforecast / classical
            # ライブラリ依存の強いモデルはここでは見ない (registry 側で制御)
            if not getattr(spec, "enabled", True):
                continue

            if engine_kind == "tsfm" and task.allow_tsfm:
                names.append(name)
            elif engine_kind == "neuralforecast" and task.allow_neuralforecast:
                names.append(name)
            elif engine_kind == "classical" and task.allow_classical:
                names.append(name)

        # シンプルに名前順でソートして返す
        return sorted(names)

    def plan(self, task: TimeSeriesTaskSpec, curator: CuratorOutput) -> ExperimentRecipe:
        """CuratorOutput を踏まえて実験レシピを組み立てる."""
        models = self._select_models(task)

        backend = "local"
        if task.max_training_time_minutes and task.max_training_time_minutes > 60:
            # 時間が潤沢なら Optuna / Ray などの分散バックエンドを許可
            backend = "optuna"

        extra: Dict[str, object] = {
            "target_horizon": task.target_horizon,
            "validation_scheme": curator.recommended_validation_scheme,
        }

        return ExperimentRecipe(
            models=models,
            feature_sets=curator.candidate_feature_sets,
            search_backend=backend,
            num_samples=1,
            time_budget_hours=(task.max_training_time_minutes / 60.0 if task.max_training_time_minutes else None),
            use_tsfm=task.allow_tsfm,
            use_neuralforecast=task.allow_neuralforecast,
            use_classical=task.allow_classical,
            extra_params=extra,
        )
