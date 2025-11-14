# NeuralForecast Model Analyzer - 拡張機能

## 📋 概要

基本分析システムを拡張し、以下の3つのフェーズで高度な機能を提供します：

- **フェーズ2**: 複数モデル比較
- **フェーズ3**: 予測データ統合と高度な評価
- **フェーズ4**: 自動化とアラートシステム

## 🚀 クイックスタート

### インストール

```bash
# 基本パッケージに加えて
pip install scipy requests  # 拡張機能用
```

### 対話型実行

```bash
python extended_runner.py
```

メニューから機能を選択して実行できます。

## 📦 フェーズ2: 複数モデル比較

### 概要

複数のモデルを横断的に比較し、最適なモデルを選定します。

### 機能

- ✅ **複数モデルの一括分析**: リストから自動実行
- ✅ **ハイパーパラメータ相関分析**: スコアとの相関を定量化
- ✅ **統計的比較**: ペアワイズ比較、分散分析
- ✅ **総合ランキング**: 重み付きスコアでベストモデルを特定
- ✅ **比較レポート**: 包括的なサマリを自動生成

### 使用方法

#### 1. モデルリストファイルを作成

`model_list.txt`:
```
# 比較するモデルのディレクトリ（1行に1つ）
/path/to/model1
/path/to/model2
/path/to/model3
```

#### 2. 比較実行

```bash
python multi_model_comparator.py model_list.txt
```

または：

```python
from multi_model_comparator import MultiModelComparator

comparator = MultiModelComparator()
results = comparator.analyze_multiple_models([
    "/path/to/model1",
    "/path/to/model2",
    "/path/to/model3"
])

# レポート生成
comparator.generate_comparison_report()
```

### 出力

```
nf_auto_runs/comparative_analysis/
├── model_summary_20250511_143022.csv         # 全モデルのサマリ
├── model_ranking_20250511_143022.csv         # ランキング
├── hyperparameter_correlation_*.json         # 相関分析
├── statistical_comparison_*.json             # 統計的比較
├── comparative_analysis_20250511_143022.xlsx # 統合Excel
└── comparison_report_20250511_143022.txt     # テキストレポート
```

### ランキングアルゴリズム

複合スコア = 健全性スコア(50%) + 層健全性(30%) + メモリ効率(20%)

各メトリクスは0-1に正規化され、重み付き平均で総合評価を算出します。

## 📊 フェーズ3: 予測データ統合

### 概要

`predictions.csv`を分析に統合し、Document 1の評価メニュー（A〜J）を実装します。

### 機能

#### A. 誤差の分解・安定性
- MAE, RMSE, MAPE, sMAPE
- MASE（ナイーブ予測との比較）
- バイアス分析
- 水準別誤差（低需要/中需要/高需要）

#### B. 確率予測の校正と区間品質
- PICP (Prediction Interval Coverage Probability)
- MIL (Mean Interval Length)
- Winklerスコア
- 校正状態の判定

#### C. 統計的モデル比較
- 残差の自己相関検定
- 正規性検定（Shapiro-Wilk）
- 白色ノイズ検定

#### D. データドリフト・レジーム変化
- Kolmogorov-Smirnov検定
- 平均値・分散のシフト検出
- 前半/後半の分布比較

#### E. ロバストネス・ストレス試験
- 外れ値での精度評価
- ゼロ値での予測性能
- ロバストネス比率

#### F. 多変量構造
- 系列間の相関分析
- 系列ごとのMAE評価

#### G. ビジネス適合・意思決定連携
- サービスレベル計算
- コスト敏感メトリクス
- バイアス方向の分析

#### H. 可視化・説明可能性
- 重要パラメータの抽出
- モデル複雑度との統合

### 使用方法

```bash
python prediction_integrator.py /path/to/model /path/to/predictions.csv
```

または：

```python
from prediction_integrator import PredictionAnalyzer

analyzer = PredictionAnalyzer(
    model_dir="/path/to/model",
    predictions_csv="/path/to/predictions.csv"
)

results = analyzer.run_integrated_analysis()
analyzer.generate_comprehensive_report()
```

### 出力

```
nf_auto_runs/prediction_analysis/
├── integrated_metrics_20250511_143022.json   # 全メトリクス
├── metrics_summary_20250511_143022.csv       # サマリCSV
└── integrated_report_20250511_143022.txt     # テキストレポート
```

### 実装例: カスタム評価

```python
# 特定のメトリクスにアクセス
error_metrics = results['A_error_decomposition']
print(f"MAE: {error_metrics['mae']:.4f}")
print(f"MASE: {error_metrics['mase']:.4f}")

# ビジネスメトリクス
business = results['G_business_metrics']
print(f"サービスレベル: {business['service_level']:.2%}")
print(f"総コスト: {business['total_cost']:.2f}")
```

## 🤖 フェーズ4: 自動化とアラート

### 概要

モデルの継続的監視、自動分析、アラート通知を実現します。

### 機能

- ✅ **スケジュール実行**: cron/タスクスケジューラー統合
- ✅ **健全性監視**: 閾値ベースのアラート
- ✅ **メール通知**: SMTP経由の自動通知
- ✅ **Slack通知**: Webhook統合
- ✅ **CI/CD統合**: GitHub Actions/GitLab CI対応
- ✅ **ログ管理**: 実行履歴の自動記録

### セットアップ

#### 対話型セットアップ

```bash
python automation_system.py setup
```

以下の項目を設定します：
1. 監視対象のモデルディレクトリ
2. アラート設定（メール/Slack）
3. 健全性スコア閾値（デフォルト: 60）
4. スケジュール実行方法

#### 設定ファイル: `automation_config.json`

```json
{
  "monitoring": {
    "enabled": true,
    "health_score_threshold": 60,
    "check_interval_hours": 24
  },
  "alerts": {
    "enabled": true,
    "email": {
      "smtp_server": "smtp.gmail.com",
      "smtp_port": 587,
      "sender_email": "your_email@example.com",
      "sender_password": "your_password",
      "recipients": ["recipient@example.com"]
    },
    "slack": {
      "enabled": true,
      "webhook_url": "https://hooks.slack.com/..."
    }
  },
  "models": {
    "watch_directories": [
      "/path/to/model1",
      "/path/to/model2"
    ]
  }
}
```

### スケジュール実行

#### Windows (タスクスケジューラー)

```powershell
# PowerShellで実行
$action = New-ScheduledTaskAction -Execute "python" -Argument "C:\path\to\automation_system.py run"
$trigger = New-ScheduledTaskTrigger -Daily -At 00:00
Register-ScheduledTask -TaskName "NeuralForecastMonitor" -Action $action -Trigger $trigger
```

#### Linux (cron)

```bash
# crontabを編集
crontab -e

# 毎日0時に実行
0 0 * * * cd /path/to/scripts && python automation_system.py run >> automation.log 2>&1
```

#### GitHub Actions

`.github/workflows/model_analysis.yml`:
```yaml
name: Model Analysis

on:
  schedule:
    - cron: '0 0 * * *'  # 毎日0時
  workflow_dispatch:

jobs:
  analyze:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - run: pip install -r requirements_analysis.txt
    - run: python automation_system.py run
```

### 手動監視実行

```bash
python automation_system.py monitor
```

### アラート例

#### メール通知

```
件名: ⚠ モデル健全性アラート: AutoTCN_Model

モデル: AutoTCN_Model
総合スコア: 45.3/100 (閾値: 60)
重み健全性: bad

アクション:
- モデルの再トレーニングを検討してください
- ハイパーパラメータの調整が必要です

生成日時: 2025-05-11 09:15:23
```

#### Slack通知

```
⚠ *モデル健全性アラート*
モデル: AutoTCN_Model
スコア: 45.3/100
```

## 🔄 統合パイプライン

### 完全パイプライン実行

すべてのフェーズを統合的に実行：

```bash
python extended_runner.py --full-pipeline /path/to/model --predictions /path/to/predictions.csv
```

パイプライン内容：
1. 基本分析（v2）
2. 予測データ統合（フェーズ3）
3. 可視化生成
4. 結果の統合保存

### パイプライン出力

```
nf_auto_runs/
├── analysis/                    # 基本分析結果
│   ├── model_profile_*.csv
│   ├── weight_statistics_*.csv
│   └── visualizations/
├── prediction_analysis/         # 予測統合結果
│   ├── integrated_metrics_*.json
│   └── integrated_report_*.txt
└── comparative_analysis/        # 複数モデル比較
    └── model_ranking_*.csv
```

## 📈 実用例

### 例1: モデル選定ワークフロー

```bash
# 1. 複数のモデル候補を比較
python multi_model_comparator.py candidate_models.txt

# 2. ベストモデルの詳細分析
python run_analysis.py /path/to/best_model

# 3. 予測データで性能評価
python prediction_integrator.py /path/to/best_model predictions.csv

# 4. 監視設定
python automation_system.py setup
```

### 例2: 継続的モニタリング

```python
# automation_config.jsonを設定後
from automation_system import AutomationConfig, ModelMonitor

config = AutomationConfig()
monitor = ModelMonitor(config)

# 定期実行（cronやタスクスケジューラーから）
results = monitor.monitor_models()

# 閾値以下のモデルには自動的にアラートが送信される
```

### 例3: CI/CDパイプライン

```yaml
# .gitlab-ci.yml
stages:
  - train
  - analyze
  - deploy

analyze_model:
  stage: analyze
  script:
    - python run_analysis.py models/latest
    - python prediction_integrator.py models/latest predictions.csv
  artifacts:
    reports:
      junit: nf_auto_runs/analysis/*.xml
  only:
    - main
```

## 🛠️ トラブルシューティング

### エラー1: メール送信失敗

```
✗ メールアラート送信エラー: Authentication failed
```

**解決方法**:
- Gmailの場合: アプリパスワードを使用
- セキュリティ設定で「安全性の低いアプリ」を許可
- SMTP設定を確認

### エラー2: predictions.csvのカラムが見つからない

```
Required columns not found
```

**解決方法**:
- `y`, `y_hat`カラムが必須
- 予測区間の場合: `y_hat_lo-90`, `y_hat_hi-90`
- カラム名を確認: `df.columns`

### エラー3: 相関分析でデータ不足

```
相関分析には3つ以上のモデルが必要です
```

**解決方法**:
- 少なくとも3つのモデルを分析対象に含める
- モデルリストファイルを確認

## 📚 詳細ドキュメント

- **基本分析**: `README_ANALYSIS.md`
- **SQLクエリ**: `analysis_queries.sql`
- **使用例**: `usage_examples_analysis.py`

## 🎯 ベストプラクティス

### モデル比較

1. **同一データセット**: 公平な比較のため
2. **同一評価期間**: テストセットを揃える
3. **複数メトリクス**: 単一指標に依存しない

### 予測評価

1. **複数メトリクス**: MAE, MASE, Winklerを併用
2. **ビジネス観点**: サービスレベル、コストを考慮
3. **ドリフト検出**: 定期的に実行

### 自動化

1. **段階的導入**: まず手動実行で動作確認
2. **ログ管理**: 実行履歴を定期的に確認
3. **閾値調整**: 環境に応じて最適化

## 🔍 FAQ

**Q: フェーズ2で何モデルまで比較できますか？**
A: 制限はありませんが、10-20モデル程度が実用的です。

**Q: predictions.csvの形式は？**
A: NeuralForecastの標準出力形式（`unique_id`, `ds`, `y`, `y_hat`カラム）

**Q: アラートの閾値はどう決めますか？**
A: 最初は60（デフォルト）から始め、環境に応じて調整してください。

**Q: 複数のSlackチャンネルに通知できますか？**
A: 現在は単一のWebhook URLのみ対応。複数の場合は設定を複製してください。

## 📮 サポート

拡張機能に関する質問や問題:
1. ログファイル（`automation.log`）を確認
2. エラーメッセージ全文を確認
3. 設定ファイル（`automation_config.json`）を確認

---

**バージョン**: 2.0 Extended  
**最終更新**: 2025-05-11
