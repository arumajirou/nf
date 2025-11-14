1. run_spec

```json
{
  "dataset": {
    "path": "remote:loto-life.net/csv/*",
    "freq": null,
    "n_series": null,
    "y_col": null,
    "id_col": null,
    "ds_col": "ds",
    "exogenous": {
      "known_in_advance": [],
      "observed": [],
      "static": []
    },
    "missing_handling": "none",
    "scaler": "none",
    "seasonality": null
  },
  "task": {
    "model": "AutoTFT",
    "h": 0,
    "loss": "mse",
    "metric": "val_smape",
    "seed": 1029
  },
  "tuning": {
    "backend": "none",
    "trials": 0,
    "time_budget_min": null,
    "sampler": "random",
    "early_stop": false,
    "space_preset": "custom",
    "space_overrides": {}
  },
  "validation": {
    "cv": "single",
    "folds": 1,
    "test_size": 0,
    "gap": 0,
    "stride": 1
  },
  "resources": {
    "num_cpus": 2,
    "num_gpus": 0,
    "memory_gb": null
  },
  "logging": {
    "mlflow": {
      "enabled": false,
      "tracking_uri": null,
      "experiment": null,
      "run_name": null,
      "tags": {}
    }
  },
  "paths": {
    "artifacts_root": "nf_auto_runs/",
    "logs_dir": "nf_auto_runs/logs"
  },
  "reporting": {
    "summary_csv": "nf_auto_runs/auto_run_summary.csv",
    "return_columns": [
      "auto_model",
      "backend",
      "status",
      "seconds",
      "best_metric",
      "h",
      "freq"
    ]
  },
  "proposed_env": {}
}
```

2. env_exports

```bash
# このロトETL処理では必須の環境変数は特にありません
```

3. command

```bash
python loto_pg_store.py
```

4. notes

ここからが本題です。
C:\nf 配下の **loto_feature_system_v2 の db フォルダ**で、ロトのCSVを取り込んで PostgreSQL に保存する一連の処理はだいたい次のような流れになっています。

---

### 全体像（ざっくり）

1. `db_config.py` に PostgreSQL の接続情報＆テーブル名プレフィックスを定義。
2. `setup_postgres.py` で接続テストと既存 `nf_` テーブルの整理。
3. `loto_etl.py` で loto-life の CSV を取得して、きれいな縦長 DataFrame に整形。
4. `loto_pg_store.py` で、その DataFrame を `nf_loto_final` テーブルに UPSERT（挿入 or 更新）。
5. 必要なら `postgres_manager.py` で NeuralForecast のパラメータ用テーブルなども作れる。

以下、順番に「何が起きるか」を手順形式で説明します。

---

## 手順0: 接続設定ファイル `db_config.py`

**何をしているファイルか**

* PostgreSQL への接続情報を 1 箇所にまとめた設定モジュール。

主な中身:

* `DB_CONFIG`

  * host: `127.0.0.1`
  * port: `5432`
  * database: `postgres`
  * user: `postgres`
  * password: `'z'` （ここは自分の環境に合わせて書き換える前提）
* `TABLE_PREFIX = "nf_"`

  * すべての「このプロジェクトで作るテーブル名」は `nf_` から始めるルール。
* `PYTHON_TO_PG_TYPE`

  * `int -> INTEGER`, `float -> REAL`, `str -> TEXT`, `list/dict -> JSONB` みたいな、Python の型から PostgreSQL の型へのマッピング。

**ここでやる作業**

1. PostgreSQL を自分の環境にインストール・起動。
2. `db_config.py` の `database`, `user`, `password` を自分の環境に合わせて修正。
3. 以降のスクリプトはすべてこの設定を共有して使います。

---

## 手順1: PostgreSQL の接続テスト & 既存テーブル整理 `setup_postgres.py`

このスクリプトはコマンドラインからいくつかのモードで動きます。

### 1-1. 接続テストだけしたい場合

コマンド例（`db` フォルダで）:

```bash
python setup_postgres.py test
```

処理の流れ:

1. `db_config.DB_CONFIG` を使って接続情報を表示。
2. `PostgreSQLManager` を使って実際に接続。
3. `SELECT version()` を実行して、PostgreSQL のバージョンを表示。
4. 失敗したら例外メッセージと「サービス起動してる？」「db_config 合ってる？」などのトラブルシュートヒントを表示。

### 1-2. `nf_` テーブルの状態を確認したい場合

```bash
python setup_postgres.py info
```

処理の流れ:

1. 接続。
2. `PostgreSQLManager.list_tables()` で `public` スキーマのテーブル一覧を取得。
3. その中から `nf_` で始まるテーブルだけに絞る。
4. 各テーブルについて:

   * `get_table_info()` でカラム名・型・長さ・NULL許可などを DataFrame で取得し表示。
   * `SELECT COUNT(*)` でレコード数も出す。

### 1-3. フルセットアップ（既存 nf_ テーブルの削除を含む）

```bash
python setup_postgres.py setup
# 引数なしで python setup_postgres.py でも同じ
```

処理の流れ:

1. 接続情報を表示 → 接続テスト。
2. 既存テーブル一覧を取得。
3. その中に `nf_` で始まるテーブルがあれば一覧表示して、
   「削除しますか？ (y/N)」と聞かれる。
4. `y` と答えた場合:

   * 各 `nf_` テーブルに対して `DROP TABLE IF EXISTS ... CASCADE` を実行。
   * コミットして「削除完了」と表示。
5. スキップした場合は何も削除せず、「新規セットアップ準備完了」と出る。
6. 最後に「次のステップ」として

   * `db_config.py を確認・編集`
   * `neuralforecast_extractor_postgres.py を実行`
     などの案内が表示される。

---

## 手順2: ロト CSV を整形する `loto_etl.py`

このモジュールが「CSV → キレイな DataFrame」部分を全部担当しています。

### 2-1. どこからデータを取ってくるか

`URLS` に、ロト系の CSV URL が列挙されています:

* mini / loto6 / loto7 / bingo5 / numbers3 / numbers4

`numbers3` と `numbers4` だけは `NAME_MAP` で `num3`, `num4` に置き換えて、
`loto` 列に入る省略名にしています。

### 2-2. CSV の読み込み

* `_read_csv_jp(u)`

  * `cp932` → `sjis` → `utf-8` の順でエンコーディングを試しながら `pd.read_csv`。
  * 全部だめなら最後にデフォルトで再チャレンジ。

### 2-3. 日付列・番号列の標準化

* `_rename_core_columns(df)` の中で:

  1. 列名を全部文字列化＆strip（`_normalize_columns`）。
  2. 「開催日」or「抽選日」を探して、見つかったらその列名を `ds` に変更。
  3. `ds` 列の中身から「(何回目)」みたいなカッコ書きを削除して、

     * 「YYYY年MM月DD日」→「YYYY-MM-DD」
     * 「YYYY/MM/DD」→「YYYY-MM-DD」
       のように正規化して `pd.to_datetime` で日時型にする。
  4. 列名が

     * `第1数字` → `N1`
     * `1等口数` → `N1NU`
     * `1等賞金` → `N1PM`
       のようなルールで `N*`, `N*NU`, `N*PM` へ自動リネーム。

### 2-4. ワイド形式 → ロング形式

* `_melt_numbers_long(df, loto_name)`

  1. `N1, N2, ...` だけを全部集めて番号順にソート。
  2. それ以外の列を `id_vars` として `pandas.melt` で縦持ちに変換。
  3. `var_name="unique_id"`（例: `"N1"`）, `value_name="y"`（実際の数字）にする。
  4. ついでに `loto` 列に「mini」「loto6」などの名前を入れておく。

* `build_long_dataframe(urls)`

  * すべての URL について上の処理を回し、縦持ち DataFrame を `concat`。
  * 列の並びを
    `["loto", "開催回", "ds", "unique_id", "y", その他...]`
    のようにそろえる。

### 2-5. 型を整えて最終形にする

* `finalize_df(df)`

  1. `開催回` → 整数化して `num` 列にコピー。元の `開催回` は後で削除。
  2. `キャリーオーバー` → 整数化して `CO` 列にコピー。
  3. `y`（当選数字）も int64 に統一。
  4. `loto`, `ds`, `unique_id`, `num`, `CO`, `y` 以外の列も、
     文字列や日付を除いて基本的に全部 int64 にそろえる。
  5. `ボーナス数字`, `ボーナス数字1`, `ボーナス数字2`, `キャリーオーバー`, `開催回` など
     後から不要になる列を削除。
  6. 列の順番を
     `["loto", "num", "ds", "unique_id", "y", "CO", ...その他]`
     に整えて返す。

* `build_df_final(urls=None)`

  * 上記を全部まとめて呼び出す「外部向けの入口」関数。
  * 何も渡さないと `URLS` 全部を処理して最終 DataFrame を返す。

---

## 手順3: PostgreSQL に保存する `loto_pg_store.py`

このモジュールが「最終 DataFrame → PostgreSQL」の担当です。

### 3-1. テーブル定義

* `TABLE_NAME = f"{TABLE_PREFIX}loto_final"`
  → 例: `nf_loto_final`。

* `COLS` で列の順番を定義:

  * `loto`, `num`, `ds`, `unique_id`, `y`, `CO`
  * `N1NU`, `N1PM`, ..., `N7NU`, `N7PM`

* `CREATE_SQL` でテーブル作成SQLを定義:

  * 上記のカラムを `BIGINT` / `TIMESTAMP` / `TEXT` で定義。
  * 主キーは `(loto, num, unique_id)`。
  * 検索用のインデックス:

    * `(ds)`
    * `(loto, ds)`
    * `(loto, num)`

### 3-2. 行データの準備 `_prepare_rows`

`upsert_df` から使われます。

1. 渡された DataFrame をコピー。
2. `COLS` に含まれる列で、DataFrame に存在しないものは作っておく

   * 日付列 `ds` 以外は 0 埋め。
3. `loto`, `unique_id`, `ds` 以外の列は

   * `pd.to_numeric(..., errors="coerce").fillna(0).astype("int64")`
     で全部整数にそろえる。
4. `ds` は `pd.to_datetime` で datetime 型に。
5. 最後に `data[COLS]` の順番に並べ直し、
   `NaN` を `None` に変換してタプルのリストにする
   （`execute_values` 用の形）。

### 3-3. UPSERT 本体 `upsert_df(df, batch_size=5000)`

処理の流れ:

1. `if df.empty: return 0` 空なら何もしない。

2. `ensure_table()` で `CREATE TABLE IF NOT EXISTS ...` を実行し、テーブルがなければ作る。

3. その後 `migrate_to_bigint()` を呼んで、既存の `INTEGER` カラムがあれば `BIGINT` に変更。

4. `_prepare_rows(df)` でタプルのリストを作る。

5. 接続を開いて、`batch_size` ごとに `execute_values` で
   `UPSERT_SQL_TEMPLATE` を実行:

   * `INSERT INTO nf_loto_final (...) VALUES %s`
   * `ON CONFLICT (loto, num, unique_id) DO UPDATE SET ...`
   * つまり

     * まだ存在しない組み合わせ → 新規 INSERT
     * すでにある組み合わせ → `ds`, `y`, `CO`, その他のカラムを UPDATE

6. 全チャンクを処理したら `commit()` して、処理した行数を返す。

### 3-4. 便利な CRUD 関数

* `read_by_loto_num(loto, num)`

  * ある回の結果だけを `SELECT` して dict のリストで返す。
* `read_by_date_range(loto, start, end)`

  * 期間指定で検索。`loto=None` なら全銘柄横断。
* `update_y(loto, num, unique_id, y)`

  * 特定の数字だけ `UPDATE`。
* `delete_by_loto_num(loto, num)`

  * ある回を丸ごと `DELETE`。

### 3-5. スクリプトとして実行したとき

`loto_pg_store.py` を直接実行した場合の `__main__` 部分:

1. `from loto_etl import build_df_final` をインポート。
2. `df_final = build_df_final()`

   * 手順2のETLを全部実行して、最終DataFrameを作る。
3. `n = upsert_df(df_final, batch_size=5000)`

   * 5000行ずつバルクUPSERT。
4. `print(f"UPSERT行数: {n}")` で処理した行数を表示。

---

## 手順4: 汎用の PostgreSQL マネージャ `postgres_manager.py`

こちらは「ロトの当選データ」よりも、NeuralForecast のパラメータなどを
カテゴリごとにテーブル化して保存するためのユーティリティです。

ざっくり役割:

* 接続管理（`connect`, `disconnect`, `__enter__`, `__exit__`）
* カテゴリ名 → テーブル名、パラメータ名 → カラム名への安全な変換

  * プレフィックスを削除
  * 小文字化
  * 記号を `_` にする
  * 長すぎる名前は切り詰める
* 値の型から PostgreSQL の型を推測（`infer_pg_type`）
* DataFrame（Category, Parameter, Value, Source）を受け取って:

  1. カテゴリごとにテーブルを作る（`create_table_from_category`）
  2. 1行分のデータ＋各パラメータの Source 情報を JSONB で保存（`insert_data_to_table`）
* `list_tables`, `get_table_info` で情報スキーマからメタデータを取得

`setup_postgres.py` の中ではこのクラスの `list_tables` / `get_table_info` を使っていました。

---

## 実際の作業フローのイメージ

C:\nf 配下でロトデータを Postgres に入れる典型的な手順はこんな感じになります:

1. **PostgreSQL を準備**

   * サービス起動、ユーザー・DB 作成。
   * `db_config.py` の `DB_CONFIG` を自分の環境に合わせて編集。

2. **接続確認＆不要テーブル掃除**

   * `cd C:\nf\loto_feature_system_v2\db`
   * `python setup_postgres.py test` で接続確認。
   * 必要なら `python setup_postgres.py setup` で既存 `nf_` テーブルを削除。

3. **ロトデータの取得＆保存**

   * `python loto_pg_store.py` を実行。
   * 内部で

     * loto-life の CSV を全部読み込む
     * きれいな縦長 DataFrame に整える
     * `nf_loto_final` テーブルを作成 or 更新
     * すべて UPSERT して行数を表示

4. **後からの利用**

   * Python から `read_by_loto_num`, `read_by_date_range` 等を使って分析用に読み出す。
   * 別プロジェクト（`sonnet` や `neuralforecast-automl-webui` 側）から、
     この `nf_loto_final` テーブルを時系列データとして使う想定の構成になっています。

---

ざっくりまとめると、「`setup_postgres.py` で PostgreSQL 側の掃除と接続確認 → `loto_etl.py` でロトのCSVをきれいに整形 → `loto_pg_store.py` で `nf_loto_final` にドンとUPSERT」という三段ロケットになっています。
