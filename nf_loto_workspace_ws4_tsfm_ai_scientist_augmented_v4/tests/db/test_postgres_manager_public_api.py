from importlib import import_module
import types
import pytest


def test_postgres_manager_importable():
    mod = import_module("nf_loto_platform.db.postgres_manager")
    assert isinstance(mod, types.ModuleType)


def test_postgres_manager_has_get_connection(monkeypatch):
    mod = import_module("nf_loto_platform.db.postgres_manager")
    assert hasattr(mod, "get_connection")

    dummy_conn = object()
    monkeypatch.setattr(mod.psycopg2, "connect", lambda **kwargs: dummy_conn)

    conn = mod.get_connection()
    assert conn is dummy_conn
