# ClipboardTranslator v1.10 - TextDisplay Component
"""
テキスト表示エリアUIコンポーネント
"""
import tkinter as tk
from typing import Callable, Optional
from config.constants import MESSAGES
from config.settings import config


class TextDisplay(tk.Text):
    """テキスト表示エリアコンポーネント"""

    # タグ定義
    TAGS = {
        'input_tag': '#9597f7',
        'translated_tag': '#9597f7',
        'dict_tag': '#95f797',
        'offline_tag': '#f7d195',
        'error_tag': '#ff6b6b',
        'speech_tag': '#f79595',
        'tutor_user_tag': '#87CEEB',
        'tutor_ai_tag': '#98FB98',
    }

    def __init__(self, parent: tk.Widget, on_font_size_change: Optional[Callable] = None, **kwargs):
        """
        初期化

        Parameters:
            parent: 親ウィジェット
            on_font_size_change: フォントサイズ変更時のコールバック(new_size: int)
        """
        super().__init__(
            parent,
            wrap=tk.WORD,
            bg='#333333',
            padx=12,
            pady=8,
            fg='white',
            font=('Segoe UI Emoji', 11),
            spacing1=2,
            spacing2=8,
            spacing3=8,
            **kwargs
        )

        self.configure(state='disabled')
        self._on_font_size_change = on_font_size_change
        self._last_font_change_time = 0

        # タグを設定
        for tag_name, color in self.TAGS.items():
            self.tag_configure(tag_name, foreground=color)

        # マウスホイールでフォントサイズ変更
        self.bind("<MouseWheel>", self._handle_mouse_wheel)

    def _get_message(self, key: str, **kwargs) -> str:
        """設定された言語に基づいてメッセージを取得"""
        response_language = config.get('Settings', 'response_language', fallback='JA')
        message = MESSAGES.get(response_language, MESSAGES['JA']).get(key, key)

        if kwargs:
            message = message.format(**kwargs)

        return message

    def _handle_mouse_wheel(self, event) -> Optional[str]:
        """マウスホイールでフォントサイズを変更（Ctrl+ホイール）"""
        if event.state & 0x0004:  # Ctrl押下時
            import time

            current_time = time.time()
            if current_time - self._last_font_change_time < 0.1:  # 100msスロットル
                return "break"

            self._last_font_change_time = current_time

            current_font = self.cget("font")
            if isinstance(current_font, str):
                font_parts = current_font.split()
                font_family = font_parts[0]
                try:
                    font_size = int(font_parts[1])
                except (IndexError, ValueError):
                    font_size = 11
            else:
                font_family = current_font[0] if len(current_font) > 0 else 'Segoe UI Emoji'
                font_size = current_font[1] if len(current_font) > 1 else 11

            new_size = font_size + (1 if event.delta > 0 else -1)
            new_size = max(8, min(24, new_size))

            self.config(font=(font_family, new_size))

            if self._on_font_size_change:
                self._on_font_size_change(new_size)

            return "break"

        return None

    def log_message(self, message: str) -> None:
        """ログメッセージを表示"""
        self.configure(state='normal')

        input_label = self._get_message('input_label')
        translated_label = self._get_message('translated_label')
        dict_meaning_label = self._get_message('dict_meaning_label')
        local_dict_label = self._get_message('local_dict_label')
        claude_api_error = self._get_message('claude_api_error')

        if claude_api_error in message or ("API" in message and ("エラー" in message or "error" in message.lower())):
            self.insert(tk.END, message, 'error_tag')
        elif input_label in message:
            parts = message.split(input_label, 1)
            self.insert(tk.END, parts[0])
            self.insert(tk.END, input_label, 'input_tag')
            self.insert(tk.END, parts[1] if len(parts) > 1 else "")
        elif translated_label in message:
            parts = message.split(translated_label, 1)
            self.insert(tk.END, parts[0])
            self.insert(tk.END, translated_label, 'translated_tag')
            self.insert(tk.END, parts[1] if len(parts) > 1 else "")
        elif dict_meaning_label in message:
            parts = message.split(dict_meaning_label, 1)
            self.insert(tk.END, parts[0])
            self.insert(tk.END, dict_meaning_label, 'dict_tag')
            self.insert(tk.END, parts[1] if len(parts) > 1 else "")
        elif local_dict_label in message:
            parts = message.split(local_dict_label, 1)
            self.insert(tk.END, parts[0])
            self.insert(tk.END, local_dict_label, 'offline_tag')
            self.insert(tk.END, parts[1] if len(parts) > 1 else "")
        else:
            self.insert(tk.END, message)

        self.insert(tk.END, '\n')
        self.configure(state='disabled')
        self.see(tk.END)

    def log_tutor_message(self, message: str, is_user: bool = True) -> None:
        """家庭教師モードのメッセージを表示"""
        self.configure(state='normal')

        if is_user:
            self.insert(tk.END, "\n[あなた] ", 'tutor_user_tag')
            self.insert(tk.END, message + "\n")
        else:
            self.insert(tk.END, "\n[先生] ", 'tutor_ai_tag')
            self.insert(tk.END, message + "\n")

        self.configure(state='disabled')
        self.see(tk.END)

    def copy_selected(self, clipboard_clear: Callable, clipboard_append: Callable) -> bool:
        """選択されたテキストをコピー"""
        self.configure(state='normal')
        try:
            selected_text = self.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                clipboard_clear()
                clipboard_append(selected_text)
                return True
        except tk.TclError:
            pass
        finally:
            self.configure(state='disabled')
        return False

    def select_all(self) -> None:
        """テキストをすべて選択"""
        self.configure(state='normal')
        self.tag_add(tk.SEL, "1.0", tk.END)
        self.mark_set(tk.INSERT, "1.0")
        self.see(tk.INSERT)
        self.configure(state='disabled')

    def clear(self) -> None:
        """テキストエリアをクリア"""
        self.configure(state='normal')
        self.delete("1.0", tk.END)
        self.configure(state='disabled')
