"""ロト特徴量生成メインスクリプト。

nf_loto_final から履歴/未来/静的特徴を生成し、
nf_loto_hist_exog / nf_loto_futr_exog / nf_loto_stat_exog / nf_loto_y_features
に保存する。
"""
import pandas as pd

from loto_pg_store import read_by_date_range
from postgres_manager import PostgreSQLManager
from features.futr_features import build_futr_features
from features.hist_features import build_hist_features
from features.stat_features import build_stat_features
from features.y_representation import build_y_features
from features.cleaning import clean_nan_inf

KEY_COLS_HIST = ["loto", "unique_id", "ds"]
KEY_COLS_FUTR = ["loto", "unique_id", "ds"]
KEY_COLS_STAT = ["loto", "unique_id"]

def load_nf_loto_final() -> pd.DataFrame:
    """
    nf_loto_final を全件ロードする。

    read_by_date_range(start=None, end=None) だと
    WHERE ds >= NULL AND ds < NULL になってしまい 0 件になるため、
    ここでは素直に SELECT * FROM を使う。
    """
    conn = psycopg2.connect(**DB_CONFIG)
    with conn:
        df = pd.read_sql(
            f"SELECT {', '.join(COLS)} FROM {TABLE_NAME} "
            "ORDER BY loto, ds, num, unique_id",
            conn,
        )
    return df

def main():
    print("Loading nf_loto_final...")
    df = load_nf_loto_final()
    if df.empty:
        print("nf_loto_final is empty. Abort.")
        return

    print("Building hist features...")
    hist_df = build_hist_features(df)
    hist_df = clean_nan_inf(hist_df, KEY_COLS_HIST)

    print("Building stat features...")
    stat_df = build_stat_features(df)
    stat_df = clean_nan_inf(stat_df, KEY_COLS_STAT)

    print("Building y-based features...")
    yfeat_df = build_y_features(df)
    yfeat_df = clean_nan_inf(yfeat_df, KEY_COLS_HIST)

    print("Building future features...")
    futr_df = build_futr_features(df)
    futr_df = clean_nan_inf(futr_df, KEY_COLS_FUTR)

    with PostgreSQLManager() as pm:
        print("Upserting hist features -> nf_loto_hist_exog")
        pm.upsert_dataframe(hist_df, table_name="nf_loto_hist_exog",
                            key_cols=KEY_COLS_HIST)
        print("Upserting stat features -> nf_loto_stat_exog")
        pm.upsert_dataframe(stat_df, table_name="nf_loto_stat_exog",
                            key_cols=KEY_COLS_STAT)
        print("Upserting y-based features -> nf_loto_y_features")
        pm.upsert_dataframe(yfeat_df, table_name="nf_loto_y_features",
                            key_cols=KEY_COLS_HIST)
        print("Upserting future features -> nf_loto_futr_exog")
        pm.upsert_dataframe(futr_df, table_name="nf_loto_futr_exog",
                            key_cols=KEY_COLS_FUTR)

    print("Done.")

if __name__ == "__main__":
    main()
