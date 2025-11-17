from __future__ import annotations

from dataclasses import asdict
from typing import Any, Dict, List, Sequence

from nf_loto_platform.ml import model_runner

from .domain import ExperimentOutcome, ExperimentRecipe, TimeSeriesTaskSpec


class ForecasterAgent:
    """run_loto_experiment / sweep_loto_experiments を呼び出す実験実行エージェント."""

    def run_single(
        self,
        task: TimeSeriesTaskSpec,
        recipe: ExperimentRecipe,
        table_name: str,
        loto: str,
        unique_ids: Sequence[str],
        model_name: str,
    ) -> ExperimentOutcome:
        """単一モデルで run_loto_experiment を実行するヘルパー."""
        preds, meta = model_runner.run_loto_experiment(
            table_name=table_name,
            loto=loto,
            unique_ids=unique_ids,
            model_name=model_name,
            backend=recipe.search_backend,
            horizon=task.target_horizon,
            loss=task.objective_metric,
            metric=task.objective_metric,
            num_samples=recipe.num_samples,
            cpus=1,
            gpus=0,
            search_space=recipe.extra_params.get("search_space"),
            freq=recipe.extra_params.get("freq", "D"),
            local_scaler_type=recipe.extra_params.get("local_scaler_type", "robust"),
            val_size=recipe.extra_params.get("val_size"),
            refit_with_val=bool(recipe.extra_params.get("refit_with_val", True)),
            use_init_models=bool(recipe.extra_params.get("use_init_models", False)),
            early_stop=recipe.extra_params.get("early_stop"),
            early_stop_patience_steps=int(recipe.extra_params.get("early_stop_patience_steps", 3)),
        )

        metrics = {task.objective_metric: meta.get(task.objective_metric)}
        all_model_metrics = {model_name: metrics}
        run_ids: List[str] = [str(meta.get("run_id"))]

        return ExperimentOutcome(
            best_model_name=model_name,
            metrics=metrics,
            all_model_metrics=all_model_metrics,
            run_ids=run_ids,
            meta={"single_run_meta": meta},
        )

    def run_sweep(
        self,
        task: TimeSeriesTaskSpec,
        recipe: ExperimentRecipe,
        table_name: str,
        loto: str,
        unique_ids: Sequence[str],
    ) -> ExperimentOutcome:
        """sweep_loto_experiments で複数モデルの実験をまとめて走らせる."""
        results = model_runner.sweep_loto_experiments(
            table_name=table_name,
            loto=loto,
            unique_ids=list(unique_ids),
            model_names=recipe.models,
            backends=[recipe.search_backend],
            param_spec=recipe.extra_params,
            mode="defaults",
            loss=task.objective_metric,
            metric=task.objective_metric,
            num_samples=recipe.num_samples,
            cpus=1,
            gpus=0,
        )

        all_model_metrics: Dict[str, Dict[str, float]] = {}
        run_ids: List[str] = []
        best_model = None
        best_metric = None

        for r in results:
            name = r.meta.get("model_name") or "unknown"
            metric_val = r.meta.get(task.objective_metric)
            if isinstance(metric_val, (int, float)):
                all_model_metrics.setdefault(name, {})[task.objective_metric] = float(metric_val)
                if best_metric is None or metric_val < best_metric:
                    best_metric = float(metric_val)
                    best_model = name
            run_ids.append(str(r.meta.get("run_id")))

        if best_model is None:
            # メトリクスが記録されていない場合はとりあえず先頭をベストとする
            best_model = recipe.models[0] if recipe.models else "unknown"
            best_metric = float("nan")  # type: ignore[assignment]

        metrics = {task.objective_metric: best_metric}

        return ExperimentOutcome(
            best_model_name=best_model,
            metrics=metrics,
            all_model_metrics=all_model_metrics,
            run_ids=run_ids,
            meta={"raw_results_len": len(results)},
        )
