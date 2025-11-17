"""nf_loto_platform.webui

WebUI (Streamlit など) との統合ポイントをまとめるモジュール。

現時点では Streamlit 自身の有無を判定する薄いラッパーのみを提供し、
本格的な UI 実装は別リポジトリ / ディレクトリに配置する想定。
"""

from __future__ import annotations

from typing import Any


def is_webui_available() -> bool:
    """Streamlit ベースの WebUI が利用可能かを簡易判定する。

    実際に import してみて結果だけを bool で返す。
    WebUI が導入されていない環境でも import エラーにはならず、
    常に True/False のどちらかを返すことを契約とする。
    """
    try:
        import streamlit as _st  # type: ignore[import]

        _ = _st  # noqa: F841
        return True
    except Exception:  # pragma: no cover - 環境依存
        return False


__all__ = ["is_webui_available"]
