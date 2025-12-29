# ClipboardTranslator v1.10 - SpeechController
"""
音声出力処理を担当するコントローラー
"""
from typing import Callable, Optional
from config.settings import config


class SpeechController:
    """音声出力処理コントローラー"""

    def __init__(
        self,
        clipboard_service,
        speech_handler,
        on_log: Callable[[str], None],
        on_status: Callable[[str], None],
        get_message: Callable[[str], str]
    ):
        """
        初期化

        Parameters:
            clipboard_service: クリップボードサービス
            speech_handler: 音声出力ハンドラー
            on_log: ログ出力コールバック
            on_status: ステータス更新コールバック
            get_message: メッセージ取得関数
        """
        self.clipboard = clipboard_service
        self.speech_handler = speech_handler
        self._on_log = on_log
        self._on_status = on_status
        self._get_message = get_message

    def _get_config_bool(self, section: str, key: str, default: bool = False) -> bool:
        """設定から真偽値を取得"""
        if config.has_section(section) and key in config[section]:
            return config[section].getboolean(key, default)
        return default

    def speak(self) -> None:
        """音声出力処理"""
        if self.speech_handler is None:
            self._on_log("音声出力機能が初期化されていません。")
            self._on_status('error_occurred')
            return

        if not self._get_config_bool('Settings', 'use_speech', True):
            self._on_log("音声出力機能は無効に設定されています。")
            self._on_status('service_disabled')
            return

        try:
            text = self.clipboard.get_text()

            if not text:
                self._on_log(self._get_message('clipboard_empty'))
                self._on_status('clipboard_empty')
                return

            max_length = int(config.get('Settings', 'max_translation_length', fallback='1000'))
            if len(text) > max_length:
                self._on_log(f"\n[音声出力] {self._get_message('input_label')}{text[:100]}...")
                warning_msg = self._get_message('text_too_long').format(max_length=max_length)
                self._on_log(warning_msg)
                self._on_status('text_too_long')
                return

            self._on_log(f"\n[音声出力] {self._get_message('input_label')}{text}")

            volume = float(config.get('Settings', 'speech_volume', fallback='1.0'))
            self._on_status("音声出力中...")
            success = self.speech_handler.speak(text, volume)

            if not success:
                self._on_status('service_disabled')

        except Exception as e:
            msg = f"{self._get_message('error_occurred')}: {e}"
            self._on_log(msg)
            self._on_status('error_occurred')
