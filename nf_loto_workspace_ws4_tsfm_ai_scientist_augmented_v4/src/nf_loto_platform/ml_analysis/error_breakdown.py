"""
予測誤差のスライス別・時間別の内訳を計算するユーティリティ群。

- build_error_breakdown: セグメント単位 (例: loto, unique_id) で誤差指標を集計
- build_time_series_metrics: 時系列単位 (例: 月次) で誤差指標を集計

将来的には特徴量分布や外生変数の統計もここで扱う。
"""
from __future__ import annotations

from typing import Iterable, Sequence

import pandas as pd

from .metrics import mae, rmse, smape


def build_error_breakdown(
    df: pd.DataFrame,
    group_keys: Sequence[str] = ("loto", "unique_id"),
    y_col: str = "y",
    yhat_col: str = "y_hat",
) -> pd.DataFrame:
    """group_keys ごとに誤差指標を集計した DataFrame を返す。

    Args:
        df: 予測結果を含む DataFrame（少なくとも y_col, yhat_col を含む）
        group_keys: 集計キーとなるカラム名
        y_col: 実測値カラム名
        yhat_col: 予測値カラム名

    Returns:
        group_keys + ["mae", "rmse", "smape"] を持つ DataFrame。
    """
    required = set(group_keys) | {y_col, yhat_col}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"必要なカラムが不足しています: {missing}")

    def _agg(group: pd.DataFrame) -> pd.Series:
        y = group[y_col].to_numpy()
        yhat = group[yhat_col].to_numpy()
        return pd.Series(
            {
                "mae": mae(y, yhat),
                "rmse": rmse(y, yhat),
                "smape": smape(y, yhat),
            }
        )

    grouped = df.groupby(list(group_keys), dropna=False, sort=False)
    out = grouped.apply(_agg).reset_index()
    return out


def build_time_series_metrics(
    df: pd.DataFrame,
    freq: str = "M",
    y_col: str = "y",
    yhat_col: str = "y_hat",
    ds_col: str = "ds",
) -> pd.DataFrame:
    """指定した freq 単位で誤差指標を集計した DataFrame を返す。

    Args:
        df: 予測結果を含む DataFrame（少なくとも y_col, yhat_col, ds_col を含む）
        freq: pandas の resample で使用する頻度文字列（例: "D", "W", "M"）
        y_col: 実測値カラム名
        yhat_col: 予測値カラム名
        ds_col: 日付カラム名

    Returns:
        ["ds", "mae", "rmse", "smape"] を持つ DataFrame。
        ds は resample 後の代表日時（period の左端）になる。
    """
    required = {y_col, yhat_col, ds_col}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"必要なカラムが不足しています: {missing}")

    tmp = df.copy()
    tmp[ds_col] = pd.to_datetime(tmp[ds_col])

    tmp = tmp.set_index(ds_col)

    def _agg(group: pd.DataFrame) -> pd.Series:
        y = group[y_col].to_numpy()
        yhat = group[yhat_col].to_numpy()
        return pd.Series(
            {
                "mae": mae(y, yhat),
                "rmse": rmse(y, yhat),
                "smape": smape(y, yhat),
            }
        )

    out = tmp.resample(freq).apply(_agg)
    out = out.reset_index().rename(columns={ds_col: "ds"})
    return out
