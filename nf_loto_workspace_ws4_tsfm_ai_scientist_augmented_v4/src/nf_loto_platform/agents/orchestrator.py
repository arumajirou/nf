from __future__ import annotations

from typing import Sequence

import pandas as pd

from nf_loto_platform.db.loto_repository import load_panel_by_loto

from .curator_agent import CuratorAgent
from .domain import AgentReport, ExperimentOutcome, ExperimentRecipe, TimeSeriesTaskSpec
from .forecaster_agent import ForecasterAgent
from .planner_agent import PlannerAgent
from .reporter_agent import ReporterAgent


class AgentOrchestrator:
    """Curator -> Planner -> Forecaster -> Reporter を束ねるオーケストレータ."""

    def __init__(
        self,
        curator: CuratorAgent,
        planner: PlannerAgent,
        forecaster: ForecasterAgent,
        reporter: ReporterAgent,
    ) -> None:
        self._curator = curator
        self._planner = planner
        self._forecaster = forecaster
        self._reporter = reporter

    def load_sample(self, table_name: str, loto: str, unique_ids: Sequence[str]) -> pd.DataFrame:
        """DB からサンプルデータを取得するヘルパー.

        実装は loto_repository のラッパーにとどめ、テストでは monkeypatch しやすいようにする。
        """
        panel_df = load_panel_by_loto(table_name=table_name, loto=loto, unique_ids=unique_ids)
        return panel_df

    def run_full_cycle(
        self,
        task: TimeSeriesTaskSpec,
        table_name: str,
        loto: str,
        unique_ids: Sequence[str],
    ) -> tuple[ExperimentOutcome, AgentReport]:
        """AI データサイエンティストのフルサイクルを実行する。"""
        panel_df = self.load_sample(table_name=table_name, loto=loto, unique_ids=unique_ids)
        curator_out = self._curator.run(task, panel_df)

        recipe = self._planner.plan(task, curator_out)

        outcome = self._forecaster.run_sweep(
            task=task,
            recipe=recipe,
            table_name=table_name,
            loto=loto,
            unique_ids=unique_ids,
        )

        report = self._reporter.summarize(task, outcome)

        return outcome, report
