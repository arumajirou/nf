from __future__ import annotations

from dataclasses import asdict
from typing import Any, Mapping

import pandas as pd

from .domain import CuratorOutput, TimeSeriesTaskSpec
from .llm_client import BaseLLMClient


class CuratorAgent:
    """ロト時系列のデータ診断と前処理プランを提案するエージェント."""

    def __init__(self, llm_client: BaseLLMClient) -> None:
        self._llm = llm_client

    def run(self, task: TimeSeriesTaskSpec, sample_df: pd.DataFrame) -> CuratorOutput:
        """サンプル DataFrame から統計サマリを作り、LLM に設定案を生成させる。"""
        if sample_df.empty:
            # 最低限のデフォルトにフォールバック
            return CuratorOutput(
                recommended_h=task.target_horizon,
                recommended_validation_scheme="holdout",
                candidate_feature_sets=["NO_EXOG"],
                data_profile={"empty": True},
                messages=["データが空だったためデフォルト設定を返しました"],
            )

        # 単純な統計サマリ
        profile: Mapping[str, Any] = {
            "rows": int(len(sample_df)),
            "unique_ids": int(sample_df["unique_id"].nunique()) if "unique_id" in sample_df.columns else None,
            "ds_min": str(sample_df["ds"].min()) if "ds" in sample_df.columns else None,
            "ds_max": str(sample_df["ds"].max()) if "ds" in sample_df.columns else None,
            "y_mean": float(sample_df["y"].mean()) if "y" in sample_df.columns else None,
            "y_std": float(sample_df["y"].std()) if "y" in sample_df.columns else None,
        }

        system_prompt = """あなたはロト時系列データ専任のデータサイエンティストです。
        与えられたデータプロファイルをもとに、予測ホライゾン/検証方法/特徴量セットの候補を提案してください。
        出力は JSON 形式にシリアライズされ、その後 Python 側でパースされます。
        """

        user_prompt = f"task_spec={task}\n\nprofile={profile}"

        # ここでは LLM の出力をそのまま使わず、安全なデフォルトを決め打ちしつつ
        # LLM 出力は説明メッセージとしてだけ利用する。
        llm_raw = self._llm.generate(system_prompt=system_prompt, user_prompt=user_prompt)

        # horizon/検証方式は単純に task から決める
        recommended_h = task.target_horizon
        validation = "rolling_cv" if profile.get("rows", 0) > 200 else "holdout"

        candidate_feature_sets = ["NO_EXOG", "FUTR_BASIC"]
        if profile.get("unique_ids", 1) > 1:
            candidate_feature_sets.append("HIST_GLOBAL")

        return CuratorOutput(
            recommended_h=recommended_h,
            recommended_validation_scheme=validation,
            candidate_feature_sets=candidate_feature_sets,
            data_profile=profile,
            messages=["LLM_hint", llm_raw],
        )
