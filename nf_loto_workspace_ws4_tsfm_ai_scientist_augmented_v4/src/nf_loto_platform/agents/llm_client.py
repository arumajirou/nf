from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


class BaseLLMClient(ABC):
    """LLM 呼び出しを抽象化する最小限のインターフェイス.

    実装側では OpenAI / Azure / ローカル LLM などを隠蔽する。
    テストでは EchoLLMClient を使うことで外部依存を避ける。
    """

    @abstractmethod
    def generate(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:  # noqa: D401
        """LLM から 1 つのテキスト応答を生成する。"""
        raise NotImplementedError


@dataclass
class EchoLLMClient(BaseLLMClient):
    """テスト用の簡易 LLM クライアント.

    入力プロンプトを要約した固定形式の文字列を返すだけで、
    外部 API を一切呼ばない。
    """

    max_chars: int = 512

    def generate(self, system_prompt: str, user_prompt: str, **kwargs: Any) -> str:  # noqa: D401
        """system + user を結合して先頭 max_chars だけ返す。"""
        combined = f"[SYSTEM]{system_prompt}\n[USER]{user_prompt}"
        if len(combined) > self.max_chars:
            combined = combined[: self.max_chars] + "..."
        return combined
