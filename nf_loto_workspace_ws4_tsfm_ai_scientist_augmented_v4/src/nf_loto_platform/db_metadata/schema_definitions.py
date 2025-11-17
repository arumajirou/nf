"""DDL strings and table name constants for metadata tables.

These are kept in Python so that migrations and tests can share the
same source of truth.
"""

NF_MODEL_RUNS_TABLE = "nf_model_runs"
NF_FEATURE_SETS_TABLE = "nf_feature_sets"
NF_DATASETS_TABLE = "nf_datasets"
NF_MODEL_REGISTRY_TABLE = "nf_model_registry"
NF_DRIFT_METRICS_TABLE = "nf_drift_metrics"
NF_RESIDUAL_ANOMALIES_TABLE = "nf_residual_anomalies"
NF_REPORTS_TABLE = "nf_reports"

DDL_EXTEND_METADATA_TABLES = """
-- Metadata tables for NeuralForecast MLOps extensions

CREATE TABLE IF NOT EXISTS nf_feature_sets (
    id              SERIAL PRIMARY KEY,
    name            TEXT NOT NULL,
    description     TEXT,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS nf_datasets (
    id              SERIAL PRIMARY KEY,
    table_name      TEXT NOT NULL,
    loto            TEXT NOT NULL,
    unique_ids      TEXT[] NOT NULL,
    ds_start        DATE,
    ds_end          DATE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS nf_model_registry (
    id              SERIAL PRIMARY KEY,
    model_key       TEXT NOT NULL,
    run_id          INTEGER NOT NULL REFERENCES nf_model_runs(id),
    stage           TEXT NOT NULL DEFAULT 'dev', -- dev / staging / prod / archived
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS nf_drift_metrics (
    id              SERIAL PRIMARY KEY,
    run_id          INTEGER NOT NULL REFERENCES nf_model_runs(id),
    column_name     TEXT NOT NULL,
    mean_diff       DOUBLE PRECISION,
    std_ratio       DOUBLE PRECISION,
    kl_div          DOUBLE PRECISION,
    window_start    DATE,
    window_end      DATE,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS nf_residual_anomalies (
    id              SERIAL PRIMARY KEY,
    run_id          INTEGER NOT NULL REFERENCES nf_model_runs(id),
    ds              TIMESTAMPTZ NOT NULL,
    unique_id       TEXT NOT NULL,
    residual        DOUBLE PRECISION,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS nf_reports (
    id              SERIAL PRIMARY KEY,
    run_id          INTEGER NOT NULL REFERENCES nf_model_runs(id),
    report_type     TEXT NOT NULL, -- 'html', 'pdf', ...
    storage_path    TEXT NOT NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
"""


def get_extend_metadata_ddl() -> str:
    """Return the SQL DDL used to create all metadata tables."""
    return DDL_EXTEND_METADATA_TABLES
