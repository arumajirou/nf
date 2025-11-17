from __future__ import annotations

import platform
import time
from typing import Dict, Any

try:  # pragma: no cover - psutil may not be installed in all environments
    import psutil
    _PSUTIL_AVAILABLE = True
except Exception:  # pragma: no cover
    psutil = None  # type: ignore[assignment]
    _PSUTIL_AVAILABLE = False


def collect_resource_snapshot() -> Dict[str, Any]:
    """Collect a light‑weight snapshot of system resources.

    戻り値:
        CPU・メモリ・プロセス使用量などを含む辞書。
        psutil が無い環境では、最低限の情報（プラットフォーム・タイムスタンプ・cpu_percent=0.0）のみを返す。
    """
    snapshot: Dict[str, Any] = {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "timestamp": time.time(),
    }

    if _PSUTIL_AVAILABLE:
        try:
            snapshot["cpu_percent"] = psutil.cpu_percent(interval=None)
            vm = psutil.virtual_memory()
            snapshot["memory_total"] = vm.total
            snapshot["memory_used"] = vm.used
            snapshot["memory_percent"] = vm.percent

            proc = psutil.Process()
            pm = proc.memory_info()
            snapshot["process_rss"] = pm.rss
            snapshot["process_vms"] = pm.vms
        except Exception:  # pragma: no cover - defensive
            # Snapshot はベストエフォート。途中で失敗しても取れた分だけ返す。
            pass
    else:
        # psutil が無い環境向けのフォールバック
        snapshot["cpu_percent"] = 0.0

    return snapshot


def collect_resource_usage() -> Dict[str, Any]:
    """外部から利用しやすいエイリアス関数。

    tests ではこの関数を前提としているので、実装は collect_resource_snapshot に委譲する。
    """
    return collect_resource_snapshot()
