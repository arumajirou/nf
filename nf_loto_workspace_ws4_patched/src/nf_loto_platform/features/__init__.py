"""特徴量生成モジュール.

本番ではより多くの特徴量をここに集約していく想定だが、
テストしやすい最小機能としてラグ特徴量付与のユーティリティを提供する。
"""

from __future__ import annotations

from typing import Hashable

import pandas as pd


def add_lag_feature(
    panel: pd.DataFrame,
    group_col: Hashable = "unique_id",
    time_col: Hashable = "ds",
    target_col: Hashable = "y",
    lag: int = 1,
    new_col: Hashable | None = None,
) -> pd.DataFrame:
    """パネルデータに単純なラグ特徴量を追加する。

    Parameters
    ----------
    panel:
        列 `group_col`, `time_col`, `target_col` を含む DataFrame。
    group_col, time_col, target_col:
        グルーピング・時系列・目的変数の列名。
    lag:
        何ステップ前を参照するか。
    new_col:
        生成する列名。None の場合は ``f"{target_col}_lag{lag}"`` を用いる。

    Returns
    -------
    pd.DataFrame
        入力と同じ列に加えてラグ列を 1 本追加した DataFrame。
        元の DataFrame は破壊的変更しない。
    """
    if new_col is None:
        new_col = f"{target_col}_lag{lag}"

    df = panel.copy()
    df = df.sort_values([group_col, time_col])
    df[new_col] = df.groupby(group_col)[target_col].shift(lag)
    return df


__all__ = ["add_lag_feature"]
