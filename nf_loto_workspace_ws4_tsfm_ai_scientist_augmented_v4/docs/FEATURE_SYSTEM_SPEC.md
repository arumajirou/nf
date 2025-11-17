# ロト特徴量生成システム仕様 (ダイジェスト)

* NeuralForecast の外生変数グループ:
  * `futr_` プレフィックス: 未来既知外生 (`futr_exog_list`)
  * `hist_` プレフィックス: 履歴外生 (`hist_exog_list`)
  * `stat_` プレフィックス: 静的外生 (`stat_exog_list`)
* 特徴量生成モジュール:
  * `features/futr_features.py`: 未来日付 + カレンダー特徴
  * `features/hist_features.py`: ラグ・ローリング統計 + 拡張余地
  * `features/stat_features.py`: 系列レベル統計
  * `features/y_representation.py`: y の異常スコア
  * `features/cleaning.py`: NaN / inf の除去
  * `features/gpu_utils.py`: GPU 検出・ワーカー数制御
  * `features/feature_config.py`: 各種設定の集中管理
  * `features/registry.py`: nf_feature_registry メタテーブル管理
* メインスクリプト:
  * `loto_feature_builder.py` が nf_loto_final を読み込み、
    各特徴量を生成して nf_loto_* テーブルに格納する。
