# ClipboardTranslator v1.00 - Main Window
import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import webbrowser
import pyperclip
from pynput import keyboard

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

# スレッドロック
translation_lock = threading.Lock()
clipboard_lock = threading.Lock()


class TranslationApp(tk.Tk):
    """メインアプリケーションウィンドウ"""

    def __init__(self):
        super().__init__()
        self.title(APP_TITLE)
        self.geometry("300x400")

        # ウィンドウアイコンを設定
        self.set_window_icon()

        # 辞書サイズの初期化
        self.dictionary_size = 0
        self.base_dictionary_size = 0
        self.ngsl_words_count = 0

        # 設定の読み込み
        load_config()
        self.config_file = get_config_file_path()

        # 辞書の初期化（SQLiteモード）
        self.init_dictionary()

        # 履歴の初期化
        self.init_history()

        # 音声出力ハンドラーの初期化
        self.init_speech_handler()

        # メニューバーの作成（最初に作成）
        self.create_menu()

        # === フッター部分を先にpackする（BOTTOMは先にpackしたものが最下部） ===

        # 状態表示ラベル（最下部）
        self.status_label = tk.Label(self, text="待機中...", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)

        # 会話入力パネルの作成（ステータスバーの上）
        self.create_chat_panel()

        # === メインコンテンツ（残りのスペースを埋める） ===

        # テキストエリアの作成
        # フォント: 絵文字対応 + 日本語読みやすさを考慮
        # 優先順: Segoe UI Emoji（絵文字）, Yu Gothic UI（日本語）, Meiryo UI（フォールバック）
        self.text_area = tk.Text(
            self,
            wrap=tk.WORD,
            bg='#333333',
            padx=12,
            pady=8,
            fg='white',
            font=('Segoe UI Emoji', 11),
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
        self.text_area.tag_configure('tutor_user_tag', foreground='#87CEEB')
        self.text_area.tag_configure('tutor_ai_tag', foreground='#98FB98')

        # 右クリックメニューの設定
        self.create_context_menu()
        self.text_area.bind("<Button-3>", self.show_context_menu)

        # 家庭教師チャットハンドラーを初期化（履歴検索機能付き）
        self.tutor_handler = TutorChatHandler(history_manager=self.history)

        # ウィンドウの閉じるボタン押下時の処理を設定
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # ホットキーリスナーの開始
        self.hotkey_thread = threading.Thread(target=self.hotkey_listener, daemon=True)
        self.hotkey_thread.start()

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

    def create_chat_panel(self):
        """開閉可能な会話入力パネルを作成"""
        # パネルの表示状態
        self.chat_panel_visible = False

        # 会話パネルのコンテナ（最初は非表示）
        self.chat_panel_frame = tk.Frame(self, bg='#2a2a2a')

        # トグルボタン（常に表示）
        self.chat_toggle_frame = tk.Frame(self, bg='#404040')
        self.chat_toggle_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.chat_toggle_btn = tk.Button(
            self.chat_toggle_frame,
            text="▲ 質問・相談する",
            command=self.toggle_chat_panel,
            bg='#404040',
            fg='#ffffff',
            activebackground='#505050',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            cursor='hand2',
            font=('Yu Gothic UI', 9)
        )
        self.chat_toggle_btn.pack(fill=tk.X, pady=2)

        # 入力エリア（パネル内）
        self.chat_input_frame = tk.Frame(self.chat_panel_frame, bg='#2a2a2a')
        self.chat_input_frame.pack(fill=tk.X, padx=5, pady=5)

        # 入力テキストボックス（絵文字対応フォント）
        self.chat_input = tk.Text(
            self.chat_input_frame,
            height=2,
            wrap=tk.WORD,
            bg='#1e1e1e',
            fg='#ffffff',
            insertbackground='#ffffff',
            font=('Segoe UI Emoji', 10),
            relief=tk.FLAT,
            padx=8,
            pady=5
        )
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.chat_input.bind('<Return>', self.on_chat_enter)
        self.chat_input.bind('<Shift-Return>', self.on_chat_newline)

        # 送信ボタン
        self.chat_send_btn = tk.Button(
            self.chat_input_frame,
            text="送信",
            command=self.send_chat_message,
            bg='#4a7c59',
            fg='#ffffff',
            activebackground='#5a8c69',
            activeforeground='#ffffff',
            relief=tk.FLAT,
            cursor='hand2',
            font=('Yu Gothic UI', 9),
            width=6
        )
        self.chat_send_btn.pack(side=tk.RIGHT, padx=(5, 0))

        # ヒントラベル
        self.chat_hint = tk.Label(
            self.chat_panel_frame,
            text="「教えて」「質問していい？」などで家庭教師モードが起動します",
            bg='#2a2a2a',
            fg='#888888',
            font=('Yu Gothic UI', 8)
        )
        self.chat_hint.pack(anchor=tk.W, padx=8, pady=(0, 5))

    def toggle_chat_panel(self):
        """会話パネルの表示/非表示を切り替える"""
        if self.chat_panel_visible:
            # パネルを非表示
            self.chat_panel_frame.pack_forget()
            self.chat_toggle_btn.config(text="▲ 質問・相談する")
            self.chat_panel_visible = False
        else:
            # パネルを表示（トグルボタンの上に）
            self.chat_panel_frame.pack(side=tk.BOTTOM, fill=tk.X, before=self.chat_toggle_frame)
            self.chat_toggle_btn.config(text="▼ 閉じる")
            self.chat_panel_visible = True
            # 入力欄にフォーカス
            self.chat_input.focus_set()

    def on_chat_enter(self, event):
        """Enterキーで送信"""
        self.send_chat_message()
        return 'break'  # デフォルトの改行を防止

    def on_chat_newline(self, event):
        """Shift+Enterで改行"""
        return None  # デフォルト動作（改行挿入）を許可

    def send_chat_message(self):
        """チャットメッセージを送信"""
        message = self.chat_input.get("1.0", tk.END).strip()
        if not message:
            return

        # 入力欄をクリア
        self.chat_input.delete("1.0", tk.END)

        # ユーザーのメッセージを表示
        self.log_tutor_message(message, is_user=True)

        # RAG家庭教師処理を実行（別スレッドで）
        self.update_status("考え中...")
        threading.Thread(target=self.process_tutor_message, args=(message,), daemon=True).start()

    def log_tutor_message(self, message, is_user=True):
        """家庭教師モードのメッセージを表示"""
        self.text_area.configure(state='normal')

        if is_user:
            self.text_area.insert(tk.END, "\n[あなた] ", 'tutor_user_tag')
            self.text_area.insert(tk.END, message + "\n")
        else:
            self.text_area.insert(tk.END, "\n[先生] ", 'tutor_ai_tag')
            self.text_area.insert(tk.END, message + "\n")

        self.text_area.configure(state='disabled')
        self.text_area.see(tk.END)

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

            self.status_label.config(text=status_text)

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
        """フォントサイズを変更（スロットル処理付き：100ms間隔で制限）"""
        if event.state & 0x0004:
            import time

            # スロットル: 最後の変更から100ms以内は無視
            current_time = time.time()
            if hasattr(self, '_last_font_change_time'):
                if current_time - self._last_font_change_time < 0.1:  # 100ms
                    return "break"

            self._last_font_change_time = current_time

            current_font = self.text_area.cget("font")
            if isinstance(current_font, str):
                font_parts = current_font.split()
                font_family = font_parts[0]
                try:
                    font_size = int(font_parts[1])
                except (IndexError, ValueError):
                    font_size = 11
            else:
                font_family = current_font[0] if len(current_font) > 0 else 'Yu Gothic UI'
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
    def _build_hotkey_string(self, key, use_ctrl, use_alt, use_shift):
        """pynput用のホットキー文字列を構築する"""
        parts = []
        if use_ctrl:
            parts.append('<ctrl>')
        if use_alt:
            parts.append('<alt>')
        if use_shift:
            parts.append('<shift>')
        parts.append(key.lower())
        return '+'.join(parts)

    def hotkey_listener(self):
        """ホットキーを監視する（pynput版）"""
        # 設定からホットキーを読み込み
        hotkey_key = config.get('Settings', 'hotkey_key', fallback='d')
        dict_hotkey_key = config.get('Settings', 'dict_hotkey_key', fallback='j')
        speech_hotkey_key = config.get('Settings', 'speech_hotkey_key', fallback='t')

        use_ctrl = self.get_config_bool('Settings', 'hotkey_ctrl', True)
        use_alt = self.get_config_bool('Settings', 'hotkey_alt', True)
        use_shift = self.get_config_bool('Settings', 'hotkey_shift', False)

        dict_use_ctrl = self.get_config_bool('Settings', 'dict_hotkey_ctrl', True)
        dict_use_alt = self.get_config_bool('Settings', 'dict_hotkey_alt', True)
        dict_use_shift = self.get_config_bool('Settings', 'dict_hotkey_shift', False)

        speech_use_ctrl = self.get_config_bool('Settings', 'speech_hotkey_ctrl', True)
        speech_use_alt = self.get_config_bool('Settings', 'speech_hotkey_alt', True)
        speech_use_shift = self.get_config_bool('Settings', 'speech_hotkey_shift', False)

        # ホットキー文字列を構築
        translate_hotkey = self._build_hotkey_string(hotkey_key, use_ctrl, use_alt, use_shift)
        dict_hotkey = self._build_hotkey_string(dict_hotkey_key, dict_use_ctrl, dict_use_alt, dict_use_shift)
        speech_hotkey = self._build_hotkey_string(speech_hotkey_key, speech_use_ctrl, speech_use_alt, speech_use_shift)

        print(f"ホットキー設定: 翻訳={translate_hotkey}, 辞書={dict_hotkey}, 音声={speech_hotkey}")

        # GlobalHotKeysを設定
        hotkey_map = {
            translate_hotkey: self.hotkey_callback,
            dict_hotkey: self.dict_hotkey_callback,
            speech_hotkey: self.speech_hotkey_callback,
        }

        self.global_hotkeys = keyboard.GlobalHotKeys(hotkey_map)
        self.global_hotkeys.start()
        self.global_hotkeys.join()

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
        if hasattr(self, 'global_hotkeys') and self.global_hotkeys:
            self.global_hotkeys.stop()
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

        # 辞書データベースを閉じる
        try:
            close_dictionary()
            print("辞書データベースを閉じました")
        except Exception as e:
            print(f"辞書終了エラー: {e}")

        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                config.write(f)
        except Exception as e:
            print(f"設定保存エラー: {e}")

        self.after(100, self.destroy)
