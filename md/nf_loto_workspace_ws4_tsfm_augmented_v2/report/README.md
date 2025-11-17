# pytest レポート出力ガイド

このディレクトリは、テスト実行結果や解析レポートを HTML などで保存するための場所です。

## pytest-html によるレポート出力例

```bash
# ルートディレクトリで実行
pytest --html=report/pytest_report.html --self-contained-html
```

- `report/pytest_report.html` に単一ファイルの HTML レポートが生成されます。
- CI から成果物として保存する場合も、このパスをそのまま利用できます。

## 既存サンプル

- `pytest_report_example.html` : 今回の検証用に生成されたサンプルレポートです。
