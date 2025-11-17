from nf_loto_platform.reports import html_reporter
from pathlib import Path


def test_html_reporter_generates_string(tmp_path):
    html = html_reporter.render_simple_report(title="test", body="ok")
    assert isinstance(html, str)
    out = tmp_path / "report.html"
    html_reporter.write_report(out, html)
    assert out.exists()
