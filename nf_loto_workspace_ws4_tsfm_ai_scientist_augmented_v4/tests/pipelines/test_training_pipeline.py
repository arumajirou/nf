from pathlib import Path

import pytest

from nf_loto_platform.core.exceptions import RunError
from nf_loto_platform.pipelines import training_pipeline


def _write_dummy_legacy_runner(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")


def test_run_legacy_nf_auto_runner_raises_when_missing(tmp_path):
    """legacy runner が存在しない場合に RunError になることを確認する。"""
    base_root = tmp_path  # legacy/ 配下はまだ作らない
    with pytest.raises(RunError):
        training_pipeline.run_legacy_nf_auto_runner(base_root=base_root)


def test_run_legacy_nf_auto_runner_executes_dummy_script(tmp_path):
    """簡易な nf_auto_runner_full.py を用意した場合に正常終了すること。

    - dummy スクリプトでは単に print してから SystemExit(0) する。
    - training_pipeline 側では SystemExit を許容して RunError を出さない。
    """
    base_root = tmp_path
    legacy_runner = (
        base_root / "legacy" / "nf_loto_webui" / "nf_auto_runner_full.py"
    )
    _write_dummy_legacy_runner(
        legacy_runner,
        "import sys\nprint('dummy runner executed')\nsys.exit(0)\n",
    )

    # 例外が出なければ OK（SystemExit は内部で握りつぶされる想定）
    training_pipeline.run_legacy_nf_auto_runner(base_root=base_root)
