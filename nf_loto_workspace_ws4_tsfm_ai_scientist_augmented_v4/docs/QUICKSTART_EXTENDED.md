# 拡張機能 クイックスタートガイド

## 🎯 5分で始める拡張機能

### ステップ1: 依存パッケージのインストール

```bash
pip install scipy requests
```

または完全版:
```bash
pip install -r requirements_extended.txt
```

---

## 📊 フェーズ2: 複数モデル比較

### 最小コマンド

```bash
# 1. モデルリストを作成
echo "/path/to/model1" > models.txt
echo "/path/to/model2" >> models.txt
echo "/path/to/model3" >> models.txt

# 2. 比較実行
python multi_model_comparator.py models.txt
```

### 結果確認

```bash
# 出力ディレクトリ
ls nf_auto_runs/comparative_analysis/

# ランキング確認
cat nf_auto_runs/comparative_analysis/comparison_report_*.txt
```

---

## 🔬 フェーズ3: 予測データ統合

### 最小コマンド

```bash
python prediction_integrator.py ./model ./predictions.csv
```

### 結果確認

```bash
# レポート確認
cat nf_auto_runs/prediction_analysis/integrated_report_*.txt

# メトリクス詳細
cat nf_auto_runs/prediction_analysis/integrated_metrics_*.json
```

---

## 🤖 フェーズ4: 自動化

### 最小セットアップ

```bash
# 1. 対話型セットアップ
python automation_system.py setup

# 質問に答えていく:
# - 監視するモデルディレクトリ: /path/to/model
# - アラートを有効化: n (最初はスキップ推奨)
# - 健全性スコア閾値: 60
# - スケジュール: 4 (スキップ)

# 2. 手動実行でテスト
python automation_system.py monitor
```

### スケジュール実行（Linux）

```bash
# crontabに追加（毎日0時実行）
(crontab -l 2>/dev/null; echo "0 0 * * * cd $(pwd) && python automation_system.py run") | crontab -
```

---

## 🔄 統合パイプライン

### 全機能を一度に実行

```bash
python extended_runner.py --full-pipeline ./model --predictions ./predictions.csv
```

### 対話型メニュー

```bash
python extended_runner.py
```

メニューから機能を選択。

---

## 📋 チェックリスト

### フェーズ2を使う前に

- [ ] 複数のモデルディレクトリを用意
- [ ] モデルリストファイル（models.txt）を作成
- [ ] `scipy`をインストール

### フェーズ3を使う前に

- [ ] `predictions.csv`を用意（必須カラム: `y`, `y_hat`）
- [ ] モデルディレクトリを指定
- [ ] `scipy`をインストール

### フェーズ4を使う前に

- [ ] 監視対象のモデルディレクトリを決定
- [ ] 健全性スコアの閾値を決定（推奨: 60）
- [ ] メール通知を使う場合: SMTP設定を準備
- [ ] `requests`をインストール（Slack通知の場合）

---

## 💡 よくある質問

**Q: どのフェーズから始めればいい？**
A: 
- 複数モデルの選定が必要 → フェーズ2
- 実際の予測精度を評価したい → フェーズ3
- 継続的に監視したい → フェーズ4

**Q: 全部使う必要がある？**
A: いいえ。必要な機能だけ使えます。独立して動作します。

**Q: 基本分析（v2）との違いは？**
A: 
- 基本分析: 単一モデルの構造・重み分析
- フェーズ2: 複数モデル間の比較
- フェーズ3: 実際の予測性能評価
- フェーズ4: 自動化・継続監視

---

## 🎓 実用例

### 例1: 新規モデル開発

```bash
# 1. 候補モデルを複数学習
# 2. フェーズ2で比較
python multi_model_comparator.py candidates.txt
# 3. ベストモデルをフェーズ3で詳細評価
python prediction_integrator.py ./best_model ./predictions.csv
# 4. 本番環境でフェーズ4で監視
python automation_system.py setup
```

### 例2: 既存モデルの監視

```bash
# 1. 自動化セットアップ
python automation_system.py setup
# 2. cronで毎日実行
# → 異常時に自動アラート
```

### 例3: 予測精度の深掘り分析

```bash
# predictions.csvがあれば即座に実行
python prediction_integrator.py ./model ./predictions.csv

# A〜Hの全メトリクスが自動計算される
```

---

## 📂 出力ファイル構造

```
nf_auto_runs/
├── analysis/                    # 基本分析（v2）
│   ├── model_profile_*.csv
│   └── visualizations/
├── comparative_analysis/        # フェーズ2
│   ├── model_ranking_*.csv
│   └── comparison_report_*.txt
├── prediction_analysis/         # フェーズ3
│   ├── integrated_metrics_*.json
│   └── integrated_report_*.txt
└── automation.log              # フェーズ4
```

---

## 🚨 トラブルシューティング

### エラー: ModuleNotFoundError: No module named 'scipy'

```bash
pip install scipy
```

### エラー: predictions.csv not found

```bash
# ファイルパスを確認
ls ./predictions.csv
# または絶対パスを使用
python prediction_integrator.py ./model /full/path/to/predictions.csv
```

### エラー: メール送信失敗

```bash
# automation_config.jsonを編集
# sender_passwordを正しいアプリパスワードに設定
```

---

## 📞 次のステップ

- 詳細ドキュメント: `README_EXTENDED.md`
- 基本分析: `README_ANALYSIS.md`
- 使用例: `usage_examples_analysis.py`

---

**準備完了！** 早速使ってみましょう 🚀
