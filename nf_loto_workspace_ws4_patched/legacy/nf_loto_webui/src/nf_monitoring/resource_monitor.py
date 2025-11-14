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

    Returned keys are stable and JSON‑serialisable so they can be safely
    stored in PostgreSQL or logged as structured JSON.
    """
    snapshot: Dict[str, Any] = {
        "timestamp": time.time(),
        "platform": platform.platform(),
    }
    if not _PSUTIL_AVAILABLE:
        return snapshot

    assert psutil is not None  # type: ignore[truthy-function]

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
        # Snapshot is best‑effort; partial information is acceptable.
        pass
    return snapshot
