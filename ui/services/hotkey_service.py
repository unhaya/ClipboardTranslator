# ClipboardTranslator v1.10 - HotkeyService
"""
グローバルホットキーの監視・管理を担当するサービス
"""
import platform
import threading
from typing import Callable, Dict, Optional
from pynput import keyboard
from config.settings import config

# macOS判定
IS_MACOS = platform.system() == 'Darwin'


class HotkeyService:
    """グローバルホットキー管理サービス"""

    def __init__(self):
        """初期化"""
        self.global_hotkeys: Optional[keyboard.GlobalHotKeys] = None
        self.hotkey_thread: Optional[threading.Thread] = None
        self._callbacks: Dict[str, Callable] = {}

    def _get_config_bool(self, section: str, key: str, default: bool = False) -> bool:
        """設定から真偽値を取得"""
        if config.has_section(section) and key in config[section]:
            return config[section].getboolean(key, default)
        return default

    def _build_hotkey_string(self, key: str, use_ctrl: bool, use_alt: bool, use_shift: bool) -> str:
        """pynput用のホットキー文字列を構築する

        macOSでは Ctrl → Cmd に自動変換
        """
        parts = []
        if use_ctrl:
            if IS_MACOS:
                parts.append('<cmd>')  # macOSではCtrlをCmdに変換
            else:
                parts.append('<ctrl>')
        if use_alt:
            parts.append('<alt>')
        if use_shift:
            parts.append('<shift>')
        parts.append(key.lower())
        return '+'.join(parts)

    def start(self, on_translate: Callable, on_dictionary: Callable, on_speech: Callable) -> None:
        """
        ホットキーリスナーを開始する

        Parameters:
            on_translate: 翻訳ホットキーが押されたときのコールバック
            on_dictionary: 辞書ホットキーが押されたときのコールバック
            on_speech: 音声出力ホットキーが押されたときのコールバック
        """
        self._callbacks = {
            'translate': on_translate,
            'dictionary': on_dictionary,
            'speech': on_speech,
        }
        self.hotkey_thread = threading.Thread(target=self._listener, daemon=True)
        self.hotkey_thread.start()

    def _listener(self) -> None:
        """ホットキーを監視する（pynput版）"""
        # 設定からホットキーを読み込み
        hotkey_key = config.get('Settings', 'hotkey_key', fallback='d')
        dict_hotkey_key = config.get('Settings', 'dict_hotkey_key', fallback='j')
        speech_hotkey_key = config.get('Settings', 'speech_hotkey_key', fallback='t')

        use_ctrl = self._get_config_bool('Settings', 'hotkey_ctrl', True)
        use_alt = self._get_config_bool('Settings', 'hotkey_alt', True)
        use_shift = self._get_config_bool('Settings', 'hotkey_shift', False)

        dict_use_ctrl = self._get_config_bool('Settings', 'dict_hotkey_ctrl', True)
        dict_use_alt = self._get_config_bool('Settings', 'dict_hotkey_alt', True)
        dict_use_shift = self._get_config_bool('Settings', 'dict_hotkey_shift', False)

        speech_use_ctrl = self._get_config_bool('Settings', 'speech_hotkey_ctrl', True)
        speech_use_alt = self._get_config_bool('Settings', 'speech_hotkey_alt', True)
        speech_use_shift = self._get_config_bool('Settings', 'speech_hotkey_shift', False)

        # ホットキー文字列を構築
        translate_hotkey = self._build_hotkey_string(hotkey_key, use_ctrl, use_alt, use_shift)
        dict_hotkey = self._build_hotkey_string(dict_hotkey_key, dict_use_ctrl, dict_use_alt, dict_use_shift)
        speech_hotkey = self._build_hotkey_string(speech_hotkey_key, speech_use_ctrl, speech_use_alt, speech_use_shift)

        print(f"ホットキー設定: 翻訳={translate_hotkey}, 辞書={dict_hotkey}, 音声={speech_hotkey}")

        # GlobalHotKeysを設定
        hotkey_map = {
            translate_hotkey: self._callbacks['translate'],
            dict_hotkey: self._callbacks['dictionary'],
            speech_hotkey: self._callbacks['speech'],
        }

        self.global_hotkeys = keyboard.GlobalHotKeys(hotkey_map)
        self.global_hotkeys.start()
        self.global_hotkeys.join()

    def restart(self) -> None:
        """ホットキーリスナーを再起動する"""
        if self.global_hotkeys:
            self.global_hotkeys.stop()
        self.hotkey_thread = threading.Thread(target=self._listener, daemon=True)
        self.hotkey_thread.start()

    def stop(self) -> None:
        """ホットキーリスナーを停止する"""
        if self.global_hotkeys:
            self.global_hotkeys.stop()
            self.global_hotkeys = None
