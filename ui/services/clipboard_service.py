# ClipboardTranslator v1.10 - ClipboardService
"""
クリップボード操作を担当するサービス
- スレッドセーフなロック管理
- クリップボードの読み書き
"""
import threading
import pyperclip


class ClipboardService:
    """クリップボード操作のサービスクラス"""

    def __init__(self):
        self._lock = threading.Lock()

    def get_text(self) -> str:
        """
        クリップボードからテキストを取得

        Returns:
            str: クリップボードのテキスト（空の場合は空文字列）
        """
        with self._lock:
            try:
                return pyperclip.paste() or ""
            except Exception:
                return ""

    def set_text(self, text: str) -> bool:
        """
        クリップボードにテキストを設定

        Parameters:
            text: 設定するテキスト

        Returns:
            bool: 成功した場合True
        """
        with self._lock:
            try:
                pyperclip.copy(text)
                return True
            except Exception:
                return False
