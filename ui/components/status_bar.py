# ClipboardTranslator v1.10 - StatusBar Component
"""
ステータスバーUIコンポーネント
"""
import tkinter as tk
from typing import Optional, Callable
from config.constants import MESSAGES
from config.settings import config


class StatusBar(tk.Frame):
    """ステータスバーコンポーネント"""

    def __init__(self, parent: tk.Widget, **kwargs):
        """
        初期化

        Parameters:
            parent: 親ウィジェット
        """
        super().__init__(parent, **kwargs)

        # ステータスラベル
        self.status_label = tk.Label(
            self,
            text="待機中...",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.pack(fill=tk.X)

        # 自動リセット用のタイマーID
        self._reset_timer_id: Optional[str] = None

    def _get_message(self, key: str, **kwargs) -> str:
        """設定された言語に基づいてメッセージを取得"""
        response_language = config.get('Settings', 'response_language', fallback='JA')
        message = MESSAGES.get(response_language, MESSAGES['JA']).get(key, key)

        if kwargs:
            message = message.format(**kwargs)

        return message

    def update(self, message_key: str, duration: int = 3000, **kwargs) -> None:
        """
        ステータスバーのメッセージを更新

        Parameters:
            message_key: メッセージキーまたは直接のメッセージ文字列
            duration: メッセージ表示時間（ミリ秒）。0の場合は自動リセットしない
            **kwargs: メッセージのフォーマット用パラメータ
        """
        # 既存のタイマーをキャンセル
        if self._reset_timer_id:
            self.after_cancel(self._reset_timer_id)
            self._reset_timer_id = None

        # メッセージを取得（キーが存在しない場合は直接文字列として使用）
        if message_key in MESSAGES.get('JA', {}) or message_key in MESSAGES.get('EN', {}):
            message = self._get_message(message_key, **kwargs)
        else:
            message = message_key

        self.status_label.config(text=message)

        # 自動リセットの設定
        if duration > 0:
            waiting_msg = self._get_message('waiting')
            self._reset_timer_id = self.after(
                duration,
                lambda: self.status_label.config(text=waiting_msg)
            )

    def set_text(self, text: str) -> None:
        """
        ステータスバーのテキストを直接設定（自動リセットなし）

        Parameters:
            text: 表示するテキスト
        """
        # 既存のタイマーをキャンセル
        if self._reset_timer_id:
            self.after_cancel(self._reset_timer_id)
            self._reset_timer_id = None

        self.status_label.config(text=text)
