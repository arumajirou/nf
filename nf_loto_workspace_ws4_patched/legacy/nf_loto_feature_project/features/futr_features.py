from datetime import timedelta
from typing import List
import pandas as pd

from .feature_config import DEFAULT_CONFIG

def _generate_future_dates(df: pd.DataFrame, horizon_days: int = 365) -> pd.DataFrame:
    # ds の最大値から未来 1 年分を生成
    max_ds = df["ds"].max()
    # 仮に日次ステップで生成しておき、後でフィルタも可能
    future_dates = pd.date_range(max_ds + timedelta(days=1),
                                 max_ds + timedelta(days=horizon_days),
                                 freq="D")
    rows = []
    for (loto, uid), _ in df.groupby(["loto", "unique_id"]):
        for ds in future_dates:
            rows.append({"loto": loto, "unique_id": uid, "ds": ds})
    return pd.DataFrame(rows)

def _add_calendar_features(df: pd.DataFrame) -> pd.DataFrame:
    cfg = DEFAULT_CONFIG.futr_calendar
    df = df.copy()
    if cfg.add_month:
        df["futr_month"] = df["ds"].dt.month
    if cfg.add_dow:
        df["futr_dow"] = df["ds"].dt.weekday
    if cfg.add_weekofyear:
        df["futr_weekofyear"] = df["ds"].dt.isocalendar().week.astype(int)
    if cfg.add_cyclical:
        doy = df["ds"].dt.dayofyear
        df["futr_sin_2pi_doy"] = (2 * 3.14159265 * doy / 365.25).apply(lambda x: __import__("math").sin(x))
        df["futr_cos_2pi_doy"] = (2 * 3.14159265 * doy / 365.25).apply(lambda x: __import__("math").cos(x))
    # 休日フラグなどは環境依存なのでダミー実装
    if cfg.add_holiday_flags:
        df["futr_is_holiday"] = 0
    return df

def build_futr_features(base_df: pd.DataFrame) -> pd.DataFrame:
    """未来既知外生 (futr_) を生成する。

    出力: loto, unique_id, ds, futr_* カラム
    """
    futr_df = _generate_future_dates(base_df)
    futr_df = _add_calendar_features(futr_df)
    # ロト固有特徴 (抽選日など) はここに追加していく
    # 例: 金曜が抽選日のロトであれば futr_is_draw_day_loto6 を付ける 等
    return futr_df
