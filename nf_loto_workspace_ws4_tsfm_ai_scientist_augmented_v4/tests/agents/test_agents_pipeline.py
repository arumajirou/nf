"""AI データサイエンティスト層 (agents パッケージ) の軽量テスト.

- TimeSeriesTaskSpec / CuratorOutput / ExperimentRecipe / ExperimentOutcome / AgentReport の整合性
- CuratorAgent -> PlannerAgent -> ForecasterAgent -> ReporterAgent の最小フロー
- AgentOrchestrator.run_full_cycle が例外なく完走すること
"""

from __future__ import annotations

from dataclasses import asdict

import pandas as pd
import pytest

pytest.importorskip("neuralforecast")

from nf_loto_platform.agents import (
    AgentOrchestrator,
    CuratorAgent,
    EchoLLMClient,
    ForecasterAgent,
    PlannerAgent,
    ReporterAgent,
    TimeSeriesTaskSpec,
)


@pytest.fixture
def simple_panel_df() -> pd.DataFrame:
    data = []
    for uid in ["s1", "s2"]:
        for i in range(10):
            data.append({"unique_id": uid, "ds": f"2024-01-{i+1:02d}", "y": float(i)})
    return pd.DataFrame.from_records(data)


def test_curator_agent_produces_reasonable_output(simple_panel_df: pd.DataFrame) -> None:
    task = TimeSeriesTaskSpec(loto_kind="loto6", target_horizon=4)
    curator = CuratorAgent(EchoLLMClient())
    out = curator.run(task, simple_panel_df)

    assert out.recommended_h == task.target_horizon
    assert out.recommended_validation_scheme in {"holdout", "rolling_cv"}
    assert out.candidate_feature_sets  # 非空
    assert out.data_profile["rows"] == len(simple_panel_df)


def test_planner_agent_uses_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    # レジストリを最小限のダミーで差し替え
    class DummySpec:
        def __init__(self, name: str, engine_kind: str, enabled: bool = True) -> None:
            self.name = name
            self.engine_kind = engine_kind
            self.enabled = enabled
            self.family = "TSFM"
            self.univariate = True
            self.multivariate = True
            self.forecast_type = "direct"
            self.exogenous = None

    dummy_registry = {
        "Chronos2-ZeroShot": DummySpec("Chronos2-ZeroShot", "tsfm"),
        "AutoNHITS": DummySpec("AutoNHITS", "neuralforecast"),
        "ClassicalARIMA": DummySpec("ClassicalARIMA", "classical"),
    }

    from nf_loto_platform import agents as agents_pkg

    planner = agents_pkg.PlannerAgent(registry=dummy_registry)
    task = TimeSeriesTaskSpec(loto_kind="loto6", target_horizon=4, allow_classical=False)
    curator_out = agents_pkg.CuratorOutput(
        recommended_h=4,
        recommended_validation_scheme="holdout",
        candidate_feature_sets=["NO_EXOG"],
        data_profile={},
        messages=[],
    )

    recipe = planner.plan(task, curator_out)
    # TSFM + NeuralForecast が選ばれ、classical は除外されるはず
    assert set(recipe.models) == {"Chronos2-ZeroShot", "AutoNHITS"}


def test_agent_orchestrator_full_cycle(monkeypatch: pytest.MonkeyPatch, simple_panel_df: pd.DataFrame) -> None:
    """DB・モデルランナーをスタブしてフルサイクルが完走することだけ検証する."""
    # DB スタブ
    def _fake_load_panel_by_loto(table_name: str, loto: str, unique_ids):
        return simple_panel_df

    monkeypatch.setattr(
        "nf_loto_platform.db.loto_repository.load_panel_by_loto",
        _fake_load_panel_by_loto,
    )

    # model_runner.sweep_loto_experiments をスタブ
    class DummyResult:
        def __init__(self, model_name: str, run_id: int, metric: float) -> None:
            self.meta = {"model_name": model_name, "run_id": run_id, "mae": metric}
            self.preds = None

    def _fake_sweep(*args, **kwargs):
        return [
            DummyResult("Chronos2-ZeroShot", 1, 0.5),
            DummyResult("AutoNHITS", 2, 0.8),
        ]

    monkeypatch.setattr(
        "nf_loto_platform.ml.model_runner.sweep_loto_experiments",
        _fake_sweep,
    )

    curator = CuratorAgent(EchoLLMClient())
    planner = PlannerAgent(
        registry={
            "Chronos2-ZeroShot": type("S", (), {"engine_kind": "tsfm", "family": "TSFM", "univariate": True, "multivariate": True, "forecast_type": "direct", "exogenous": None, "enabled": True})(),
            "AutoNHITS": type("S", (), {"engine_kind": "neuralforecast", "family": "MLP", "univariate": True, "multivariate": False, "forecast_type": "direct", "exogenous": None, "enabled": True})(),
        }
    )
    forecaster = ForecasterAgent()
    reporter = ReporterAgent(EchoLLMClient())

    orchestrator = AgentOrchestrator(
        curator=curator,
        planner=planner,
        forecaster=forecaster,
        reporter=reporter,
    )

    task = TimeSeriesTaskSpec(loto_kind="loto6", target_horizon=4)
    outcome, report = orchestrator.run_full_cycle(
        task=task,
        table_name="nf_loto_panel",
        loto="loto6",
        unique_ids=["s1", "s2"],
    )

    assert outcome.best_model_name == "Chronos2-ZeroShot"
    assert "loto6" in report.summary
    assert report.details_markdown  # EchoLLMClient 由来の文字列
