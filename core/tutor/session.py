# ClipboardTranslator v1.00 - Tutor Session Management
# 会話セッション管理モジュール

from datetime import datetime
from typing import List, Dict, Optional
from config.constants import get_message
from config.settings import config


class TutorSession:
    """家庭教師会話セッションを管理するクラス"""

    def __init__(self, max_history: int = 10):
        """
        セッションを初期化

        Parameters:
            max_history: 保持する会話履歴の最大数
        """
        self.max_history = max_history
        self.conversation_history: List[Dict] = []
        self.session_start: Optional[datetime] = None
        self.is_active = False

    def start_session(self):
        """セッションを開始"""
        self.session_start = datetime.now()
        self.is_active = True
        self.conversation_history = []
        print(f"家庭教師セッション開始: {self.session_start}")

    def end_session(self):
        """セッションを終了"""
        self.is_active = False
        duration = None
        if self.session_start:
            duration = datetime.now() - self.session_start
        print(f"家庭教師セッション終了: 会話数={len(self.conversation_history)}, 時間={duration}")

    def add_message(self, role: str, content: str):
        """
        メッセージを履歴に追加

        Parameters:
            role: 'user' または 'assistant'
            content: メッセージ内容
        """
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now().isoformat()
        }
        self.conversation_history.append(message)

        # 最大履歴数を超えたら古いものを削除
        if len(self.conversation_history) > self.max_history * 2:
            self.conversation_history = self.conversation_history[-self.max_history * 2:]

    def get_context_messages(self, limit: int = 6) -> List[Dict]:
        """
        直近の会話コンテキストを取得

        Parameters:
            limit: 取得する最大メッセージ数

        Returns:
            直近の会話リスト
        """
        return self.conversation_history[-limit:]

    def format_context_for_prompt(self, limit: int = 6) -> str:
        """
        プロンプト用に会話コンテキストをフォーマット

        Parameters:
            limit: 取得する最大メッセージ数

        Returns:
            フォーマットされた会話履歴文字列
        """
        messages = self.get_context_messages(limit)
        if not messages:
            return ""

        formatted = []
        for msg in messages:
            lang = config.get("response_language", "EN")
            role_label = get_message("tutor_user_label", lang) if msg['role'] == 'user' else get_message("tutor_ai_label", lang)
            formatted.append(f"{role_label}: {msg['content']}")

        return "\n".join(formatted)

    def clear_history(self):
        """会話履歴をクリア"""
        self.conversation_history = []
        print("会話履歴をクリアしました")

    @property
    def message_count(self) -> int:
        """会話メッセージ数を取得"""
        return len(self.conversation_history)
