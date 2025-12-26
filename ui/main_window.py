# ClipboardTranslator v1.00 - Main Window
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import webbrowser
import pyperclip
import keyboard

# 親ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.constants import MESSAGES, VERSION, APP_TITLE
from config.settings import ConfigManager, config, load_config, get_config_file_path
from core.translation import translate_with_deepl, query_claude_api
from core.dictionary import check_dictionary
from core.language_detection import detect_language, is_single_word
from core.text_to_speech import TextToSpeechHandler
from core.history import TranslationHistory
from core.vocabulary import VocabularyManager
from core.network import is_connected

# スレッドロック
translation_lock = threading.Lock()
clipboard_lock = threading.Lock()


class TranslationApp(tk.Tk):
    """メインアプリケーションウィンドウ"""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("300x400")

        # 辞書サイズの初期化
        self.dictionary_size = 0
        self.base_dictionary_size = 0
        self.ngsl_words_count = 0

        # 設定の読み込み
        load_config()
        self.config_file = get_config_file_path()

        # 履歴の初期化
        self.init_history()

        # 単語帳の初期化
        self.init_vocabulary()

        # 音声出力ハンドラーの初期化
        self.init_speech_handler()

        # テキストエリアの作成
        self.text_area = tk.Text(
            self,
            wrap=tk.WORD,
            bg='#333333',
            padx=8,
            pady=8,
            fg='white',
            font=('Serif', 11),
            spacing1=2,
            spacing2=8,
            spacing3=8,
        )
        self.text_area.pack(expand=True, fill=tk.BOTH)
        self.text_area.configure(state='disabled')
        self.text_area.bind("<MouseWheel>", self.change_font_size)

        # タグの設定
        self.text_area.tag_configure('input_tag', foreground='#9597f7')
        self.text_area.tag_configure('translated_tag', foreground='#9597f7')
        self.text_area.tag_configure('dict_tag', foreground='#95f797')
        self.text_area.tag_configure('offline_tag', foreground='#f7d195')
        self.text_area.tag_configure('error_tag', foreground='#ff6b6b')
        self.text_area.tag_configure('speech_tag', foreground='#f79595')

        # 右クリックメニューの設定
        self.create_context_menu()
        self.text_area.bind("<Button-3>", self.show_context_menu)

        # 状態表示ラベル
        self.status_label = tk.Label(self, text="待機中...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # メニューバーの作成
        self.create_menu()

        # ウィンドウの閉じるボタン押下時の処理を設定
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ホットキーリスナーの開始
        self.hotkey_thread = threading.Thread(target=self.hotkey_listener, daemon=True)
        self.hotkey_thread.start()

        self.log_message(self.get_message('script_running'))

    def init_history(self):
        """翻訳履歴機能を初期化する"""
        self.history = TranslationHistory(self)
        print("翻訳履歴機能を初期化しました")

    def init_vocabulary(self):
        """単語帳機能を初期化する"""
        try:
            self.vocab_manager = VocabularyManager(self)
            print("単語帳機能を初期化しました")
        except Exception as e:
            print(f"単語帳機能の初期化に失敗しました: {e}")

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

        # 単語帳メニュー
        vocabulary_menu = tk.Menu(menu_bar, tearoff=0)
        vocabulary_menu.add_command(label="単語帳を開く", command=self.show_vocabulary_window)
        vocabulary_menu.add_command(label="クリップボードの単語を追加", command=self.add_clipboard_to_vocabulary)
        menu_bar.add_cascade(label="単語帳", menu=vocabulary_menu)

        # ヘルプメニュー
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="使い方", command=self.show_help)
        help_menu.add_command(label="バージョン情報", command=self.show_about)
        menu_bar.add_cascade(label="ヘルプ", menu=help_menu)

        self.config(menu=menu_bar)
        self.menu_bar = menu_bar

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
        self.text_area.configure(state='normal')
        try:
            selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            if selected_text:
                self.clipboard_clear()
                self.clipboard_append(selected_text)
                self.update_status('text_copied')
        except tk.TclError:
            self.update_status('no_text_selected')
        self.text_area.configure(state='disabled')

    def select_all_text(self):
        """テキストをすべて選択"""
        self.text_area.configure(state='normal')
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        self.text_area.configure(state='disabled')
        self.update_status('all_text_selected')

    def clear_text(self):
        """テキストエリアをクリア"""
        self.text_area.configure(state='normal')
        self.text_area.delete(1.0, tk.END)
        self.text_area.configure(state='disabled')
        self.update_status('text_cleared')

    def update_status(self, message_key, duration=3000, **kwargs):
        """ステータスバーのメッセージを更新"""
        if message_key in MESSAGES['JA'] or message_key in MESSAGES['EN']:
            message = self.get_message(message_key, **kwargs)
        else:
            message = message_key

        self.status_label.config(text=message)
        waiting_msg = self.get_message('waiting')
        self.after(duration, lambda: self.status_label.config(text=waiting_msg))

    def update_speech_status(self, message):
        """音声出力の状態を更新する"""
        self.update_status(message)

    def handle_speech_error(self, message):
        """音声出力のエラーを処理する"""
        self.log_message(f"音声出力エラー: {message}")
        self.update_status('error_occurred')

    def change_font_size(self, event):
        """フォントサイズを変更"""
        if event.state & 0x0004:
            current_font = self.text_area.cget("font")
            if isinstance(current_font, str):
                font_parts = current_font.split()
                font_family = font_parts[0]
                try:
                    font_size = int(font_parts[1])
                except (IndexError, ValueError):
                    font_size = 11
            else:
                font_family = current_font[0] if len(current_font) > 0 else 'Serif'
                font_size = current_font[1] if len(current_font) > 1 else 11

            new_size = font_size + (1 if event.delta > 0 else -1)
            if new_size < 8:
                new_size = 8
            elif new_size > 24:
                new_size = 24

            new_font = (font_family, new_size)
            self.text_area.config(font=new_font)
            self.update_status('font_size', font_size=new_size)
            return "break"

    def log_message(self, message):
        """ログメッセージをテキストエリアに表示"""
        self.text_area.configure(state='normal')

        input_label = self.get_message('input_label')
        translated_label = self.get_message('translated_label')
        dict_meaning_label = self.get_message('dict_meaning_label')
        local_dict_label = self.get_message('local_dict_label')
        claude_api_error = self.get_message('claude_api_error')

        if claude_api_error in message or ("API" in message and ("エラー" in message or "error" in message.lower())):
            self.text_area.insert(tk.END, message, 'error_tag')
        elif input_label in message:
            parts = message.split(input_label, 1)
            self.text_area.insert(tk.END, parts[0])
            self.text_area.insert(tk.END, input_label, 'input_tag')
            self.text_area.insert(tk.END, parts[1] if len(parts) > 1 else "")
        elif translated_label in message:
            parts = message.split(translated_label, 1)
            self.text_area.insert(tk.END, parts[0])
            self.text_area.insert(tk.END, translated_label, 'translated_tag')
            self.text_area.insert(tk.END, parts[1] if len(parts) > 1 else "")
        elif dict_meaning_label in message:
            parts = message.split(dict_meaning_label, 1)
            self.text_area.insert(tk.END, parts[0])
            self.text_area.insert(tk.END, dict_meaning_label, 'dict_tag')
            self.text_area.insert(tk.END, parts[1] if len(parts) > 1 else "")
        elif local_dict_label in message:
            parts = message.split(local_dict_label, 1)
            self.text_area.insert(tk.END, parts[0])
            self.text_area.insert(tk.END, local_dict_label, 'offline_tag')
            self.text_area.insert(tk.END, parts[1] if len(parts) > 1 else "")
        else:
            self.text_area.insert(tk.END, message)

        self.text_area.insert(tk.END, '\n')
        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

    # ホットキー関連
    def hotkey_listener(self):
        """ホットキーを監視する"""
        hotkey_key = config.get('Settings', 'hotkey_key', fallback='d')
        dict_hotkey_key = config.get('Settings', 'dict_hotkey_key', fallback='j')
        speech_hotkey_key = config.get('Settings', 'speech_hotkey_key', fallback='t')

        keyboard.on_release_key(hotkey_key, self.hotkey_callback, suppress=True)
        keyboard.on_release_key(dict_hotkey_key, self.dict_hotkey_callback, suppress=True)
        keyboard.on_release_key(speech_hotkey_key, self.speech_hotkey_callback, suppress=True)
        keyboard.wait()

    def hotkey_callback(self, e):
        """通常の翻訳ホットキーが押されたときの処理"""
        use_ctrl = self.get_config_bool('Settings', 'hotkey_ctrl', True)
        use_alt = self.get_config_bool('Settings', 'hotkey_alt', True)
        use_shift = self.get_config_bool('Settings', 'hotkey_shift', False)

        ctrl_pressed = keyboard.is_pressed('ctrl')
        alt_pressed = keyboard.is_pressed('alt')
        shift_pressed = keyboard.is_pressed('shift')

        if ((not use_ctrl or ctrl_pressed) and
            (not use_alt or alt_pressed) and
            (not use_shift or shift_pressed)):
            self.update_status("翻訳中...")
            threading.Thread(target=self.perform_translation, daemon=True).start()

    def dict_hotkey_callback(self, e):
        """辞書専用ホットキーが押されたときの処理"""
        use_ctrl = self.get_config_bool('Settings', 'dict_hotkey_ctrl', True)
        use_alt = self.get_config_bool('Settings', 'dict_hotkey_alt', True)
        use_shift = self.get_config_bool('Settings', 'dict_hotkey_shift', False)

        ctrl_pressed = keyboard.is_pressed('ctrl')
        alt_pressed = keyboard.is_pressed('alt')
        shift_pressed = keyboard.is_pressed('shift')

        if ((not use_ctrl or ctrl_pressed) and
            (not use_alt or alt_pressed) and
            (not use_shift or shift_pressed)):
            self.update_status("辞書検索中...")
            threading.Thread(target=self.perform_dictionary_translation, daemon=True).start()

    def speech_hotkey_callback(self, e):
        """音声出力ホットキーが押されたときの処理"""
        use_ctrl = self.get_config_bool('Settings', 'speech_hotkey_ctrl', True)
        use_alt = self.get_config_bool('Settings', 'speech_hotkey_alt', True)
        use_shift = self.get_config_bool('Settings', 'speech_hotkey_shift', False)

        ctrl_pressed = keyboard.is_pressed('ctrl')
        alt_pressed = keyboard.is_pressed('alt')
        shift_pressed = keyboard.is_pressed('shift')

        if ((not use_ctrl or ctrl_pressed) and
            (not use_alt or alt_pressed) and
            (not use_shift or shift_pressed)):
            self.update_status("音声出力を準備中...")
            threading.Thread(target=self.perform_speech, daemon=True).start()

    def restart_hotkey_listener(self):
        """ホットキーリスナーを再起動する"""
        keyboard.unhook_all()
        self.hotkey_thread = threading.Thread(target=self.hotkey_listener, daemon=True)
        self.hotkey_thread.start()

    # 翻訳処理
    def perform_translation(self):
        """通常の翻訳処理"""
        with translation_lock:
            try:
                with clipboard_lock:
                    text = pyperclip.paste()

                if not text:
                    self.log_message(self.get_message('clipboard_empty'))
                    self.update_status('clipboard_empty')
                    return

                max_length = int(config.get('Settings', 'max_translation_length', fallback='1000'))
                if len(text) > max_length:
                    self.log_message(f"\n{self.get_message('input_label')}{text[:100]}...")
                    warning_msg = self.get_message('text_too_long', max_length=max_length)
                    self.log_message(warning_msg)
                    self.update_status('text_too_long')
                    return

                self.log_message(f"\n{self.get_message('input_label')}{text}")

                source_lang = detect_language(text)
                target_lang = 'EN' if source_lang == 'JA' else 'JA'

                # 履歴から検索 - キャッシュ機能
                for entry in self.history.history:
                    if entry['original_text'] == text and entry['source_lang'] == source_lang:
                        translated = entry['translated_text']
                        self.log_message(f"{self.get_message('translated_label')} [キャッシュから]\n{translated}")
                        with clipboard_lock:
                            pyperclip.copy(translated)
                        self.update_status('translation_complete')
                        return

                # ローカル辞書で翻訳
                if is_single_word(text):
                    local_result = check_dictionary(text, source_lang)
                    if local_result:
                        self.log_message(f"{self.get_message('translated_label')}\n{local_result}")
                        with clipboard_lock:
                            pyperclip.copy(local_result)
                        self.update_status('local_dict_used')
                        self.history.add_entry(text, local_result, source_lang, target_lang, "normal")
                        return

                # DeepL APIで翻訳
                use_deepl = self.get_config_bool('Settings', 'use_deepl', True)

                if use_deepl and is_connected():
                    translated = translate_with_deepl(text, target_lang)

                    if translated:
                        self.log_message(f"{self.get_message('translated_label')}\n{translated}")
                        with clipboard_lock:
                            pyperclip.copy(translated)
                        self.update_status('translation_complete')
                        self.history.add_entry(text, translated, source_lang, target_lang, "normal")
                    else:
                        self.update_status('translation_failed')
                else:
                    self.update_status('service_disabled')

            except Exception as e:
                msg = f"{self.get_message('error_occurred')}: {e}"
                self.log_message(msg)
                self.update_status('error_occurred')

    def perform_dictionary_translation(self):
        """辞書検索処理"""
        with translation_lock:
            try:
                with clipboard_lock:
                    text = pyperclip.paste()

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
                    with clipboard_lock:
                        pyperclip.copy(local_res)
                    self.update_status('local_dict_used')
                    local_dict_result = local_res
                else:
                    local_dict_result = None

                # Claude APIで詳細を取得
                if claude_api_key and prompt_template and is_connected():
                    self.update_status('translation_in_progress')
                    claude_result = query_claude_api(text, prompt_template, claude_api_key)

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
            with clipboard_lock:
                text = pyperclip.paste()

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

    def show_vocabulary_window(self):
        """単語帳ウィンドウを表示"""
        from .vocabulary_dialog import show_vocabulary_dialog
        show_vocabulary_dialog(self)

    def add_clipboard_to_vocabulary(self):
        """クリップボードの単語を単語帳に追加"""
        if not hasattr(self, 'vocab_manager'):
            messagebox.showwarning("警告", "単語帳機能が初期化されていません")
            return

        with clipboard_lock:
            text = pyperclip.paste()

        if not text:
            self.log_message(self.get_message('clipboard_empty'))
            self.update_status('clipboard_empty')
            return

        source_lang = detect_language(text)
        target_lang = 'EN' if source_lang == 'JA' else 'JA'

        local_result = check_dictionary(text, source_lang)
        translated = local_result or ""

        if not translated and self.get_config_bool('Settings', 'use_deepl', True) and is_connected():
            translated = translate_with_deepl(text, target_lang) or ""

        self.vocab_manager.add_word(text, translated, source_lang, target_lang)
        messagebox.showinfo("追加完了", f"単語「{text}」を単語帳に追加しました")

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

    # ウィンドウ位置の保存/読み込み
    def save_window_position(self):
        """ウィンドウの位置とサイズを設定ファイルに保存"""
        try:
            x = self.winfo_x()
            y = self.winfo_y()
            width = self.winfo_width()
            height = self.winfo_height()

            if not config.has_section('Window'):
                config.add_section('Window')

            config.set('Window', 'x', str(x))
            config.set('Window', 'y', str(y))
            config.set('Window', 'width', str(width))
            config.set('Window', 'height', str(height))

            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)

            print(f"ウィンドウ位置を保存しました: {self.config_file}")
        except Exception as e:
            print(f"ウィンドウ位置の保存に失敗しました: {e}")

    def load_window_position(self):
        """保存されたウィンドウの位置とサイズを読み込み適用"""
        try:
            if os.path.exists(self.config_file):
                config.read(self.config_file, encoding='utf-8')

                if config.has_section('Window'):
                    x = config.getint('Window', 'x', fallback=100)
                    y = config.getint('Window', 'y', fallback=100)
                    width = config.getint('Window', 'width', fallback=300)
                    height = config.getint('Window', 'height', fallback=400)

                    screen_width = self.winfo_screenwidth()
                    screen_height = self.winfo_screenheight()

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

                    self.geometry(f"{width}x{height}+{x}+{y}")
                    return True

            self.geometry("300x400")
            return False
        except Exception as e:
            print(f"ウィンドウ位置の読み込みに失敗しました: {e}")
            self.geometry("300x400")
            return False

    def on_closing(self):
        """アプリケーション終了時の処理"""
        print("=== アプリケーション終了処理開始 ===")

        self.save_window_position()

        if hasattr(self, 'speech_handler') and self.speech_handler:
            try:
                self.speech_handler.cleanup()
            except Exception as e:
                print(f"音声出力ハンドラークリーンアップエラー: {e}")

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)
        except Exception as e:
            print(f"設定保存エラー: {e}")

        self.after(100, self.destroy)
