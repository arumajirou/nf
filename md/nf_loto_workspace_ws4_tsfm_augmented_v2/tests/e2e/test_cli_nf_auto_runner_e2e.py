from pathlib import Path

import pytest

from nf_loto_platform.pipelines import training_pipeline


@pytest.mark.e2e
def test_cli_nf_auto_runner_e2e_with_dummy_legacy_script(tmp_path):
    """CLI 相当の経路で legacy runner を 1 周させる E2E スモークテスト。

    - 実際の CLI 実装はまだ薄いが、`training_pipeline.run_legacy_nf_auto_runner`
      を通して `legacy/nf_loto_webui/nf_auto_runner_full.py` が実行される経路を確認する。
    - テストではダミーの nf_auto_runner_full.py を生成し、SystemExit(0) で終了させる。
    """
    base_root = tmp_path
    legacy_runner = (
        base_root / "legacy" / "nf_loto_webui" / "nf_auto_runner_full.py"
    )
    legacy_runner.parent.mkdir(parents=True, exist_ok=True)
    legacy_runner.write_text(
        "import sys\nprint('dummy cli runner executed')\nsys.exit(0)\n",
        encoding="utf-8",
    )

    # 例外が出なければ OK
    training_pipeline.run_legacy_nf_auto_runner(base_root=base_root)
