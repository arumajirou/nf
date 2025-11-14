
import os, pandas as pd

TARGET_SCHEMA = os.getenv("TARGET_SCHEMA", "public")
TARGET_TABLES = [
    "nf_model_profile",
    "nf_dataset_profile",
    "nf_training_state",
    "nf_weight_statistics",
    "nf_model_complexity",
    "nf_model_diagnosis",
    "nf_parameter_sensitivity",
    "nf_optimization_suggestions",
    "nf_runs",
    "nf_models",
    "nf_model",
    "nf_hparams",
    "nf_ckpt",
    "nf_config",
    "nf_pkl",
]
MAX_ROWS = None

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    host = os.getenv("PGHOST", "127.0.0.1")
    port = os.getenv("PGPORT", "5432")
    db   = os.getenv("PGDATABASE", "postgres")
    user = os.getenv("PGUSER", "postgres")
    pw   = os.getenv("PGPASSWORD", "")
    DATABASE_URL = f"postgresql+psycopg2://{user}:{pw}@{host}:{port}/{db}"

from sqlalchemy import create_engine, text
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def q(sql: str, params=None) -> pd.DataFrame:
    with engine.begin() as cx:
        return pd.read_sql(text(sql), cx, params=params or {})

placeholders = ",".join(["%s"] * len(TARGET_TABLES))
sql = f"""
SELECT table_name
FROM information_schema.tables
WHERE table_schema = %s
  AND table_name IN ({placeholders})
ORDER BY table_name
"""
params = tuple([TARGET_SCHEMA] + TARGET_TABLES)
with engine.begin() as cx:
    exists_df = pd.read_sql(text(sql), cx, params=params)

existing_tables = exists_df["table_name"].tolist()
print("existing:", existing_tables)

dfs = {}
for t in existing_tables:
    lim = f" LIMIT {int(MAX_ROWS)}" if MAX_ROWS else ""
    df = q(f'SELECT * FROM "{TARGET_SCHEMA}"."{t}"{lim}')
    dfs[t] = df
    globals()[f"df_{t}"] = df
    print(t, len(df))

# 例: print(dfs["nf_model_profile"].head())
