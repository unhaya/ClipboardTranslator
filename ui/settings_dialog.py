# ClipboardTranslator v1.00 - Settings Dialog
import os
import sys
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import requests

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.constants import DEEPL_URL, KEY_OPTIONS
from config.settings import config, get_config_file_path
from core.translation import query_claude_api


def show_settings_dialog(app):
    """設定ダイアログを表示"""
    settings_window = tk.Toplevel(app)
    settings_window.title("設定")
    settings_window.geometry("550x550")
    settings_window.minsize(550, 520)
    settings_window.resizable(True, True)
    settings_window.transient(app)
    settings_window.grab_set()

    # スタイル設定
    style = ttk.Style()
    default_font = ('Yu Gothic UI', 9)
    style.configure('.', font=default_font)
    style.configure("TNotebook", background="#f0f0f0", borderwidth=0)
    style.configure("TNotebook.Tab", background="#e0e0e0", padding=[8, 4], font=default_font)
    style.configure("TFrame", background="#ffffff")
    style.configure("TLabelframe", background="#ffffff", borderwidth=1, relief="solid")
    style.configure("TLabelframe.Label", background="#ffffff", foreground="#333333",
                    font=(default_font[0], default_font[1], 'bold'))
    style.configure("TButton", background="#e0e0e0", foreground="#000000", padding=[10, 5], font=default_font)
    style.configure("TCheckbutton", background="#ffffff", font=default_font)
    style.configure("TRadiobutton", background="#ffffff", font=default_font)
    style.configure("TLabel", background="#ffffff", font=default_font)
    style.configure("Preview.TLabel", font=(default_font[0], default_font[1], 'bold'), foreground="#0078d7")

    # ボタンフレーム
    button_frame = ttk.Frame(settings_window)
    button_frame.pack(side="bottom", fill="x", pady=10, padx=15)

    # メインコンテンツ
    main_frame = ttk.Frame(settings_window, padding=10)
    main_frame.pack(fill="both", expand=True)

    # タブコントロール
    tab_control = ttk.Notebook(main_frame)
    tab_control.pack(fill="both", expand=True)

    # タブ
    translation_tab = ttk.Frame(tab_control, padding=10)
    api_tab = ttk.Frame(tab_control, padding=10)
    shortcut_tab = ttk.Frame(tab_control, padding=10)
    speech_tab = ttk.Frame(tab_control, padding=10)
    ui_tab = ttk.Frame(tab_control, padding=10)

    tab_control.add(translation_tab, text=" 翻訳設定 ")
    tab_control.add(api_tab, text=" API設定 ")
    tab_control.add(shortcut_tab, text=" ショートカット ")
    tab_control.add(speech_tab, text=" 音声設定 ")
    tab_control.add(ui_tab, text=" 表示設定 ")

    # === 翻訳設定タブ ===
    translation_frame = ttk.LabelFrame(translation_tab, text="翻訳オプション", padding=15)
    translation_frame.pack(fill="x", pady=10)

    use_deepl_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'use_deepl', True))
    ttk.Checkbutton(translation_frame, text="DeepL APIを使用", variable=use_deepl_var).pack(anchor="w", pady=5)

    auto_add_vocab_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'auto_add_to_vocabulary', False))
    ttk.Checkbutton(translation_frame, text="翻訳した単語を自動的に単語帳に追加",
                    variable=auto_add_vocab_var).pack(anchor="w", pady=5)

    # === API設定タブ ===
    # DeepL API
    api_frame = ttk.LabelFrame(api_tab, text="DeepL API設定", padding=15)
    api_frame.pack(fill="x", pady=10)

    ttk.Label(api_frame, text="DeepL APIキー:").pack(anchor="w", pady=(0, 5))
    api_key_var = tk.StringVar(value=config.get('Settings', 'deepl_api_key', fallback=''))
    api_key_entry = ttk.Entry(api_frame, textvariable=api_key_var, width=40)
    api_key_entry.pack(fill="x")

    # Claude API
    claude_frame = ttk.LabelFrame(api_tab, text="Claude API設定", padding=15)
    claude_frame.pack(fill="x", pady=(20, 10))

    ttk.Label(claude_frame, text="Claude APIキー:").pack(anchor="w", pady=(0, 5))
    claude_api_key_var = tk.StringVar(value=config.get('Settings', 'claude_api_key', fallback=''))
    claude_api_key_entry = ttk.Entry(claude_frame, textvariable=claude_api_key_var, width=40)
    claude_api_key_entry.pack(fill="x")

    ttk.Label(claude_frame, text="プロンプトテンプレート:").pack(anchor="w", pady=(10, 5))
    prompt_text = tk.Text(claude_frame, width=40, height=8, wrap=tk.WORD)
    prompt_text.pack(fill="x")
    prompt_text.insert("1.0", config.get('Settings', 'claude_prompt_template', fallback=''))

    # === ショートカット設定タブ ===
    # 翻訳ホットキー
    shortcut_frame = ttk.LabelFrame(shortcut_tab, text="翻訳ホットキー設定", padding=15)
    shortcut_frame.pack(fill="x", pady=10)

    modifiers_frame = ttk.Frame(shortcut_frame)
    modifiers_frame.pack(fill="x", pady=5)
    ttk.Label(modifiers_frame, text="修飾キー:").pack(side="left", padx=(0, 10))

    hotkey_ctrl_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'hotkey_ctrl', True))
    hotkey_alt_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'hotkey_alt', True))
    hotkey_shift_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'hotkey_shift', False))

    ttk.Checkbutton(modifiers_frame, text="Ctrl", variable=hotkey_ctrl_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(modifiers_frame, text="Alt", variable=hotkey_alt_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(modifiers_frame, text="Shift", variable=hotkey_shift_var).pack(side="left")

    key_frame = ttk.Frame(shortcut_frame)
    key_frame.pack(fill="x", pady=10)
    ttk.Label(key_frame, text="キー:").pack(side="left", padx=(0, 10))

    hotkey_key_var = tk.StringVar(value=config.get('Settings', 'hotkey_key', fallback='d'))
    key_combo = ttk.Combobox(key_frame, textvariable=hotkey_key_var, values=KEY_OPTIONS, width=15)
    key_combo.pack(side="left")

    # 辞書ホットキー
    dict_shortcut_frame = ttk.LabelFrame(shortcut_tab, text="辞書検索ホットキー設定", padding=15)
    dict_shortcut_frame.pack(fill="x", pady=(20, 10))

    dict_modifiers_frame = ttk.Frame(dict_shortcut_frame)
    dict_modifiers_frame.pack(fill="x", pady=5)
    ttk.Label(dict_modifiers_frame, text="修飾キー:").pack(side="left", padx=(0, 10))

    dict_hotkey_ctrl_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'dict_hotkey_ctrl', True))
    dict_hotkey_alt_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'dict_hotkey_alt', True))
    dict_hotkey_shift_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'dict_hotkey_shift', False))

    ttk.Checkbutton(dict_modifiers_frame, text="Ctrl", variable=dict_hotkey_ctrl_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(dict_modifiers_frame, text="Alt", variable=dict_hotkey_alt_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(dict_modifiers_frame, text="Shift", variable=dict_hotkey_shift_var).pack(side="left")

    dict_key_frame = ttk.Frame(dict_shortcut_frame)
    dict_key_frame.pack(fill="x", pady=10)
    ttk.Label(dict_key_frame, text="キー:").pack(side="left", padx=(0, 10))

    dict_hotkey_key_var = tk.StringVar(value=config.get('Settings', 'dict_hotkey_key', fallback='j'))
    dict_key_combo = ttk.Combobox(dict_key_frame, textvariable=dict_hotkey_key_var, values=KEY_OPTIONS, width=15)
    dict_key_combo.pack(side="left")

    # 音声ホットキー
    speech_shortcut_frame = ttk.LabelFrame(shortcut_tab, text="音声出力ホットキー設定", padding=15)
    speech_shortcut_frame.pack(fill="x", pady=(20, 10))

    speech_modifiers_frame = ttk.Frame(speech_shortcut_frame)
    speech_modifiers_frame.pack(fill="x", pady=5)
    ttk.Label(speech_modifiers_frame, text="修飾キー:").pack(side="left", padx=(0, 10))

    speech_hotkey_ctrl_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'speech_hotkey_ctrl', True))
    speech_hotkey_alt_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'speech_hotkey_alt', True))
    speech_hotkey_shift_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'speech_hotkey_shift', False))

    ttk.Checkbutton(speech_modifiers_frame, text="Ctrl", variable=speech_hotkey_ctrl_var).pack(side="left",
                                                                                                padx=(0, 10))
    ttk.Checkbutton(speech_modifiers_frame, text="Alt", variable=speech_hotkey_alt_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(speech_modifiers_frame, text="Shift", variable=speech_hotkey_shift_var).pack(side="left")

    speech_key_frame = ttk.Frame(speech_shortcut_frame)
    speech_key_frame.pack(fill="x", pady=10)
    ttk.Label(speech_key_frame, text="キー:").pack(side="left", padx=(0, 10))

    speech_hotkey_key_var = tk.StringVar(value=config.get('Settings', 'speech_hotkey_key', fallback='t'))
    speech_key_combo = ttk.Combobox(speech_key_frame, textvariable=speech_hotkey_key_var, values=KEY_OPTIONS, width=15)
    speech_key_combo.pack(side="left")

    # === 音声設定タブ ===
    speech_frame = ttk.LabelFrame(speech_tab, text="音声出力機能", padding=15)
    speech_frame.pack(fill="x", pady=10)

    use_speech_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'use_speech', True))
    ttk.Checkbutton(speech_frame, text="音声出力機能を有効にする", variable=use_speech_var).pack(anchor="w", pady=5)

    volume_frame = ttk.Frame(speech_frame)
    volume_frame.pack(fill="x", pady=10)
    ttk.Label(volume_frame, text="音量:").pack(side="left", padx=(0, 10))

    speech_volume_var = tk.DoubleVar(value=float(config.get('Settings', 'speech_volume', fallback='1.0')))
    volume_scale = ttk.Scale(volume_frame, from_=0.0, to=1.0, length=200,
                             orient="horizontal", variable=speech_volume_var)
    volume_scale.pack(side="left", padx=(0, 10))

    volume_label = ttk.Label(volume_frame, text=f"{int(speech_volume_var.get() * 100)}%")
    volume_label.pack(side="left")

    def update_volume_label(*args):
        volume_label.config(text=f"{int(speech_volume_var.get() * 100)}%")

    speech_volume_var.trace_add("write", update_volume_label)

    # === 表示設定タブ ===
    ui_frame = ttk.LabelFrame(ui_tab, text="表示言語設定", padding=15)
    ui_frame.pack(fill="x", pady=10)

    response_language_var = tk.StringVar(value=config.get('Settings', 'response_language', fallback='JA'))
    ttk.Label(ui_frame, text="メッセージとラベルの言語:").pack(anchor="w", pady=(0, 5))

    lang_frame = ttk.Frame(ui_frame)
    lang_frame.pack(fill="x", pady=5)
    ttk.Radiobutton(lang_frame, text="日本語", variable=response_language_var, value="JA").pack(side="left",
                                                                                                 padx=(0, 20))
    ttk.Radiobutton(lang_frame, text="English", variable=response_language_var, value="EN").pack(side="left")

    # 文字数制限
    limit_frame = ttk.LabelFrame(ui_tab, text="翻訳文字数制限", padding=15)
    limit_frame.pack(fill="x", pady=10)

    ttk.Label(limit_frame, text="一度に翻訳できる最大文字数:").pack(anchor="w", pady=(0, 5))
    max_length_options = ["100", "500", "1000", "2000", "3000"]
    max_length_var = tk.StringVar(value=config.get('Settings', 'max_translation_length', fallback='1000'))
    max_length_combo = ttk.Combobox(limit_frame, textvariable=max_length_var,
                                    values=max_length_options, width=10, state="readonly")
    max_length_combo.pack(anchor="w", pady=5)

    def save_settings():
        """設定を保存"""
        # 修飾キーのチェック
        if not (hotkey_ctrl_var.get() or hotkey_alt_var.get() or hotkey_shift_var.get()):
            messagebox.showerror("エラー", "翻訳用に少なくとも1つの修飾キーを選択してください。")
            return

        if not (dict_hotkey_ctrl_var.get() or dict_hotkey_alt_var.get() or dict_hotkey_shift_var.get()):
            messagebox.showerror("エラー", "辞書検索用に少なくとも1つの修飾キーを選択してください。")
            return

        if not (speech_hotkey_ctrl_var.get() or speech_hotkey_alt_var.get() or speech_hotkey_shift_var.get()):
            messagebox.showerror("エラー", "音声出力用に少なくとも1つの修飾キーを選択してください。")
            return

        # 区切り行のチェック
        if '---' in hotkey_key_var.get():
            messagebox.showerror("エラー", "有効なキーを選択してください。")
            return

        if '---' in dict_hotkey_key_var.get():
            messagebox.showerror("エラー", "辞書検索用に有効なキーを選択してください。")
            return

        if '---' in speech_hotkey_key_var.get():
            messagebox.showerror("エラー", "音声出力用に有効なキーを選択してください。")
            return

        # 設定を保存
        if not config.has_section('Settings'):
            config.add_section('Settings')

        config['Settings']['use_deepl'] = str(use_deepl_var.get())
        config['Settings']['auto_add_to_vocabulary'] = str(auto_add_vocab_var.get())
        config['Settings']['deepl_api_key'] = api_key_var.get().strip()
        config['Settings']['claude_api_key'] = claude_api_key_var.get().strip()
        config['Settings']['claude_prompt_template'] = prompt_text.get("1.0", tk.END).strip()
        config['Settings']['response_language'] = response_language_var.get()
        config['Settings']['max_translation_length'] = max_length_var.get()

        # ホットキー設定
        config['Settings']['hotkey_ctrl'] = str(hotkey_ctrl_var.get())
        config['Settings']['hotkey_alt'] = str(hotkey_alt_var.get())
        config['Settings']['hotkey_shift'] = str(hotkey_shift_var.get())
        config['Settings']['hotkey_key'] = hotkey_key_var.get()

        config['Settings']['dict_hotkey_ctrl'] = str(dict_hotkey_ctrl_var.get())
        config['Settings']['dict_hotkey_alt'] = str(dict_hotkey_alt_var.get())
        config['Settings']['dict_hotkey_shift'] = str(dict_hotkey_shift_var.get())
        config['Settings']['dict_hotkey_key'] = dict_hotkey_key_var.get()

        config['Settings']['use_speech'] = str(use_speech_var.get())
        config['Settings']['speech_volume'] = str(speech_volume_var.get())
        config['Settings']['speech_hotkey_ctrl'] = str(speech_hotkey_ctrl_var.get())
        config['Settings']['speech_hotkey_alt'] = str(speech_hotkey_alt_var.get())
        config['Settings']['speech_hotkey_shift'] = str(speech_hotkey_shift_var.get())
        config['Settings']['speech_hotkey_key'] = speech_hotkey_key_var.get()

        try:
            config_file = get_config_file_path()
            with open(config_file, 'w', encoding='utf-8') as f:
                config.write(f)

            app.restart_hotkey_listener()
            messagebox.showinfo("設定", "設定を保存しました")
            app.update_status('settings_saved')
        except Exception as e:
            messagebox.showerror("エラー", f"設定の保存中にエラーが発生しました: {e}")

        settings_window.destroy()

    # ボタン
    ttk.Button(button_frame, text="保存", command=save_settings).pack(side="right", padx=5)
    ttk.Button(button_frame, text="キャンセル", command=settings_window.destroy).pack(side="right", padx=5)
