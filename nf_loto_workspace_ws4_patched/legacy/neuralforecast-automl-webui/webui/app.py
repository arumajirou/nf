"""
NeuralForecast AutoML WebUI - メインアプリケーション

Streamlitベースの時系列予測モデル自動最適化WebUI
"""

import streamlit as st
import sys
import os
from pathlib import Path

# プロジェクトルートをPythonパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# ページ設定（最初に実行）
st.set_page_config(
    page_title="NeuralForecast AutoML",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/neuralforecast-automl-webui',
        'Report a bug': 'https://github.com/your-repo/neuralforecast-automl-webui/issues',
        'About': '# NeuralForecast AutoML WebUI\n時系列予測モデルの自動最適化システム'
    }
)

# カスタムCSS
st.markdown("""
<style>
/* メインコンテンツ */
.main {
    padding: 1rem;
}

/* メトリクスカード */
.metric-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 20px;
    border-radius: 10px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.metric-value {
    font-size: 36px;
    font-weight: bold;
    margin: 10px 0;
}

.metric-label {
    font-size: 14px;
    opacity: 0.9;
}

/* ステータスバッジ */
.status-badge {
    padding: 5px 10px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: bold;
    display: inline-block;
}

.status-running {
    background-color: #17a2b8;
    color: white;
}

.status-completed {
    background-color: #28a745;
    color: white;
}

.status-failed {
    background-color: #dc3545;
    color: white;
}

.status-pending {
    background-color: #6c757d;
    color: white;
}

/* プログレスバー */
.progress-container {
    width: 100%;
    height: 30px;
    background-color: #e9ecef;
    border-radius: 15px;
    overflow: hidden;
    margin: 10px 0;
}

.progress-bar {
    height: 100%;
    background: linear-gradient(90deg, #4e73df 0%, #1cc88a 100%);
    transition: width 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
}

/* ボタン */
.stButton>button {
    width: 100%;
    border-radius: 5px;
    padding: 10px;
    font-weight: bold;
}

/* サイドバー */
.css-1d391kg {
    padding-top: 2rem;
}

/* データフレーム */
.dataframe {
    font-size: 12px;
}

/* エクスパンダー */
.streamlit-expanderHeader {
    font-weight: bold;
    font-size: 16px;
}

/* アラート */
.stAlert {
    padding: 1rem;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# セッション状態の初期化
def init_session_state():
    """セッション状態の初期化"""
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        st.session_state.current_experiment = None
        st.session_state.current_run = None
        st.session_state.uploaded_dataset = None
        st.session_state.config = {}
        st.session_state.training_active = False
        st.session_state.monitoring_active = False

init_session_state()

# サイドバー
with st.sidebar:
    st.title("🚀 NeuralForecast AutoML")
    st.markdown("---")
    
    # ナビゲーション
    st.subheader("📌 Navigation")
    
    # システム状態
    st.markdown("---")
    st.subheader("💻 System Status")
    
    # 簡易リソース表示
    import psutil
    
    cpu_percent = psutil.cpu_percent(interval=0.1)
    mem = psutil.virtual_memory()
    
    st.metric("CPU Usage", f"{cpu_percent:.1f}%")
    st.metric("RAM Usage", f"{mem.percent:.1f}%")
    st.metric("Available RAM", f"{mem.available / (1024**3):.1f} GB")
    
    # GPU情報（利用可能な場合）
    try:
        import GPUtil
        gpus = GPUtil.getGPUs()
        if gpus:
            gpu = gpus[0]
            st.metric("GPU Usage", f"{gpu.load * 100:.1f}%")
            st.metric("VRAM Usage", f"{gpu.memoryUtil * 100:.1f}%")
    except:
        pass
    
    st.markdown("---")
    
    # クイックアクション
    st.subheader("⚡ Quick Actions")
    
    if st.button("🆕 New Experiment"):
        st.session_state.current_experiment = None
        st.switch_page("pages/2_📤_Data_Upload.py")
    
    if st.button("📊 View Results"):
        st.switch_page("pages/5_📈_Results.py")
    
    if st.button("📜 History"):
        st.switch_page("pages/6_📜_History.py")
    
    st.markdown("---")
    
    # 設定
    with st.expander("⚙️ Settings"):
        st.selectbox("Theme", ["Light", "Dark", "Auto"])
        st.checkbox("Enable notifications", value=True)
        st.checkbox("Auto-save experiments", value=True)
    
    # フッター
    st.markdown("---")
    st.caption("Version 1.0.0")
    st.caption("© 2025 NeuralForecast AutoML")

# メインコンテンツ
st.title("🏠 Dashboard")
st.markdown("### Welcome to NeuralForecast AutoML WebUI")

# 概要説明
st.info("""
**NeuralForecast AutoML** は、時系列予測モデルの自動ハイパーパラメータ最適化を
直感的なWebインターフェースで実現するシステムです。

**主な機能:**
- 📤 データアップロード・管理
- ⚙️ モデル設定・パラメータ選択
- 🚀 リアルタイム実行監視
- 💻 リソースモニタリング
- 📊 実験履歴管理
- 📈 予測結果可視化
""")

# クイックスタートガイド
st.markdown("### 🚀 Quick Start Guide")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    #### 1️⃣ データアップロード
    CSVまたはParquetファイルをアップロード
    - 必須カラム: `unique_id`, `ds`, `y`
    - オプション: 外生変数
    """)
    if st.button("📤 Upload Data →", key="upload_btn"):
        st.switch_page("pages/2_📤_Data_Upload.py")

with col2:
    st.markdown("""
    #### 2️⃣ モデル設定
    モデルとパラメータを選択
    - Quick/Standard/Advanced モード
    - 28種類のモデル対応
    """)
    if st.button("⚙️ Configure Model →", key="config_btn"):
        st.switch_page("pages/3_⚙️_Model_Config.py")

with col3:
    st.markdown("""
    #### 3️⃣ 学習実行
    最適化を開始して結果を確認
    - リアルタイム進捗監視
    - リソース使用状況可視化
    """)
    if st.button("🚀 Start Training →", key="train_btn"):
        st.switch_page("pages/4_🚀_Training.py")

st.markdown("---")

# 最近の実験
st.markdown("### 📊 Recent Experiments")

# ダミーデータ（実際はデータベースから取得）
recent_experiments_data = {
    "Name": ["NHITS_experiment_1", "TFT_forecast_2", "DLinear_test_3"],
    "Model": ["NHITS", "TFT", "DLinear"],
    "Status": ["Running", "Completed", "Failed"],
    "Progress": [70, 100, 0],
    "Duration": ["8m 34s", "15m 22s", "2m 10s"],
    "Best Loss": [0.234, 0.189, None]
}

import pandas as pd
df = pd.DataFrame(recent_experiments_data)

# ステータスに応じた色分け
def style_status(val):
    if val == "Running":
        return 'background-color: #17a2b8; color: white'
    elif val == "Completed":
        return 'background-color: #28a745; color: white'
    elif val == "Failed":
        return 'background-color: #dc3545; color: white'
    return ''

styled_df = df.style.applymap(style_status, subset=['Status'])
st.dataframe(styled_df, use_container_width=True, hide_index=True)

# 統計情報
st.markdown("---")
st.markdown("### 📈 Statistics")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        label="Total Experiments",
        value="42",
        delta="+5 this week"
    )

with col2:
    st.metric(
        label="Running",
        value="3",
        delta="+1"
    )

with col3:
    st.metric(
        label="Completed Today",
        value="5",
        delta="+2"
    )

with col4:
    st.metric(
        label="Avg. Training Time",
        value="12.5 min",
        delta="-1.5 min"
    )

# フッター
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Need help? Check out the <a href='#'>User Guide</a> or <a href='#'>API Reference</a></p>
</div>
""", unsafe_allow_html=True)
