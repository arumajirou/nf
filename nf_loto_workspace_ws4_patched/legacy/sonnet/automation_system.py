"""
フェーズ4: 自動化システム
Automation & Alert System

機能:
- スケジュール実行（cron/Task Scheduler）
- アラート機能（健全性スコアが閾値以下）
- CI/CDパイプライン統合
- メール通知
"""

import os
import sys
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional
import subprocess
import argparse


class AutomationConfig:
    """自動化設定"""
    
    def __init__(self, config_file: str = "automation_config.json"):
        self.config_file = Path(config_file)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """設定ファイルを読み込み"""
        if self.config_file.exists():
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # デフォルト設定
            return {
                'monitoring': {
                    'enabled': True,
                    'health_score_threshold': 60,
                    'check_interval_hours': 24
                },
                'alerts': {
                    'enabled': False,
                    'email': {
                        'smtp_server': 'smtp.gmail.com',
                        'smtp_port': 587,
                        'sender_email': 'your_email@example.com',
                        'sender_password': '',
                        'recipients': ['recipient@example.com']
                    },
                    'slack': {
                        'enabled': False,
                        'webhook_url': ''
                    }
                },
                'models': {
                    'watch_directories': [],
                    'analysis_on_new_model': True
                },
                'logging': {
                    'log_file': 'nf_auto_runs/automation.log',
                    'keep_logs_days': 30
                }
            }
    
    def save_config(self):
        """設定を保存"""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)
        print(f"✓ 設定保存: {self.config_file}")


class AlertManager:
    """アラート管理"""
    
    def __init__(self, config: AutomationConfig):
        self.config = config.config
    
    def send_email_alert(self, subject: str, body: str) -> bool:
        """メールアラートを送信"""
        if not self.config['alerts']['enabled']:
            return False
        
        email_config = self.config['alerts']['email']
        
        try:
            msg = MIMEMultipart()
            msg['From'] = email_config['sender_email']
            msg['To'] = ', '.join(email_config['recipients'])
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
            server.starttls()
            server.login(email_config['sender_email'], email_config['sender_password'])
            
            text = msg.as_string()
            server.sendmail(
                email_config['sender_email'],
                email_config['recipients'],
                text
            )
            server.quit()
            
            print("✓ メールアラート送信完了")
            return True
            
        except Exception as e:
            print(f"✗ メールアラート送信エラー: {e}")
            return False
    
    def send_slack_alert(self, message: str) -> bool:
        """Slackアラートを送信"""
        if not self.config['alerts']['slack']['enabled']:
            return False
        
        webhook_url = self.config['alerts']['slack']['webhook_url']
        
        try:
            import requests
            
            payload = {'text': message}
            response = requests.post(webhook_url, json=payload)
            
            if response.status_code == 200:
                print("✓ Slackアラート送信完了")
                return True
            else:
                print(f"✗ Slackアラート送信エラー: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"✗ Slackアラート送信エラー: {e}")
            return False
    
    def check_and_alert(self, analysis_results: Dict) -> bool:
        """分析結果をチェックしてアラート"""
        diagnosis = analysis_results.get('model_diagnosis')
        
        if diagnosis is None or len(diagnosis) == 0:
            return False
        
        overall_score = diagnosis['overall_score'].iloc[0]
        weight_health = diagnosis['weight_health'].iloc[0]
        model_alias = analysis_results.get('model_profile', {}).get('model_alias', ['Unknown'])[0] if analysis_results.get('model_profile') is not None else 'Unknown'
        
        threshold = self.config['monitoring']['health_score_threshold']
        
        if overall_score < threshold:
            # アラート発動
            subject = f"⚠ モデル健全性アラート: {model_alias}"
            body = f"""
モデル健全性アラート

モデル: {model_alias}
総合スコア: {overall_score:.1f}/100 (閾値: {threshold})
重み健全性: {weight_health}

アクション:
- モデルの再トレーニングを検討してください
- ハイパーパラメータの調整が必要です

詳細は分析レポートを確認してください。

生成日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            """
            
            # メール送信
            self.send_email_alert(subject, body)
            
            # Slack送信
            slack_message = f"⚠ *モデル健全性アラート*\nモデル: {model_alias}\nスコア: {overall_score:.1f}/100"
            self.send_slack_alert(slack_message)
            
            return True
        
        return False


class ModelMonitor:
    """モデル監視システム"""
    
    def __init__(self, config: AutomationConfig):
        self.config = config
        self.alert_manager = AlertManager(config)
    
    def monitor_models(self) -> Dict:
        """モデルを監視"""
        print("\n" + "="*80)
        print("モデル監視開始")
        print("="*80)
        print(f"日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        
        watch_dirs = self.config.config['models']['watch_directories']
        
        if not watch_dirs:
            print("⚠ 監視ディレクトリが設定されていません")
            return {}
        
        results = {}
        alerts_triggered = 0
        
        for i, model_dir in enumerate(watch_dirs, 1):
            print(f"[{i}/{len(watch_dirs)}] 監視中: {model_dir}")
            
            model_path = Path(model_dir)
            if not model_path.exists():
                print(f"  ⚠ ディレクトリが見つかりません")
                continue
            
            try:
                # モデル分析を実行
                from neuralforecast_analyzer_v2 import NeuralForecastAnalyzer
                
                analyzer = NeuralForecastAnalyzer(str(model_path))
                analysis_results = analyzer.run_full_analysis(
                    save_to_postgres=True,
                    save_to_files=True
                )
                
                # アラートチェック
                if self.alert_manager.check_and_alert(analysis_results):
                    alerts_triggered += 1
                    print(f"  ⚠ アラート発動")
                else:
                    print(f"  ✓ 正常")
                
                results[str(model_path)] = analysis_results
                
            except Exception as e:
                print(f"  ✗ エラー: {e}")
                continue
        
        print("\n" + "="*80)
        print(f"監視完了: {len(results)} モデル分析, {alerts_triggered} アラート")
        print("="*80)
        
        return results
    
    def detect_new_models(self) -> List[str]:
        """新しいモデルを検出"""
        # 実装: 監視ディレクトリ内の新しいモデルディレクトリを検出
        # タイムスタンプやメタデータを使用
        new_models = []
        # TODO: 実装
        return new_models


class CIIntegration:
    """CI/CD統合"""
    
    @staticmethod
    def generate_github_actions_workflow() -> str:
        """GitHub Actionsワークフローを生成"""
        workflow = """
name: NeuralForecast Model Analysis

on:
  push:
    paths:
      - 'models/**'
  schedule:
    - cron: '0 0 * * *'  # 毎日0時に実行
  workflow_dispatch:

jobs:
  analyze-models:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout
      uses: actions/checkout@v3
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install pandas numpy torch psycopg2-binary matplotlib seaborn
    
    - name: Run model analysis
      env:
        DB_PASSWORD: ${{ secrets.DB_PASSWORD }}
      run: |
        python run_analysis.py models/latest_model --no-postgres
    
    - name: Upload results
      uses: actions/upload-artifact@v3
      with:
        name: analysis-results
        path: nf_auto_runs/analysis/
    
    - name: Check health score
      run: |
        python -c "
        import pandas as pd
        import sys
        df = pd.read_csv('nf_auto_runs/analysis/model_diagnosis_*.csv')
        score = df['overall_score'].iloc[0]
        if score < 60:
            print(f'⚠ Health score too low: {score}')
            sys.exit(1)
        "
"""
        return workflow
    
    @staticmethod
    def generate_gitlab_ci_config() -> str:
        """GitLab CIコンフィグを生成"""
        config = """
stages:
  - analyze
  - alert

analyze_models:
  stage: analyze
  image: python:3.10
  script:
    - pip install pandas numpy torch psycopg2-binary
    - python run_analysis.py models/latest_model
  artifacts:
    paths:
      - nf_auto_runs/analysis/
    expire_in: 1 week
  only:
    - schedules
    - pushes

check_health:
  stage: alert
  image: python:3.10
  script:
    - python check_model_health.py
  only:
    - schedules
"""
        return config


def create_scheduled_task_windows(script_path: str, schedule_time: str = "00:00"):
    """Windowsタスクスケジューラーにタスクを作成"""
    task_name = "NeuralForecastModelAnalysis"
    
    # PowerShellスクリプトを生成
    ps_script = f"""
$action = New-ScheduledTaskAction -Execute "python" -Argument "{script_path}"
$trigger = New-ScheduledTaskTrigger -Daily -At {schedule_time}
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
Register-ScheduledTask -TaskName "{task_name}" -Action $action -Trigger $trigger -Settings $settings -Description "NeuralForecast model analysis"
"""
    
    print("Windowsタスクスケジューラー登録コマンド:")
    print(ps_script)
    
    return ps_script


def create_cron_job_linux(script_path: str, schedule: str = "0 0 * * *"):
    """Linux cronジョブを作成"""
    cron_entry = f"{schedule} cd {Path(script_path).parent} && python {Path(script_path).name} >> automation.log 2>&1"
    
    print("cron設定:")
    print(f"  crontab -e")
    print(f"  {cron_entry}")
    
    return cron_entry


def setup_automation():
    """自動化セットアップ"""
    print("\n" + "="*80)
    print("自動化セットアップウィザード")
    print("="*80)
    
    config = AutomationConfig()
    
    # 1. 監視ディレクトリ設定
    print("\n[1/4] 監視するモデルディレクトリを設定")
    while True:
        model_dir = input("  モデルディレクトリ（空でスキップ）: ").strip()
        if not model_dir:
            break
        config.config['models']['watch_directories'].append(model_dir)
    
    # 2. アラート設定
    print("\n[2/4] アラート設定")
    enable_alerts = input("  アラートを有効化しますか？ (y/n): ").strip().lower() == 'y'
    config.config['alerts']['enabled'] = enable_alerts
    
    if enable_alerts:
        print("  メール設定:")
        config.config['alerts']['email']['sender_email'] = input("    送信元メール: ").strip()
        config.config['alerts']['email']['sender_password'] = input("    パスワード: ").strip()
        recipients = input("    受信者メール（カンマ区切り）: ").strip()
        config.config['alerts']['email']['recipients'] = [r.strip() for r in recipients.split(',')]
    
    # 3. 健全性スコア閾値
    print("\n[3/4] 監視設定")
    threshold = input("  健全性スコア閾値（デフォルト: 60）: ").strip()
    if threshold:
        config.config['monitoring']['health_score_threshold'] = int(threshold)
    
    # 4. スケジュール設定
    print("\n[4/4] スケジュール設定")
    print("  スケジュール実行方法を選択:")
    print("    1. Windows タスクスケジューラー")
    print("    2. Linux cron")
    print("    3. GitHub Actions")
    print("    4. スキップ")
    
    choice = input("  選択 (1-4): ").strip()
    
    if choice == '1':
        schedule_time = input("  実行時刻（HH:MM, デフォルト: 00:00）: ").strip() or "00:00"
        script_path = str(Path(__file__).parent / "scheduled_analysis.py")
        create_scheduled_task_windows(script_path, schedule_time)
    
    elif choice == '2':
        schedule = input("  cronスケジュール（デフォルト: 0 0 * * *）: ").strip() or "0 0 * * *"
        script_path = str(Path(__file__).parent / "scheduled_analysis.py")
        create_cron_job_linux(script_path, schedule)
    
    elif choice == '3':
        workflow = CIIntegration.generate_github_actions_workflow()
        workflow_path = Path(".github/workflows/model_analysis.yml")
        workflow_path.parent.mkdir(parents=True, exist_ok=True)
        with open(workflow_path, 'w') as f:
            f.write(workflow)
        print(f"  ✓ GitHub Actionsワークフロー作成: {workflow_path}")
    
    # 設定を保存
    config.save_config()
    
    print("\n✓ セットアップ完了")


def run_scheduled_analysis():
    """スケジュール実行用のメイン関数"""
    config = AutomationConfig()
    monitor = ModelMonitor(config)
    
    # ログファイルの設定
    log_file = config.config['logging']['log_file']
    Path(log_file).parent.mkdir(parents=True, exist_ok=True)
    
    # ログに記録
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n{'='*80}\n")
        f.write(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"{'='*80}\n")
    
    # 監視実行
    results = monitor.monitor_models()
    
    # ログに記録
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"分析完了: {len(results)} モデル\n")


# メイン実行
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='NeuralForecast 自動化システム')
    
    parser.add_argument('command', choices=['setup', 'run', 'monitor'],
                       help='実行するコマンド')
    
    args = parser.parse_args()
    
    if args.command == 'setup':
        setup_automation()
    
    elif args.command == 'run':
        run_scheduled_analysis()
    
    elif args.command == 'monitor':
        config = AutomationConfig()
        monitor = ModelMonitor(config)
        monitor.monitor_models()
