# ClipboardTranslator v1.10 - ChatPanel Component
"""
チャット入力パネルUIコンポーネント
"""
import tkinter as tk
from typing import Callable, Optional
from config.constants import get_message
from config.settings import config


class ChatPanel(tk.Frame):
    """開閉可能なチャット入力パネルコンポーネント"""

    def __init__(
        self,
        parent: tk.Widget,
        on_send: Callable[[str], None],
        **kwargs
    ):
        """
        初期化

        Parameters:
            parent: 親ウィジェット
            on_send: メッセージ送信時のコールバック(message: str)
        """
        super().__init__(parent, **kwargs)

        self._on_send = on_send
        self._panel_visible = False

        # トグルボタン用フレーム（常に表示）
        self._toggle_frame = tk.Frame(self, bg='#404040')
        self._toggle_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self._toggle_btn = tk.Button(
            self._toggle_frame,
            text=self._get_message('chat_toggle'),
            command=self.toggle,
            bg='#404040',
            fg='#ffffff',
            activebackground='#505050',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            cursor='hand2',
            font=('Yu Gothic UI', 9)
        )
        self._toggle_btn.pack(fill=tk.X, pady=2)

        # 会話パネルのコンテナ（最初は非表示）
        self._panel_frame = tk.Frame(self, bg='#2a2a2a')

        # 入力エリア
        self._input_frame = tk.Frame(self._panel_frame, bg='#2a2a2a')
        self._input_frame.pack(fill=tk.X, padx=5, pady=5)

        # 入力テキストボックス（絵文字対応フォント）
        self._input_text = tk.Text(
            self._input_frame,
            height=3,
            wrap=tk.WORD,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='#ffffff',
            font=('Segoe UI Emoji', 10),
            relief=tk.FLAT,
            padx=8,
            pady=5
        )
        self._input_text.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self._input_text.bind('<Return>', self._on_enter)
        self._input_text.bind('<Shift-Return>', self._on_newline)

        # 送信ボタン
        self._send_btn = tk.Button(
            self._input_frame,
            text=self._get_message('chat_send'),
            command=self._send,
            bg='#4a7c59',
            fg='#ffffff',
            activebackground='#5a8c69',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            cursor='hand2',
            font=('Yu Gothic UI', 9),
            width=6
        )
        self._send_btn.pack(side=tk.RIGHT, padx=(5, 0))

    def _get_message(self, key: str, **kwargs) -> str:
        """設定された言語に基づいてメッセージを取得"""
        response_language = config.get('Settings', 'response_language', fallback='EN')
        return get_message(key, response_language, **kwargs)

    def toggle(self) -> None:
        """パネルの表示/非表示を切り替える"""
        if self._panel_visible:
            self._panel_frame.pack_forget()
            self._toggle_btn.config(text=self._get_message('chat_toggle'))
            self._panel_visible = False
        else:
            self._panel_frame.pack(side=tk.BOTTOM, fill=tk.X, before=self._toggle_frame)
            self._toggle_btn.config(text=self._get_message('chat_toggle_close'))
            self._panel_visible = True
            self._input_text.focus_set()

    @property
    def is_visible(self) -> bool:
        """パネルが表示中かどうか"""
        return self._panel_visible

    def _on_enter(self, event) -> str:
        """Enterキーで送信"""
        self._send()
        return 'break'

    def _on_newline(self, event) -> Optional[str]:
        """Shift+Enterで改行"""
        return None

    def _send(self) -> None:
        """メッセージを送信"""
        message = self._input_text.get("1.0", tk.END).strip()
        if not message:
            return

        self._input_text.delete("1.0", tk.END)
        self._on_send(message)

    def clear_input(self) -> None:
        """入力欄をクリア"""
        self._input_text.delete("1.0", tk.END)

    def focus_input(self) -> None:
        """入力欄にフォーカス"""
        self._input_text.focus_set()
