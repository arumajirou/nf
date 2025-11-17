import sys
from pathlib import Path
import pytest

# --- パス解決（インポート時に実行される） ---
_HERE = Path(__file__).resolve()
# tests/ の親 (プロジェクトルート) までさかのぼる
_PROJECT_ROOT = _HERE.parent.parent
_SRC_ROOT = _PROJECT_ROOT / "src"

if _SRC_ROOT.exists():
    s = str(_SRC_ROOT)
    if s not in sys.path:
        sys.path.insert(0, s)

@pytest.fixture(scope="session")
def project_root() -> Path:
    """プロジェクトルート (src, tests, legacy などを含むルート)。"""
    return _PROJECT_ROOT

@pytest.fixture(scope="session")
def src_root() -> Path:
    """src ディレクトリへのパス。"""
    return _SRC_ROOT

def pytest_configure(config: pytest.Config) -> None:
    config.addinivalue_line("markers", "integration: integration tests requiring DB or external services")
    config.addinivalue_line("markers", "e2e: end-to-end tests including CLI/WebUI")
    config.addinivalue_line("markers", "nonfunctional: performance/reproducibility related tests")
    config.addinivalue_line("markers", "slow: potentially slow tests")
