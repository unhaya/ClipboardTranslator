# ClipboardTranslator v1.10 - WindowService
"""
ウィンドウ位置の保存・復元を担当するサービス
"""
import os
import tkinter as tk
from config.settings import config, get_config_file_path


class WindowService:
    """ウィンドウ位置管理サービス"""

    def __init__(self, window: tk.Tk):
        """
        初期化

        Parameters:
            window: 管理対象のTkウィンドウ
        """
        self.window = window
        self.config_file = get_config_file_path()

    def save_position(self) -> bool:
        """
        ウィンドウの位置とサイズを設定ファイルに保存

        Returns:
            bool: 成功した場合True
        """
        try:
            x = self.window.winfo_x()
            y = self.window.winfo_y()
            width = self.window.winfo_width()
            height = self.window.winfo_height()

            if not config.has_section('Window'):
                config.add_section('Window')

            config.set('Window', 'x', str(x))
            config.set('Window', 'y', str(y))
            config.set('Window', 'width', str(width))
            config.set('Window', 'height', str(height))

            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)

            print(f"ウィンドウ位置を保存しました: {self.config_file}")
            return True
        except Exception as e:
            print(f"ウィンドウ位置の保存に失敗しました: {e}")
            return False

    def load_position(self) -> bool:
        """
        保存されたウィンドウの位置とサイズを読み込み適用

        Returns:
            bool: 位置が復元された場合True
        """
        try:
            if os.path.exists(self.config_file):
                config.read(self.config_file, encoding='utf-8')

                if config.has_section('Window'):
                    x = config.getint('Window', 'x', fallback=100)
                    y = config.getint('Window', 'y', fallback=100)
                    width = config.getint('Window', 'width', fallback=300)
                    height = config.getint('Window', 'height', fallback=400)

                    # 画面内に収まるよう調整
                    x, y, width, height = self._ensure_on_screen(x, y, width, height)

                    self.window.geometry(f"{width}x{height}+{x}+{y}")
                    return True

            self.window.geometry("300x400")
            return False
        except Exception as e:
            print(f"ウィンドウ位置の読み込みに失敗しました: {e}")
            self.window.geometry("300x400")
            return False

    def _ensure_on_screen(self, x: int, y: int, width: int, height: int) -> tuple:
        """
        ウィンドウが画面内に収まるよう調整

        Parameters:
            x, y: ウィンドウ位置
            width, height: ウィンドウサイズ

        Returns:
            tuple: 調整後の (x, y, width, height)
        """
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()

        if x < 0:
            x = 0
        elif x > screen_width - 100:
            x = screen_width - 300

        if y < 0:
            y = 0
        elif y > screen_height - 100:
            y = screen_height - 300

        width = max(300, width)
        height = max(400, height)

        return x, y, width, height
