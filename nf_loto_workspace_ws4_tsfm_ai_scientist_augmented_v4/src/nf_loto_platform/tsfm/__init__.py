"""TSFM (Time Series Foundation Model) ハブ層.

各種 TSFM を共通インターフェイスで扱うためのアダプタとハブクラスを提供する。
実際のモデル本体はオプショナル依存とし、インポートに失敗した場合は
詳細なエラーメッセージ付きで NotImplementedError を投げる。
"""
from .base import (
    TSFMCapabilities,
    CostEstimate,
    ForecastResult,
    BaseTSFMAdapter,
    TSFMHub,
)

__all__ = [
    "TSFMCapabilities",
    "CostEstimate",
    "ForecastResult",
    "BaseTSFMAdapter",
    "TSFMHub",
]
