class ConfigError(Exception):
    """設定エラー。"""
    pass


class DataError(Exception):
    """データ整合性エラー。"""
    pass


class RunError(Exception):
    """実行時のラッパーエラー。"""
    pass
