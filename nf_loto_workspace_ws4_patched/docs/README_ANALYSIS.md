# NeuralForecast Model Analyzer v2

4つの基本ファイルのみからNeuralForecastモデルを完全分析するシステム

## 📋 概要

このシステムは、NeuralForecastで学習されたモデルディレクトリ内の4つの基本ファイルを解析し、モデルの構造・パラメータ・学習状態・健全性を包括的に評価します。

### 解析対象ファイル

1. `alias_to_model.pkl` - モデルエイリアスマッピング
2. `configuration.pkl` - 完全なモデル設定
3. `dataset.pkl` - データセット統計・メタ情報
4. `*.ckpt` - PyTorch Lightning チェックポイント

### 主な機能

- ✅ **モデルプロファイル抽出**: ハイパーパラメータ、パラメータ数、構造
- ✅ **重み統計量分析**: 層別の統計・健全性スコア・異常検出
- ✅ **学習状態分析**: エポック数、収束判定、Early stopping
- ✅ **複雑度評価**: メモリフットプリント、パラメータ効率
- ✅ **健全性診断**: 総合スコアと具体的な推奨事項
- ✅ **最適化提案**: 優先度付きの改善アクション
- ✅ **PostgreSQL統合**: 構造化データベース保存
- ✅ **可視化**: レポート用グラフ生成

## 🚀 クイックスタート

### 1. インストール

```bash
# 基本パッケージ
pip install pandas openpyxl torch numpy

# PostgreSQL統合（オプション）
pip install psycopg2-binary

# 可視化（オプション）
pip install matplotlib seaborn
```

または、requirements.txtから一括インストール:

```bash
pip install -r requirements_analysis.txt
```

### 2. PostgreSQLセットアップ（使用する場合）

```bash
# db_config.pyを編集してパスワード設定
nano db_config.py

# テーブル作成
python setup_analysis_tables.py create
```

### 3. 分析実行

```bash
# 基本実行
python run_analysis.py /path/to/model/directory

# または直接
python neuralforecast_analyzer_v2.py
```

### 4. 結果確認

```bash
# ファイル出力
ls nf_auto_runs/analysis/

# PostgreSQLクエリ
psql -U postgres -d postgres -f analysis_queries.sql
```

## 📁 ファイル構成

```
.
├── neuralforecast_analyzer_v2.py      # メイン分析エンジン
├── setup_analysis_tables.py           # PostgreSQLテーブル作成
├── analysis_visualizer.py             # 可視化生成
├── run_analysis.py                    # 簡易実行スクリプト
├── analysis_queries.sql               # SQLクエリ集
├── db_config.py                       # データベース設定
├── postgres_manager.py                # PostgreSQLマネージャー
├── requirements_analysis.txt          # 依存パッケージ
└── README_ANALYSIS.md                 # このファイル
```

## 💻 使用方法

### 基本的な使い方

```python
from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer

# 分析実行
analyzer = NeuralForecastAnalyzer("path/to/model")
results = analyzer.run_full_analysis(
    save_to_postgres=True,   # PostgreSQLに保存
    save_to_files=True,      # CSV/Excelに保存
    output_dir="nf_auto_runs/analysis"
)

# 結果確認
for table_name, df in results.items():
    print(f"{table_name}: {len(df)} rows")
```

### コマンドラインオプション

```bash
# PostgreSQL保存なし
python run_analysis.py /path/to/model --no-postgres

# 可視化のみ（既存データから）
python run_analysis.py /path/to/model --visualize-only

# ファイル保存のみ（PostgreSQLなし）
python run_analysis.py /path/to/model --no-postgres

# 出力ディレクトリ指定
python run_analysis.py /path/to/model --output ./my_results
```

### 可視化の生成

```bash
# 分析結果から可視化を生成
python analysis_visualizer.py nf_auto_runs/analysis
```

生成される可視化:
- `weight_distributions.png` - 重み分布の統計
- `hyperparameter_radar.png` - ハイパーパラメータの重要度
- `model_complexity_overview.png` - モデル複雑度の概観
- `diagnosis_summary.png` - 診断サマリ

## 📊 出力データ

### ファイル出力

```
nf_auto_runs/analysis/
├── model_profile_20250511_143022.csv
├── dataset_profile_20250511_143022.csv
├── training_state_20250511_143022.csv
├── weight_statistics_20250511_143022.csv
├── model_complexity_20250511_143022.csv
├── parameter_sensitivity_20250511_143022.csv
├── model_diagnosis_20250511_143022.csv
├── optimization_suggestions_20250511_143022.csv
├── model_analysis_20250511_143022.xlsx  # 統合Excel
└── visualizations/
    ├── weight_distributions.png
    ├── hyperparameter_radar.png
    ├── model_complexity_overview.png
    └── diagnosis_summary.png
```

### PostgreSQLテーブル

| テーブル名 | 内容 |
|-----------|------|
| `nf_model_profile` | モデル基本情報 |
| `nf_dataset_profile` | データセット統計 |
| `nf_training_state` | 学習状態 |
| `nf_weight_statistics` | 層別重み統計 |
| `nf_model_complexity` | 複雑度評価 |
| `nf_parameter_sensitivity` | パラメータ重要度 |
| `nf_model_diagnosis` | 健全性診断 |
| `nf_optimization_suggestions` | 最適化提案 |
| `vw_model_analysis_summary` | 統合サマリビュー |

## 🔍 便利なクエリ例

### 健全性スコアが低いモデルを検索

```sql
SELECT 
    model_alias,
    overall_score,
    weight_health,
    convergence_status
FROM nf_model_diagnosis
WHERE overall_score < 60
ORDER BY overall_score ASC;
```

### 高優先度の最適化提案

```sql
SELECT 
    mp.model_alias,
    os.parameter_name,
    os.expected_impact,
    os.priority
FROM nf_optimization_suggestions os
JOIN nf_model_profile mp ON os.model_dir_hash = mp.model_dir_hash
WHERE os.priority >= 4
ORDER BY os.priority DESC;
```

### 全モデルのサマリ

```sql
SELECT * FROM vw_model_analysis_summary
ORDER BY analyzed_at DESC;
```

その他のクエリは `analysis_queries.sql` を参照してください。

## 🎯 分析内容の詳細

### 1. モデルプロファイル抽出
- ハイパーパラメータの完全抽出
- パラメータ数（総数・学習可能数）
- モデルクラスとアーキテクチャ

### 2. 重み統計量分析
- **層別統計**: 平均・標準偏差・最小・最大
- **ノルム**: L1/L2ノルム
- **スパース性**: ゼロ比率
- **外れ値**: 3σ超過率
- **健全性スコア**: 0-10点評価

### 3. 学習状態分析
- 完了エポック数
- Early stoppingの発動有無
- 最終学習率
- チェックポイントサイズ

### 4. モデル複雑度分析
- **パラメータ効率**: params / (h × input_size)
- **メモリフットプリント**: MB単位
- **複雑度カテゴリ**: light/medium/heavy

### 5. 健全性診断
- **総合スコア**: 0-100点
- **重み健全性**: good/warning/bad
- **収束状態**: early_stopped/completed
- **推奨事項**: 具体的な改善アクション

### 6. 最適化提案
- **カテゴリ別提案**: パラメータ削減/学習安定化/容量向上
- **優先度**: 1-5（5が最高）
- **期待効果**: 定量的な影響予測

## ⚙️ 設定

### db_config.py

```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'port': 5432,
    'database': 'postgres',
    'user': 'postgres',
    'password': 'your_password',  # 変更必須
}
```

## 🐛 トラブルシューティング

### エラー1: ファイルが見つからない

```
✗ alias_to_model.pkl が見つかりません
```

**解決方法**: モデルディレクトリのパスを確認してください。4つの基本ファイルが全て存在する必要があります。

### エラー2: PostgreSQL接続エラー

```
✗ PostgreSQL接続失敗
```

**解決方法**:
1. PostgreSQLサービスが起動しているか確認
2. `db_config.py`のパスワードが正しいか確認
3. `setup_postgres.py test`で接続テスト

### エラー3: メモリエラー

```
MemoryError: Unable to allocate array
```

**解決方法**:
- 不要なプロセスを終了
- より大きいメモリのマシンで実行
- バッチ処理に分割（大規模モデルの場合）

### エラー4: 可視化エラー

```
ImportError: No module named 'matplotlib'
```

**解決方法**:
```bash
pip install matplotlib seaborn
```

## 📚 詳細ドキュメント

- **設計書**: システム全体の設計思想と実装詳細
- **SQLクエリ集**: `analysis_queries.sql`
- **インストールガイド**: `INSTALL.md`

## 🔄 ワークフロー例

### 日常運用

```bash
# 1. 新しいモデルを分析
python run_analysis.py /path/to/new/model

# 2. 結果をPostgreSQLで確認
psql -U postgres -d postgres

# 3. 健全性スコアをチェック
SELECT model_alias, overall_score, weight_health 
FROM nf_model_diagnosis 
ORDER BY overall_score DESC;

# 4. 最適化提案を確認
SELECT * FROM nf_optimization_suggestions 
WHERE priority >= 4;

# 5. 可視化レポートを生成
python analysis_visualizer.py nf_auto_runs/analysis
```

### バッチ処理

```python
from pathlib import Path
from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer

# 複数モデルを一括分析
model_dirs = Path("models").glob("*/")

for model_dir in model_dirs:
    print(f"\n分析中: {model_dir}")
    analyzer = NeuralForecastAnalyzer(str(model_dir))
    results = analyzer.run_full_analysis(
        save_to_postgres=True,
        save_to_files=True
    )
```

## 🎓 使用例

### 例1: モデルの健全性チェック

```python
from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer

analyzer = NeuralForecastAnalyzer("path/to/model")
results = analyzer.run_full_analysis()

# 診断結果を確認
diagnosis = results['model_diagnosis']
print(f"総合スコア: {diagnosis['overall_score'].iloc[0]}")
print(f"健全性: {diagnosis['weight_health'].iloc[0]}")
```

### 例2: 最適化提案の取得

```python
suggestions = results['optimization_suggestions']
high_priority = suggestions[suggestions['priority'] >= 4]

for _, row in high_priority.iterrows():
    print(f"パラメータ: {row['parameter_name']}")
    print(f"現在値: {row['current_value']}")
    print(f"推奨値: {row['suggested_value']}")
    print(f"効果: {row['expected_impact']}")
    print()
```

### 例3: 重み統計の可視化

```python
weight_stats = results['weight_statistics']

# 健全性スコアが低い層を抽出
unhealthy_layers = weight_stats[weight_stats['health_score'] < 5]
print(f"要注意層: {len(unhealthy_layers)} 個")
print(unhealthy_layers[['layer_name', 'health_score', 'outlier_ratio']])
```

## 🤝 貢献

バグ報告や機能提案は歓迎します。

## 📝 ライセンス

このプロジェクトはMITライセンスの下で公開されています。

## 📮 サポート

問題が発生した場合:
1. エラーメッセージ全文を確認
2. `setup_postgres.py test`で接続テスト
3. `python --version`と`pip list`で環境確認
4. 詳細なスタックトレースを含めて報告

---

**バージョン**: 2.0  
**最終更新**: 2025-05-11
