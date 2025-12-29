# ClipboardTranslator v1.10 - Main Window
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import webbrowser

# 親ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.constants import MESSAGES, VERSION, APP_TITLE
from config.settings import ConfigManager, config, load_config, get_config_file_path
from core.translation import translate_with_deepl, query_claude_api
from core.dictionary import check_dictionary, init_dictionaries, close_dictionary
from core.language_detection import detect_language, is_single_word
from core.text_to_speech import TextToSpeechHandler
from core.history import TranslationHistory
from core.network import is_connected
from core.tutor import TutorChatHandler
from .services.clipboard_service import ClipboardService
from .services.window_service import WindowService
from .services.hotkey_service import HotkeyService
from .components.status_bar import StatusBar
from .components.text_display import TextDisplay
from .components.chat_panel import ChatPanel
from .controllers.translation_controller import TranslationController

# スレッドロック
translation_lock = threading.Lock()


class TranslationApp(tk.Tk):
    """メインアプリケーションウィンドウ"""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("300x400")

        # ウィンドウアイコンを設定
        self.set_window_icon()

        # サービスの初期化
        self.clipboard = ClipboardService()
        self.window_service = WindowService(self)
        self.hotkey_service = HotkeyService()

        # 辞書サイズの初期化
        self.dictionary_size = 0
        self.base_dictionary_size = 0
        self.ngsl_words_count = 0

        # 設定の読み込み
        load_config()

        # 辞書の初期化（SQLiteモード）
        self.init_dictionary()

        # 履歴の初期化
        self.init_history()

        # 音声出力ハンドラーの初期化
        self.init_speech_handler()

        # メニューバーの作成（最初に作成）
        self.create_menu()

        # === フッター部分を先にpackする（BOTTOMは先にpackしたものが最下部） ===

        # ステータスバー（最下部）
        self.status_bar = StatusBar(self)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        # 会話入力パネル（ステータスバーの上）
        self.chat_panel = ChatPanel(self, on_send=self._on_chat_send)
        self.chat_panel.pack(side=tk.BOTTOM, fill=tk.X)

        # === メインコンテンツ（残りのスペースを埋める） ===

        # テキスト表示エリア
        self.text_display = TextDisplay(
            self,
            on_font_size_change=lambda size: self.update_status('font_size', font_size=size)
        )
        self.text_display.pack(expand=True, fill=tk.BOTH)

        # 右クリックメニューの設定
        self.create_context_menu()
        self.text_display.bind("<Button-3>", self.show_context_menu)

        # 家庭教師チャットハンドラーを初期化（履歴検索機能付き）
        self.tutor_handler = TutorChatHandler(history_manager=self.history)

        # コントローラーの初期化
        self.translation_controller = TranslationController(
            clipboard_service=self.clipboard,
            history_manager=self.history,
            on_log=self.log_message,
            on_status=self.update_status,
            get_message=self.get_message
        )

        # ウィンドウの閉じるボタン押下時の処理を設定
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ホットキーリスナーの開始
        self.hotkey_service.start(
            on_translate=self.hotkey_callback,
            on_dictionary=self.dict_hotkey_callback,
            on_speech=self.speech_hotkey_callback
        )

        self.log_message(self.get_message('script_running'))

    def init_dictionary(self):
        """辞書機能を初期化する"""
        try:
            # dataディレクトリのパスを取得
            app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            data_dir = os.path.join(app_dir, 'data')

            # SQLiteモードで辞書を初期化
            init_dictionaries(data_dir, use_sqlite=True)

            # 辞書サイズを取得
            from core.dictionary import get_dictionary_size
            size = get_dictionary_size()
            self.dictionary_size = size.get('total', 0)
            print(f"辞書機能を初期化しました: {self.dictionary_size}単語")
        except Exception as e:
            print(f"辞書機能の初期化に失敗しました: {e}")
            self.dictionary_size = 0

    def init_history(self):
        """翻訳履歴機能を初期化する"""
        self.history = TranslationHistory(self)
        print("翻訳履歴機能を初期化しました")

    def init_speech_handler(self):
        """音声出力ハンドラーを初期化する"""
        try:
            self.speech_handler = TextToSpeechHandler(
                status_callback=self.update_speech_status,
                error_callback=self.handle_speech_error
            )
            print("音声出力ハンドラーを初期化しました")
        except Exception as e:
            print(f"音声出力ハンドラーの初期化に失敗しました: {e}")
            self.speech_handler = None

    def set_window_icon(self):
        """ウィンドウアイコンを設定する"""
        try:
            # アイコンファイルのパスを取得
            if getattr(sys, 'frozen', False):
                # PyInstallerでビルドされた場合
                base_path = sys._MEIPASS
            else:
                # 開発環境
                base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

            icon_path = os.path.join(base_path, 'icon', '翻訳.ico')

            if os.path.exists(icon_path):
                self.iconbitmap(icon_path)
                print(f"ウィンドウアイコンを設定しました: {icon_path}")
            else:
                print(f"アイコンファイルが見つかりません: {icon_path}")
        except Exception as e:
            print(f"アイコン設定エラー: {e}")

    def get_message(self, key, **kwargs):
        """設定された言語に基づいてメッセージを取得"""
        response_language = config.get('Settings', 'response_language', fallback='JA')
        message = MESSAGES[response_language].get(key, key)

        if kwargs:
            message = message.format(**kwargs)

        return message

    def get_config_bool(self, section, key, default=False):
        """設定から真偽値を取得"""
        if config.has_section(section) and key in config[section]:
            return config[section].getboolean(key, default)
        return default

    def create_menu(self):
        """メニューバーの作成"""
        menu_bar = tk.Menu(self)

        # ファイルメニュー
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="設定", command=self.show_settings)
        file_menu.add_separator()
        file_menu.add_command(label="終了", command=self.on_closing)
        menu_bar.add_cascade(label="ファイル", menu=file_menu)

        # 編集メニュー
        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="コピー", command=self.copy_selected_text)
        edit_menu.add_command(label="すべて選択", command=self.select_all_text)
        edit_menu.add_command(label="クリア", command=self.clear_text)
        menu_bar.add_cascade(label="編集", menu=edit_menu)

        # 履歴メニュー
        history_menu = tk.Menu(menu_bar, tearoff=0)
        history_menu.add_command(label="翻訳履歴を表示", command=self.show_history_window)
        history_menu.add_separator()
        history_menu.add_command(label="履歴をクリア",
                                 command=lambda: self.history.clear_history() if hasattr(self, 'history') else None)
        menu_bar.add_cascade(label="履歴", menu=history_menu)

        # ヘルプメニュー
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="使い方", command=self.show_help)
        help_menu.add_command(label="バージョン情報", command=self.show_about)
        menu_bar.add_cascade(label="ヘルプ", menu=help_menu)

        self.config(menu=menu_bar)
        self.menu_bar = menu_bar

    def _on_chat_send(self, message: str):
        """チャットパネルからメッセージが送信されたときの処理"""
        self.log_tutor_message(message, is_user=True)
        self.update_status("考え中...")
        threading.Thread(target=self.process_tutor_message, args=(message,), daemon=True).start()

    def log_tutor_message(self, message, is_user=True):
        """家庭教師モードのメッセージを表示"""
        self.text_display.log_tutor_message(message, is_user)

    def process_tutor_message(self, message):
        """家庭教師モードのメッセージを処理（TutorChatHandlerに委譲）"""
        def on_success(response):
            self.log_tutor_message(response, is_user=False)
            self.update_status('待機中...')

        def on_error(error_msg):
            self.log_tutor_message(error_msg, is_user=False)
            self.update_status('error_occurred')

        def on_search_info(metadata):
            """検索情報をステータスに表示"""
            count = metadata.get('count', 0)
            dates = metadata.get('dates', [])

            if count > 0 and dates:
                # 最新の日付を表示
                date_str = ', '.join(dates[:2])  # 最大2つの日付
                if len(dates) > 2:
                    date_str += '等'
                status_text = f"履歴{count}件を参照中 ({date_str})"
            elif count > 0:
                status_text = f"履歴{count}件を参照中..."
            else:
                status_text = "考え中..."

            self.status_bar.set_text(status_text)

        self.tutor_handler.process_message(
            message,
            on_success=on_success,
            on_error=on_error,
            on_search_info=on_search_info
        )

    def create_context_menu(self):
        """右クリックメニューの作成"""
        self.context_menu = tk.Menu(self, tearoff=0)
        self.context_menu.add_command(label="コピー", command=self.copy_selected_text)
        self.context_menu.add_command(label="すべて選択", command=self.select_all_text)
        self.context_menu.add_command(label="クリア", command=self.clear_text)

    def show_context_menu(self, event):
        """右クリックメニューを表示"""
        self.context_menu.post(event.x_root, event.y_root)

    def copy_selected_text(self):
        """選択されたテキストをコピー"""
        if self.text_display.copy_selected(self.clipboard_clear, self.clipboard_append):
            self.update_status('text_copied')
        else:
            self.update_status('no_text_selected')

    def select_all_text(self):
        """テキストをすべて選択"""
        self.text_display.select_all()
        self.update_status('all_text_selected')

    def clear_text(self):
        """テキストエリアをクリア"""
        self.text_display.clear()
        self.update_status('text_cleared')

    def update_status(self, message_key, duration=3000, **kwargs):
        """ステータスバーのメッセージを更新"""
        self.status_bar.update(message_key, duration, **kwargs)

    def update_speech_status(self, message):
        """音声出力の状態を更新する"""
        self.update_status(message)

    def handle_speech_error(self, message):
        """音声出力のエラーを処理する"""
        self.log_message(f"音声出力エラー: {message}")
        self.update_status('error_occurred')

    def log_message(self, message):
        """ログメッセージをテキストエリアに表示"""
        self.text_display.log_message(message)

    # ホットキーコールバック（HotkeyServiceから呼び出される）
    def hotkey_callback(self):
        """通常の翻訳ホットキーが押されたときの処理"""
        self.update_status("翻訳中...")
        threading.Thread(target=self.perform_translation, daemon=True).start()

    def dict_hotkey_callback(self):
        """辞書専用ホットキーが押されたときの処理"""
        self.update_status("辞書検索中...")
        threading.Thread(target=self.perform_dictionary_translation, daemon=True).start()

    def speech_hotkey_callback(self):
        """音声出力ホットキーが押されたときの処理"""
        self.update_status("音声出力を準備中...")
        threading.Thread(target=self.perform_speech, daemon=True).start()

    def restart_hotkey_listener(self):
        """ホットキーリスナーを再起動する"""
        self.hotkey_service.restart()

    # 翻訳処理
    def perform_translation(self):
        """通常の翻訳処理（TranslationControllerに委譲）"""
        self.translation_controller.translate()

    def perform_dictionary_translation(self):
        """辞書検索処理"""
        with translation_lock:
            try:
                text = self.clipboard.get_text()

                if not text:
                    self.log_message(self.get_message('clipboard_empty'))
                    self.update_status('clipboard_empty')
                    return

                max_length = int(config.get('Settings', 'max_translation_length', fallback='1000'))
                if len(text) > max_length:
                    self.log_message(f"\n[Dictionary Lookup] {self.get_message('input_label')}{text[:100]}...")
                    warning_msg = self.get_message('text_too_long', max_length=max_length)
                    self.log_message(warning_msg)
                    self.update_status('text_too_long')
                    return

                self.log_message(f"\n[Dictionary Lookup] {self.get_message('input_label')}{text}")

                if not is_single_word(text):
                    self.log_message(self.get_message('dict_only_for_words'))
                    self.update_status('error_occurred')
                    return

                source_lang = detect_language(text)
                target_lang = 'EN' if source_lang == 'JA' else 'JA'

                # 履歴から検索 - キャッシュ機能
                for entry in self.history.history:
                    if (entry['original_text'] == text and
                        entry['source_lang'] == source_lang and
                        entry['translation_type'] == "dictionary"):
                        dict_result = entry['translated_text']
                        self.log_message(f"{self.get_message('dict_meaning_label')} [キャッシュから]\n{dict_result}")
                        self.update_status('dictionary_lookup_complete')
                        return

                claude_api_key = config.get('Settings', 'claude_api_key', fallback='')
                prompt_template = config.get('Settings', 'claude_prompt_template', fallback='')

                # ローカル辞書で検索
                local_res = check_dictionary(text, source_lang)
                if local_res:
                    self.log_message(f"{self.get_message('translated_label')}\n{local_res}")
                    self.clipboard.set_text(local_res)
                    self.update_status('local_dict_used')
                    local_dict_result = local_res
                else:
                    local_dict_result = None

                # Claude APIで詳細を取得（辞書検索はHaikuで高速処理）
                if claude_api_key and prompt_template and is_connected():
                    self.update_status('translation_in_progress')
                    claude_result = query_claude_api(text, prompt_template, claude_api_key, model_type='haiku')

                    if claude_result:
                        self.log_message(f"{self.get_message('dict_meaning_label')}\n{claude_result}")
                        self.update_status('claude_lookup_complete')

                        if local_dict_result:
                            combined_result = f"{local_dict_result}\n\n{claude_result}"
                            self.history.add_entry(text, combined_result, source_lang, target_lang, "dictionary")
                        else:
                            self.history.add_entry(text, claude_result, source_lang, target_lang, "dictionary")
                    else:
                        if not local_dict_result:
                            self.log_message(self.get_message('claude_api_error'))
                            self.update_status('translation_failed')
                        elif local_dict_result:
                            self.history.add_entry(text, local_dict_result, source_lang, target_lang, "dictionary")
                elif local_dict_result:
                    self.history.add_entry(text, local_dict_result, source_lang, target_lang, "dictionary")
                else:
                    self.log_message(self.get_message('service_disabled'))
                    self.update_status('error_occurred')

            except Exception as e:
                msg = f"{self.get_message('error_occurred')}: {e}"
                self.log_message(msg)
                self.update_status('error_occurred')

    def perform_speech(self):
        """音声出力処理"""
        if not hasattr(self, 'speech_handler') or self.speech_handler is None:
            self.log_message("音声出力機能が初期化されていません。")
            self.update_status('error_occurred')
            return

        if not self.get_config_bool('Settings', 'use_speech', True):
            self.log_message("音声出力機能は無効に設定されています。")
            self.update_status('service_disabled')
            return

        try:
            text = self.clipboard.get_text()

            if not text:
                self.log_message(self.get_message('clipboard_empty'))
                self.update_status('clipboard_empty')
                return

            max_length = int(config.get('Settings', 'max_translation_length', fallback='1000'))
            if len(text) > max_length:
                self.log_message(f"\n[音声出力] {self.get_message('input_label')}{text[:100]}...")
                warning_msg = self.get_message('text_too_long', max_length=max_length)
                self.log_message(warning_msg)
                self.update_status('text_too_long')
                return

            self.log_message(f"\n[音声出力] {self.get_message('input_label')}{text}")

            volume = float(config.get('Settings', 'speech_volume', fallback='1.0'))
            self.update_status("音声出力中...")
            success = self.speech_handler.speak(text, volume)

            if not success:
                self.update_status('service_disabled')

        except Exception as e:
            msg = f"{self.get_message('error_occurred')}: {e}"
            self.log_message(msg)
            self.update_status('error_occurred')

    # ダイアログ表示
    def show_settings(self):
        """設定ダイアログを表示"""
        from .settings_dialog import show_settings_dialog
        show_settings_dialog(self)

    def show_history_window(self):
        """翻訳履歴ウィンドウを表示"""
        from .history_dialog import show_history_dialog
        show_history_dialog(self)

    def show_help(self):
        """使い方ダイアログを表示"""
        help_window = tk.Toplevel(self)
        help_window.title("使い方")
        help_window.geometry("400x400")
        help_window.transient(self)

        help_text = """
使い方:

1. 翻訳したいテキストをコピー（Ctrl+C）
2. Ctrl+Alt+D を押す（標準ショートカット）
3. 翻訳結果が自動的にクリップボードにコピーされます

辞書機能:
1. 単語を辞書検索するには Ctrl+Alt+J を押す
2. 辞書検索は単語のみに対応しています

音声出力機能:
1. テキストを音声出力するには Ctrl+Alt+T を押す
2. この機能を使うには gTTS と pygame モジュールが必要です

その他:
- Ctrl+マウスホイール: フォントサイズの変更
        """

        text_widget = tk.Text(help_window, wrap=tk.WORD, padx=10, pady=10)
        text_widget.pack(expand=True, fill=tk.BOTH)
        text_widget.insert(tk.END, help_text)
        text_widget.config(state=tk.DISABLED)

        tk.Button(help_window, text="閉じる", command=help_window.destroy).pack(pady=10)

    def show_about(self):
        """バージョン情報ダイアログを表示"""
        about_window = tk.Toplevel(self)
        about_window.title("バージョン情報")
        about_window.geometry("300x200")
        about_window.resizable(False, False)
        about_window.transient(self)

        about_text = f"""
クリップボード翻訳ツール
Version {VERSION}

DeepL API とClaude APIを使用して、
クリップボードのテキストを翻訳・解説します。
音声出力機能も搭載しています。
        """

        tk.Label(about_window, text=about_text, justify=tk.CENTER).pack(expand=True)
        tk.Button(about_window, text="閉じる", command=about_window.destroy).pack(pady=10)

    def on_closing(self):
        """アプリケーション終了時の処理"""
        print("=== アプリケーション終了処理開始 ===")

        self.window_service.save_position()

        if hasattr(self, 'speech_handler') and self.speech_handler:
            try:
                self.speech_handler.cleanup()
            except Exception as e:
                print(f"音声出力ハンドラークリーンアップエラー: {e}")

        # 辞書データベースを閉じる
        try:
            close_dictionary()
            print("辞書データベースを閉じました")
        except Exception as e:
            print(f"辞書終了エラー: {e}")

        try:
            with open(self.window_service.config_file, 'w', encoding='utf-8') as f:
                config.write(f)
        except Exception as e:
            print(f"設定保存エラー: {e}")

        self.after(100, self.destroy)
