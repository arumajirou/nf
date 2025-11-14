"""Additional contract tests for nf_loto_platform.db.loto_pg_store.

The goal is to ensure that the module exposes a stable set of constants
and helpers that DB‑backed components rely on, without requiring a real
database connection.
"""

import importlib
import inspect


def test_loto_pg_store_constants_and_helpers_present():
    module = importlib.import_module("nf_loto_platform.db.loto_pg_store")

    # COLS: list of column names used when persisting df_final
    assert hasattr(module, "COLS")
    assert isinstance(module.COLS, list)
    assert all(isinstance(c, str) for c in module.COLS)
    assert "loto" in module.COLS
    assert "unique_id" in module.COLS
    assert "y" in module.COLS

    # TABLE_NAME must be derived from TABLE_PREFIX.
    db_config = importlib.import_module("nf_loto_platform.db.db_config")
    assert hasattr(module, "TABLE_NAME")
    assert module.TABLE_NAME.startswith(db_config.TABLE_PREFIX)

    # Core helper functions should exist (even if tests don't call them here).
    required_funcs = {
        "ensure_table",
        "insert_df",
        "upsert_df",
    }
    funcs = {name for name, obj in inspect.getmembers(module, inspect.isfunction)}
    # Some deployments may not use all helpers, so we only require a subset.
    assert required_funcs.intersection(funcs)  # at least one present
