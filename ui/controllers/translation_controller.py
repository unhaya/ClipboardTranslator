# ClipboardTranslator v1.20 - TranslationController
"""
翻訳処理を担当するコントローラー
"""
import threading
from typing import Callable, Optional
from config.settings import config
from config.constants import MESSAGES
from core.translation import translate_with_deepl
from core.dictionary import check_dictionary
from core.language_detection import detect_language, is_single_word
from core.network import is_connected


# スレッドロック
translation_lock = threading.Lock()


class TranslationController:
    """翻訳処理コントローラー"""

    def __init__(
        self,
        clipboard_service,
        history_manager,
        on_log: Callable[[str], None],
        on_status: Callable[[str], None],
        get_message: Callable[[str], str]
    ):
        """
        初期化

        Parameters:
            clipboard_service: クリップボードサービス
            history_manager: 履歴マネージャー
            on_log: ログ出力コールバック
            on_status: ステータス更新コールバック
            get_message: メッセージ取得関数
        """
        self.clipboard = clipboard_service
        self.history = history_manager
        self._on_log = on_log
        self._on_status = on_status
        self._get_message = get_message

    def _get_config_bool(self, section: str, key: str, default: bool = False) -> bool:
        """設定から真偽値を取得"""
        if config.has_section(section) and key in config[section]:
            return config[section].getboolean(key, default)
        return default

    def _determine_target_language(self, source_lang: str) -> str:
        """
        翻訳先言語を決定する（v1.20: 多言語対応）

        Parameters:
            source_lang: 検出されたソース言語

        Returns:
            翻訳先言語コード
        """
        # 設定から翻訳先言語を取得
        configured_target = config.get('Settings', 'target_language', fallback='EN')
        auto_detect = self._get_config_bool('Settings', 'auto_detect_source', True)

        if auto_detect:
            # 自動検出モード: ソース言語と翻訳先言語が同じ場合は日英自動切替
            if source_lang == configured_target:
                # 日本語↔英語の自動切替（従来の動作）
                if source_lang == 'JA':
                    return 'EN'
                elif source_lang == 'EN':
                    return 'JA'
                else:
                    # その他の言語の場合は英語に翻訳
                    return 'EN'
            else:
                return configured_target
        else:
            # 固定モード: 常に設定された言語に翻訳
            return configured_target

    def translate(self) -> None:
        """通常の翻訳処理"""
        with translation_lock:
            try:
                text = self.clipboard.get_text()

                if not text:
                    self._on_log(self._get_message('clipboard_empty'))
                    self._on_status('clipboard_empty')
                    return

                max_length = int(config.get('Settings', 'max_translation_length', fallback='1000'))
                if len(text) > max_length:
                    self._on_log(f"\n{self._get_message('input_label')}{text[:100]}...")
                    warning_msg = self._get_message('text_too_long').format(max_length=max_length)
                    self._on_log(warning_msg)
                    self._on_status('text_too_long')
                    return

                self._on_log(f"\n{self._get_message('input_label')}{text}")

                source_lang = detect_language(text)
                # v1.20: 多言語対応 - 設定から翻訳先言語を決定
                target_lang = self._determine_target_language(source_lang)

                # 履歴から検索 - キャッシュ機能（SQLite/JSONどちらでも動作）
                cached = self.history.find_cached(text, source_lang, "normal")
                if cached:
                    translated = cached['translated_text']
                    self._on_log(f"{self._get_message('translated_label')} [cache]\n{translated}")
                    self.clipboard.set_text(translated)
                    self._on_status('translation_complete')
                    return

                # ローカル辞書で翻訳（日英のみ対応）
                if is_single_word(text) and target_lang in ('JA', 'EN'):
                    local_result = check_dictionary(text, source_lang)
                    if local_result:
                        self._on_log(f"{self._get_message('translated_label')}\n{local_result}")
                        self.clipboard.set_text(local_result)
                        self._on_status('local_dict_used')
                        self.history.add_entry(text, local_result, source_lang, target_lang, "normal")
                        return

                # DeepL APIで翻訳
                use_deepl = self._get_config_bool('Settings', 'use_deepl', True)

                if use_deepl and is_connected():
                    translated = translate_with_deepl(text, target_lang)

                    if translated:
                        self._on_log(f"{self._get_message('translated_label')}\n{translated}")
                        self.clipboard.set_text(translated)
                        self._on_status('translation_complete')
                        self.history.add_entry(text, translated, source_lang, target_lang, "normal")
                    else:
                        self._on_status('translation_failed')
                else:
                    self._on_status('service_disabled')

            except Exception as e:
                msg = f"{self._get_message('error_occurred')}: {e}"
                self._on_log(msg)
                self._on_status('error_occurred')
