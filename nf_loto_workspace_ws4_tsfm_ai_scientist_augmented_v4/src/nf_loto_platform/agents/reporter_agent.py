from __future__ import annotations

from typing import Any, Mapping

from .domain import AgentReport, ExperimentOutcome, TimeSeriesTaskSpec
from .llm_client import BaseLLMClient


class ReporterAgent:
    """実験結果を人間向けレポートに変換するエージェント."""

    def __init__(self, llm_client: BaseLLMClient) -> None:
        self._llm = llm_client

    def summarize(self, task: TimeSeriesTaskSpec, outcome: ExperimentOutcome) -> AgentReport:
        """タスクと実験結果からレポートを生成する."""
        system_prompt = """あなたは時系列データ専任のシニアデータサイエンティストです。
        与えられたタスク設定とモデル比較結果をもとに、実務者向けの簡潔なレポートを書いてください。
        出力は Markdown とし、日本語で書いてください。
        """

        user_prompt = f"task={task}\n\noutcome={outcome}"

        markdown = self._llm.generate(system_prompt=system_prompt, user_prompt=user_prompt)

        summary = f"タスク {task.loto_kind} (h={task.target_horizon}) に対して、ベストモデルは {outcome.best_model_name} でした。"

        actions = [
            "推奨モデルを本番候補として詳細評価する",
            "劣っているモデルの特徴をレビューし、今後の実験計画に反映する",
        ]

        return AgentReport(
            summary=summary,
            details_markdown=markdown,
            recommended_actions=actions,
            artifacts={},
        )
