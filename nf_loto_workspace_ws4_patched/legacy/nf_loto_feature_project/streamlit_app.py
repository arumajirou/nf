import os
import io
import zipfile
import inspect
import streamlit as st

import pandas as pd

PROJECT_ROOT = os.path.dirname(__file__)

st.set_page_config(page_title="NF Loto Feature Project", layout="wide")

st.title("NeuralForecast Loto 特徴量プロジェクト WebUI")

st.markdown("""
このアプリから、以下の操作を行えます。

* 実行環境・ディレクトリ構造の確認
* プロジェクト内ファイルの閲覧・編集
* 特徴量生成スクリプトの実行 (loto_feature_builder.py)
* PostgreSQL に保存されたテーブルの簡易確認
* プロジェクト一式の zip ダウンロード
""")

# タブ構成
tab_env, tab_files, tab_run, tab_db, tab_zip = st.tabs(
    ["環境情報", "ファイル閲覧/編集", "特徴量生成実行", "テーブル確認", "zip ダウンロード"]
)

with tab_env:
    st.header("1. 実行環境情報")
    st.write("Python バージョン:", os.sys.version)
    try:
        import torch
        st.write("PyTorch:", torch.__version__)
        st.write("CUDA available:", torch.cuda.is_available())
    except Exception as e:
        st.write("PyTorch はインポートできませんでした:", e)

    st.subheader("ディレクトリ構造")
    tree_lines = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        level = root.replace(PROJECT_ROOT, "").count(os.sep)
        indent = " " * 2 * level
        tree_lines.append(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for f in files:
            tree_lines.append(f"{subindent}{f}")
    st.code("\n".join(tree_lines), language="text")

with tab_files:
    st.header("2. ファイル閲覧 / 編集")

    # プロジェクト内のテキストファイル一覧
    text_files = []
    for root, dirs, files in os.walk(PROJECT_ROOT):
        for f in files:
            if f.endswith((".py", ".md", ".txt", ".ipynb", ".json", ".yml", ".yaml")):
                rel = os.path.relpath(os.path.join(root, f), PROJECT_ROOT)
                text_files.append(rel)
    text_files = sorted(text_files)

    if not text_files:
        st.info("テキストファイルが見つかりません。")
    else:
        selected = st.selectbox("ファイルを選択", text_files)
        path = os.path.join(PROJECT_ROOT, selected)
        if selected.endswith(".ipynb"):
            st.write("ipynb は JSON として表示します。")
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        edited = st.text_area("内容", content, height=400, key="editor")
        if st.button("保存", key="save_btn"):
            with open(path, "w", encoding="utf-8") as f:
                f.write(edited)
            st.success("保存しました。")

with tab_run:
    st.header("3. 特徴量生成スクリプト実行")

    st.markdown("`loto_feature_builder.py` を実行して特徴量テーブルを更新します。")

    if st.button("実行", key="run_builder"):
        import subprocess
        import sys
        cmd = [sys.executable, "loto_feature_builder.py"]
        st.write("実行コマンド:", " ".join(cmd))
        try:
            proc = subprocess.run(cmd, cwd=PROJECT_ROOT,
                                  capture_output=True, text=True, check=False)
            st.subheader("標準出力")
            st.code(proc.stdout)
            st.subheader("標準エラー")
            st.code(proc.stderr)
            st.write("return code:", proc.returncode)
        except Exception as e:
            st.error(f"実行中にエラー: {e}")

with tab_db:
    st.header("4. テーブル確認 (PostgreSQL)")
    st.write("db_config.py の設定に従って PostgreSQL に接続します。")

    from db_config import DB_CONFIG
    import psycopg2

    try:
        conn = psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        st.error(f"DB 接続エラー: {e}")
        conn = None

    if conn is not None:
        with conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT tablename
                    FROM pg_catalog.pg_tables
                    WHERE schemaname NOT IN ('pg_catalog', 'information_schema')
                      AND tablename LIKE 'nf_loto%'
                    ORDER BY tablename
                """)
                rows = cur.fetchall()
        tables = [r[0] for r in rows]
        st.write("nf_loto 系テーブル:", tables)

        target = st.selectbox("確認するテーブル", ["(選択してください)"] + tables)
        if target != "(選択してください)":
            limit = st.number_input("取得件数", min_value=1, max_value=1000, value=20)
            with conn:
                df = pd.read_sql(f"SELECT * FROM {target} ORDER BY 1 LIMIT %s", conn, params=(int(limit),))
            st.dataframe(df)

with tab_zip:
    st.header("5. プロジェクト一式 zip ダウンロード")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(PROJECT_ROOT):
            for f in files:
                full = os.path.join(root, f)
                rel = os.path.relpath(full, PROJECT_ROOT)
                zf.write(full, rel)
    buf.seek(0)
    st.download_button(
        label="nf_loto_feature_project.zip をダウンロード",
        data=buf,
        file_name="nf_loto_feature_project.zip",
        mime="application/zip",
    )
