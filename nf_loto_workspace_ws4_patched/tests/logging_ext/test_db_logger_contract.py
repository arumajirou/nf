"""Light‑weight contract tests for logging_ext.db_logger.

These do *not* hit a real database; they only verify that the expected
functions exist so that callers (model_runner, pipelines, etc.) do not
crash on import.
"""

import importlib
import inspect


def test_db_logger_public_api_shape():
    module = importlib.import_module("nf_loto_platform.logging_ext.db_logger")

    required = {
        "log_run_start",
        "log_run_end",
        "log_run_error",
    }
    funcs = {name for name, obj in inspect.getmembers(module, inspect.isfunction)}
    assert required.issubset(funcs)
