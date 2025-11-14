from __future__ import annotations

from pathlib import Path
import runpy

from ..core.exceptions import RunError


def run_legacy_nf_auto_runner(base_root: Path | None = None) -> None:
    """legacy/nf_loto_webui/nf_auto_runner_full.py をラップ実行する.

    本番コードでは、AutoModelFactory ベースのパイプラインに差し替える想定。

    Parameters
    ----------
    base_root:
        テストなどで任意のルートディレクトリを指定したい場合に利用する。
        None の場合は ``Path(__file__).resolve().parents[3]`` から自動検出する。
    """
    if base_root is None:
        root = Path(__file__).resolve().parents[3]
    else:
        root = Path(base_root)

    legacy_runner = root / "legacy" / "nf_loto_webui" / "nf_auto_runner_full.py"
    if not legacy_runner.exists():
        raise RunError(f"legacy runner not found: {legacy_runner}")
    try:
        runpy.run_path(str(legacy_runner), run_name="__main__")
    except SystemExit:
        # nf_auto_runner_full.py からの sys.exit を素通し
        return
    except Exception as exc:  # noqa: BLE001
        raise RunError(f"nf_auto_runner_full failed: {exc}") from exc
