import numpy as np
import pandas as pd

def build_stat_features(base_df: pd.DataFrame) -> pd.DataFrame:
    """静的外生 (stat_) を生成する。

    系列ごとの集約統計などを持たせる。
    出力: loto, unique_id, stat_* カラム
    """
    grp = base_df.groupby(["loto", "unique_id"])["y"]
    agg = grp.agg(["mean", "std", "min", "max"])
    agg = agg.rename(columns={
        "mean": "stat_y_mean",
        "std": "stat_y_std",
        "min": "stat_y_min",
        "max": "stat_y_max",
    })
    agg = agg.reset_index()

    # ロト種別などの追加例 (ここではダミー)
    agg["stat_loto_type"] = agg["loto"]
    # 数値位置情報などは unique_id から生成することも可能

    return agg
