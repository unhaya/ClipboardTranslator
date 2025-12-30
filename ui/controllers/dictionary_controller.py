# ClipboardTranslator v1.10 - DictionaryController
"""
辞書検索処理を担当するコントローラー
"""
import threading
from typing import Callable
from config.settings import config
from core.translation import query_claude_api
from core.dictionary import check_dictionary
from core.language_detection import detect_language, is_single_word
from core.network import is_connected


# スレッドロック
translation_lock = threading.Lock()


class DictionaryController:
    """辞書検索処理コントローラー"""

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

    def lookup(self) -> None:
        """辞書検索処理"""
        with translation_lock:
            try:
                text = self.clipboard.get_text()

                if not text:
                    self._on_log(self._get_message('clipboard_empty'))
                    self._on_status('clipboard_empty')
                    return

                max_length = int(config.get('Settings', 'max_translation_length', fallback='1000'))
                if len(text) > max_length:
                    self._on_log(f"\n[Dictionary Lookup] {self._get_message('input_label')}{text[:100]}...")
                    warning_msg = self._get_message('text_too_long').format(max_length=max_length)
                    self._on_log(warning_msg)
                    self._on_status('text_too_long')
                    return

                self._on_log(f"\n[Dictionary Lookup] {self._get_message('input_label')}{text}")

                if not is_single_word(text):
                    self._on_log(self._get_message('dict_only_for_words'))
                    self._on_status('error_occurred')
                    return

                source_lang = detect_language(text)
                target_lang = 'EN' if source_lang == 'JA' else 'JA'

                # 履歴から検索 - キャッシュ機能（SQLite/JSONどちらでも動作）
                cached = self.history.find_cached(text, source_lang, "dictionary")
                if cached:
                    dict_result = cached['translated_text']
                    self._on_log(f"{self._get_message('dict_meaning_label')} [cache]\n{dict_result}")
                    self._on_status('dictionary_lookup_complete')
                    return

                claude_api_key = config.get('Settings', 'claude_api_key', fallback='')
                prompt_template = config.get('Settings', 'claude_prompt_template', fallback='')

                # ローカル辞書で検索
                local_res = check_dictionary(text, source_lang)
                if local_res:
                    self._on_log(f"{self._get_message('translated_label')}\n{local_res}")
                    self.clipboard.set_text(local_res)
                    self._on_status('local_dict_used')
                    local_dict_result = local_res
                else:
                    local_dict_result = None

                # Claude APIで詳細を取得（辞書検索はHaikuで高速処理）
                if claude_api_key and prompt_template and is_connected():
                    self._on_status('translation_in_progress')
                    claude_result = query_claude_api(text, prompt_template, claude_api_key, model_type='haiku')

                    if claude_result:
                        self._on_log(f"{self._get_message('dict_meaning_label')}\n{claude_result}")
                        self._on_status('claude_lookup_complete')

                        if local_dict_result:
                            combined_result = f"{local_dict_result}\n\n{claude_result}"
                            self.history.add_entry(text, combined_result, source_lang, target_lang, "dictionary")
                        else:
                            self.history.add_entry(text, claude_result, source_lang, target_lang, "dictionary")
                    else:
                        if not local_dict_result:
                            self._on_log(self._get_message('claude_api_error'))
                            self._on_status('translation_failed')
                        elif local_dict_result:
                            self.history.add_entry(text, local_dict_result, source_lang, target_lang, "dictionary")
                elif local_dict_result:
                    self.history.add_entry(text, local_dict_result, source_lang, target_lang, "dictionary")
                else:
                    self._on_log(self._get_message('service_disabled'))
                    self._on_status('error_occurred')

            except Exception as e:
                msg = f"{self._get_message('error_occurred')}: {e}"
                self._on_log(msg)
                self._on_status('error_occurred')
