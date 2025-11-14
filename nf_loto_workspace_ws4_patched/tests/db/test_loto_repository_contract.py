"""Contract tests for nf_loto_platform.db.loto_repository."""

import importlib
import inspect


def test_loto_repository_public_api():
    module = importlib.import_module("nf_loto_platform.db.loto_repository")

    required_funcs = {
        "get_connection",
        "list_loto_tables",
        "load_panel_by_loto",
    }
    funcs = {name for name, obj in inspect.getmembers(module, inspect.isfunction)}
    assert required_funcs.issubset(funcs)
