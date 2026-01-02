# ClipboardTranslator v1.20 - Settings Dialog (Multi-language)
import os
import platform
import sys
import re
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import webbrowser
import requests

# macOS判定（キーラベルを変更するため）
IS_MACOS = platform.system() == 'Darwin'
CTRL_LABEL = "Cmd" if IS_MACOS else "Ctrl"
ALT_LABEL = "Option" if IS_MACOS else "Alt"

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.constants import DEEPL_URL, KEY_OPTIONS, DEFAULT_SETTINGS, TUTOR_MODEL_OPTIONS, LANGUAGE_OPTIONS, UI_LANGUAGE_OPTIONS, MESSAGES, get_message, get_default_claude_prompt, get_default_tutor_prompt
from config.settings import config, get_config_file_path
from core.translation import query_claude_api


def _center_window(window, width, height):
    """ウィンドウをモニター中央に配置"""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def show_settings_dialog(app):
    """設定ダイアログを表示"""
    # 現在のUI言語を取得
    lang = config.get('Settings', 'response_language', fallback='EN')

    # ヘルパー関数: 現在の言語でメッセージを取得
    def msg(key):
        return get_message(key, lang)

    settings_window = tk.Toplevel(app)
    settings_window.title(msg('settings_title'))
    _center_window(settings_window, 600, 700)
    settings_window.minsize(600, 650)
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
    tutor_tab = ttk.Frame(tab_control, padding=10)
    ui_tab = ttk.Frame(tab_control, padding=10)

    tab_control.add(translation_tab, text=f" {msg('tab_translation')} ")
    tab_control.add(api_tab, text=f" {msg('tab_api')} ")
    tab_control.add(shortcut_tab, text=f" {msg('tab_shortcut')} ")
    tab_control.add(speech_tab, text=f" {msg('tab_speech')} ")
    tab_control.add(tutor_tab, text=f" {msg('tab_tutor')} ")
    tab_control.add(ui_tab, text=f" {msg('tab_display')} ")

    # === 翻訳設定タブ ===
    translation_frame = ttk.LabelFrame(translation_tab, text=msg('translation_options'), padding=15)
    translation_frame.pack(fill="x", pady=10)

    use_deepl_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'use_deepl', True))
    ttk.Checkbutton(translation_frame, text=msg('use_deepl'), variable=use_deepl_var).pack(anchor="w", pady=5)

    auto_add_vocab_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'auto_add_to_vocabulary', False))
    ttk.Checkbutton(translation_frame, text=msg('auto_add_vocab'),
                    variable=auto_add_vocab_var).pack(anchor="w", pady=5)

    # === 翻訳言語設定 (v1.20) ===
    lang_setting_frame = ttk.LabelFrame(translation_tab, text=msg('target_language_section'), padding=15)
    lang_setting_frame.pack(fill="x", pady=10)

    # 言語選択
    target_lang_frame = ttk.Frame(lang_setting_frame)
    target_lang_frame.pack(fill="x", pady=5)
    ttk.Label(target_lang_frame, text=msg('target_language_label')).pack(side="left", padx=(0, 10))

    # 言語オプションの表示名リスト作成
    lang_display_values = [f"{code} - {name}" for code, name in LANGUAGE_OPTIONS]
    lang_code_map = {f"{code} - {name}": code for code, name in LANGUAGE_OPTIONS}
    lang_display_map = {code: f"{code} - {name}" for code, name in LANGUAGE_OPTIONS}

    current_target_lang = config.get('Settings', 'target_language', fallback='EN')
    target_lang_var = tk.StringVar(value=lang_display_map.get(current_target_lang, 'EN - 英語 / English'))

    target_lang_combo = ttk.Combobox(target_lang_frame, textvariable=target_lang_var,
                                      values=lang_display_values, width=30, state="readonly")
    target_lang_combo.pack(side="left")

    # 自動検出オプション
    auto_detect_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'auto_detect_source', True))
    ttk.Checkbutton(lang_setting_frame, text=msg('auto_detect_source'),
                    variable=auto_detect_var).pack(anchor="w", pady=(10, 5))

    # === API設定タブ ===
    # DeepL API
    api_frame = ttk.LabelFrame(api_tab, text=msg('deepl_api_settings'), padding=15)
    api_frame.pack(fill="x", pady=10)

    ttk.Label(api_frame, text=msg('deepl_api_key')).pack(anchor="w", pady=(0, 5))
    api_key_var = tk.StringVar(value=config.get('Settings', 'deepl_api_key', fallback=''))
    api_key_entry = ttk.Entry(api_frame, textvariable=api_key_var, width=40)
    api_key_entry.pack(fill="x")

    # Claude API
    claude_frame = ttk.LabelFrame(api_tab, text=msg('claude_api_settings'), padding=15)
    claude_frame.pack(fill="x", pady=(20, 10))

    ttk.Label(claude_frame, text=msg('claude_api_key')).pack(anchor="w", pady=(0, 5))
    claude_api_key_var = tk.StringVar(value=config.get('Settings', 'claude_api_key', fallback=''))
    claude_api_key_entry = ttk.Entry(claude_frame, textvariable=claude_api_key_var, width=40)
    claude_api_key_entry.pack(fill="x")

    ttk.Label(claude_frame, text=msg('prompt_template')).pack(anchor="w", pady=(10, 5))
    prompt_text = tk.Text(claude_frame, width=40, height=8, wrap=tk.WORD)
    prompt_text.pack(fill="x")
    prompt_text.insert("1.0", config.get('Settings', 'claude_prompt_template', fallback=''))

    # 辞書プロンプトリセットボタン
    claude_btn_frame = ttk.Frame(claude_frame)
    claude_btn_frame.pack(fill="x", pady=(5, 0))

    def reset_claude_prompt():
        """辞書検索プロンプトを現在のUI言語のデフォルトに戻す"""
        prompt_text.delete("1.0", tk.END)
        prompt_text.insert("1.0", get_default_claude_prompt(lang))

    ttk.Button(claude_btn_frame, text=msg('reset_default'), command=reset_claude_prompt).pack(side="right")

    # === ショートカット設定タブ ===
    # 翻訳ホットキー
    shortcut_frame = ttk.LabelFrame(shortcut_tab, text=msg('hotkey_translation'), padding=15)
    shortcut_frame.pack(fill="x", pady=10)

    modifiers_frame = ttk.Frame(shortcut_frame)
    modifiers_frame.pack(fill="x", pady=5)
    ttk.Label(modifiers_frame, text=msg('modifier_keys')).pack(side="left", padx=(0, 10))

    hotkey_ctrl_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'hotkey_ctrl', True))
    hotkey_alt_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'hotkey_alt', True))
    hotkey_shift_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'hotkey_shift', False))

    ttk.Checkbutton(modifiers_frame, text=CTRL_LABEL, variable=hotkey_ctrl_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(modifiers_frame, text=ALT_LABEL, variable=hotkey_alt_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(modifiers_frame, text="Shift", variable=hotkey_shift_var).pack(side="left")

    key_frame = ttk.Frame(shortcut_frame)
    key_frame.pack(fill="x", pady=10)
    ttk.Label(key_frame, text=msg('key_label')).pack(side="left", padx=(0, 10))

    hotkey_key_var = tk.StringVar(value=config.get('Settings', 'hotkey_key', fallback='d'))
    key_combo = ttk.Combobox(key_frame, textvariable=hotkey_key_var, values=KEY_OPTIONS, width=15)
    key_combo.pack(side="left")

    # 辞書ホットキー
    dict_shortcut_frame = ttk.LabelFrame(shortcut_tab, text=msg('hotkey_dictionary'), padding=15)
    dict_shortcut_frame.pack(fill="x", pady=(20, 10))

    dict_modifiers_frame = ttk.Frame(dict_shortcut_frame)
    dict_modifiers_frame.pack(fill="x", pady=5)
    ttk.Label(dict_modifiers_frame, text=msg('modifier_keys')).pack(side="left", padx=(0, 10))

    dict_hotkey_ctrl_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'dict_hotkey_ctrl', True))
    dict_hotkey_alt_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'dict_hotkey_alt', True))
    dict_hotkey_shift_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'dict_hotkey_shift', False))

    ttk.Checkbutton(dict_modifiers_frame, text=CTRL_LABEL, variable=dict_hotkey_ctrl_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(dict_modifiers_frame, text=ALT_LABEL, variable=dict_hotkey_alt_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(dict_modifiers_frame, text="Shift", variable=dict_hotkey_shift_var).pack(side="left")

    dict_key_frame = ttk.Frame(dict_shortcut_frame)
    dict_key_frame.pack(fill="x", pady=10)
    ttk.Label(dict_key_frame, text=msg('key_label')).pack(side="left", padx=(0, 10))

    dict_hotkey_key_var = tk.StringVar(value=config.get('Settings', 'dict_hotkey_key', fallback='j'))
    dict_key_combo = ttk.Combobox(dict_key_frame, textvariable=dict_hotkey_key_var, values=KEY_OPTIONS, width=15)
    dict_key_combo.pack(side="left")

    # 音声ホットキー
    speech_shortcut_frame = ttk.LabelFrame(shortcut_tab, text=msg('hotkey_speech'), padding=15)
    speech_shortcut_frame.pack(fill="x", pady=(20, 10))

    speech_modifiers_frame = ttk.Frame(speech_shortcut_frame)
    speech_modifiers_frame.pack(fill="x", pady=5)
    ttk.Label(speech_modifiers_frame, text=msg('modifier_keys')).pack(side="left", padx=(0, 10))

    speech_hotkey_ctrl_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'speech_hotkey_ctrl', True))
    speech_hotkey_alt_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'speech_hotkey_alt', True))
    speech_hotkey_shift_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'speech_hotkey_shift', False))

    ttk.Checkbutton(speech_modifiers_frame, text=CTRL_LABEL, variable=speech_hotkey_ctrl_var).pack(side="left",
                                                                                                padx=(0, 10))
    ttk.Checkbutton(speech_modifiers_frame, text=ALT_LABEL, variable=speech_hotkey_alt_var).pack(side="left", padx=(0, 10))
    ttk.Checkbutton(speech_modifiers_frame, text="Shift", variable=speech_hotkey_shift_var).pack(side="left")

    speech_key_frame = ttk.Frame(speech_shortcut_frame)
    speech_key_frame.pack(fill="x", pady=10)
    ttk.Label(speech_key_frame, text=msg('key_label')).pack(side="left", padx=(0, 10))

    speech_hotkey_key_var = tk.StringVar(value=config.get('Settings', 'speech_hotkey_key', fallback='t'))
    speech_key_combo = ttk.Combobox(speech_key_frame, textvariable=speech_hotkey_key_var, values=KEY_OPTIONS, width=15)
    speech_key_combo.pack(side="left")

    # === 音声設定タブ ===
    speech_frame = ttk.LabelFrame(speech_tab, text=msg('speech_output'), padding=15)
    speech_frame.pack(fill="x", pady=10)

    use_speech_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'use_speech', True))
    ttk.Checkbutton(speech_frame, text=msg('enable_speech'), variable=use_speech_var).pack(anchor="w", pady=5)

    volume_frame = ttk.Frame(speech_frame)
    volume_frame.pack(fill="x", pady=10)
    ttk.Label(volume_frame, text=msg('volume_label')).pack(side="left", padx=(0, 10))

    speech_volume_var = tk.DoubleVar(value=float(config.get('Settings', 'speech_volume', fallback='1.0')))
    volume_scale = ttk.Scale(volume_frame, from_=0.0, to=1.0, length=200,
                             orient="horizontal", variable=speech_volume_var)
    volume_scale.pack(side="left", padx=(0, 10))

    volume_label = ttk.Label(volume_frame, text=f"{int(speech_volume_var.get() * 100)}%")
    volume_label.pack(side="left")

    def update_volume_label(*args):
        volume_label.config(text=f"{int(speech_volume_var.get() * 100)}%")

    speech_volume_var.trace_add("write", update_volume_label)

    # === 家庭教師設定タブ ===
    tutor_enable_frame = ttk.LabelFrame(tutor_tab, text=msg('tutor_mode'), padding=15)
    tutor_enable_frame.pack(fill="x", pady=10)

    tutor_enabled_var = tk.BooleanVar(value=app.get_config_bool('Settings', 'tutor_enabled', True))
    ttk.Checkbutton(tutor_enable_frame, text=msg('enable_tutor'),
                    variable=tutor_enabled_var).pack(anchor="w", pady=5)

    # モデル選択
    model_frame = ttk.Frame(tutor_enable_frame)
    model_frame.pack(fill="x", pady=(10, 5))
    ttk.Label(model_frame, text=msg('model_label')).pack(side="left", padx=(0, 10))

    tutor_model_var = tk.StringVar(value=config.get('Settings', 'tutor_model', fallback='sonnet'))
    model_values = [opt[0] for opt in TUTOR_MODEL_OPTIONS]
    model_display = {opt[0]: opt[1] for opt in TUTOR_MODEL_OPTIONS}
    tutor_model_combo = ttk.Combobox(model_frame, textvariable=tutor_model_var,
                                      values=model_values, width=35, state="readonly")
    tutor_model_combo.pack(side="left")

    # モデル説明ラベル
    model_desc_label = ttk.Label(tutor_enable_frame, text=model_display.get(tutor_model_var.get(), ''),
                                  foreground="#666666")
    model_desc_label.pack(anchor="w", pady=(0, 5))

    def update_model_desc(*args):
        model_desc_label.config(text=model_display.get(tutor_model_var.get(), ''))

    tutor_model_var.trace_add("write", update_model_desc)

    # システムプロンプト設定
    tutor_prompt_frame = ttk.LabelFrame(tutor_tab, text=msg('system_prompt'), padding=15)
    tutor_prompt_frame.pack(fill="both", expand=True, pady=10)

    # 会話履歴設定（上部に配置）
    history_frame = ttk.Frame(tutor_prompt_frame)
    history_frame.pack(fill="x", pady=(0, 10))
    ttk.Label(history_frame, text=msg('context_history')).pack(side="left", padx=(0, 10))

    tutor_history_var = tk.StringVar(value=config.get('Settings', 'tutor_max_history', fallback='10'))
    history_options = ["3", "5", "10", "15", "20"]
    tutor_history_combo = ttk.Combobox(history_frame, textvariable=tutor_history_var,
                                        values=history_options, width=5, state="readonly")
    tutor_history_combo.pack(side="left")
    ttk.Label(history_frame, text=msg('context_history_suffix')).pack(side="left", padx=(5, 0))

    # プロンプトラベル
    ttk.Label(tutor_prompt_frame, text=msg('tutor_prompt_desc')).pack(anchor="w", pady=(0, 5))

    # スクロールバー付きテキストエリア
    tutor_prompt_container = ttk.Frame(tutor_prompt_frame)
    tutor_prompt_container.pack(fill="both", expand=True)

    tutor_prompt_scrollbar = ttk.Scrollbar(tutor_prompt_container)
    tutor_prompt_scrollbar.pack(side="right", fill="y")

    tutor_prompt_text = tk.Text(tutor_prompt_container, width=50, height=10, wrap=tk.WORD,
                                 yscrollcommand=tutor_prompt_scrollbar.set)
    tutor_prompt_text.pack(side="left", fill="both", expand=True)
    tutor_prompt_scrollbar.config(command=tutor_prompt_text.yview)

    default_tutor_prompt = DEFAULT_SETTINGS.get('tutor_system_prompt', '')
    current_tutor_prompt = config.get('Settings', 'tutor_system_prompt', fallback=default_tutor_prompt)
    tutor_prompt_text.insert("1.0", current_tutor_prompt)

    # リセットボタン
    tutor_btn_frame = ttk.Frame(tutor_prompt_frame)
    tutor_btn_frame.pack(fill="x", pady=(10, 0))

    def reset_tutor_prompt():
        """プロンプトを現在のUI言語のデフォルトに戻す"""
        tutor_prompt_text.delete("1.0", tk.END)
        tutor_prompt_text.insert("1.0", get_default_tutor_prompt(lang))

    ttk.Button(tutor_btn_frame, text=msg('reset_default'), command=reset_tutor_prompt).pack(side="right")

    # === 表示設定タブ ===
    ui_frame = ttk.LabelFrame(ui_tab, text=msg('display_language'), padding=15)
    ui_frame.pack(fill="x", pady=10)

    # UI言語選択（ドロップダウン）
    current_ui_lang = config.get('Settings', 'response_language', fallback='EN')
    response_language_var = tk.StringVar(value=current_ui_lang)

    # UI言語オプションの表示名リスト作成
    ui_lang_display_values = [f"{name}" for code, name in UI_LANGUAGE_OPTIONS]
    ui_lang_code_map = {name: code for code, name in UI_LANGUAGE_OPTIONS}
    ui_lang_display_map = {code: name for code, name in UI_LANGUAGE_OPTIONS}

    ttk.Label(ui_frame, text=msg('ui_language_label')).pack(anchor="w", pady=(0, 5))

    lang_frame = ttk.Frame(ui_frame)
    lang_frame.pack(fill="x", pady=5)

    ui_lang_combo = ttk.Combobox(lang_frame,
                                  values=ui_lang_display_values,
                                  width=25,
                                  state="readonly")
    # 現在の言語を選択状態に
    current_display = ui_lang_display_map.get(current_ui_lang, 'English')
    ui_lang_combo.set(current_display)
    ui_lang_combo.pack(side="left")

    # 即時反映のためのコールバック
    def on_ui_language_change(event=None):
        """UI言語変更時に即時保存・反映し、ダイアログを再起動"""
        selected_display = ui_lang_combo.get()
        selected_code = ui_lang_code_map.get(selected_display, 'EN')
        response_language_var.set(selected_code)

        # 設定を即時保存
        if not config.has_section('Settings'):
            config.add_section('Settings')
        config['Settings']['response_language'] = selected_code

        # 翻訳先言語もUI言語と同じに設定
        config['Settings']['target_language'] = selected_code

        # プロンプトも新しい言語のデフォルトに更新
        config['Settings']['claude_prompt_template'] = get_default_claude_prompt(selected_code)
        config['Settings']['tutor_system_prompt'] = get_default_tutor_prompt(selected_code)

        try:
            config_file = get_config_file_path()
            with open(config_file, 'w', encoding='utf-8') as f:
                config.write(f)

            # メインアプリのUI更新をトリガー
            if hasattr(app, 'update_ui_language'):
                app.update_ui_language(selected_code)

            # ステータス更新
            app.update_status('ui_language_changed')

            # ダイアログを閉じて再度開く（UI言語を即時反映）
            settings_window.destroy()
            show_settings_dialog(app)

        except Exception as e:
            print(f"UI language save error: {e}")

    ui_lang_combo.bind('<<ComboboxSelected>>', on_ui_language_change)

    # 文字数制限
    limit_frame = ttk.LabelFrame(ui_tab, text=msg('char_limit_section'), padding=15)
    limit_frame.pack(fill="x", pady=10)

    ttk.Label(limit_frame, text=msg('char_limit_label')).pack(anchor="w", pady=(0, 5))
    max_length_options = ["100", "500", "1000", "2000", "3000"]
    max_length_var = tk.StringVar(value=config.get('Settings', 'max_translation_length', fallback='1000'))
    max_length_combo = ttk.Combobox(limit_frame, textvariable=max_length_var,
                                    values=max_length_options, width=10, state="readonly")
    max_length_combo.pack(anchor="w", pady=5)

    def save_settings():
        """設定を保存"""
        # 修飾キーのチェック
        if not (hotkey_ctrl_var.get() or hotkey_alt_var.get() or hotkey_shift_var.get()):
            messagebox.showerror("Error", msg('error_modifier_translation'))
            return

        if not (dict_hotkey_ctrl_var.get() or dict_hotkey_alt_var.get() or dict_hotkey_shift_var.get()):
            messagebox.showerror("Error", msg('error_modifier_dictionary'))
            return

        if not (speech_hotkey_ctrl_var.get() or speech_hotkey_alt_var.get() or speech_hotkey_shift_var.get()):
            messagebox.showerror("Error", msg('error_modifier_speech'))
            return

        # 区切り行のチェック
        if '---' in hotkey_key_var.get():
            messagebox.showerror("Error", msg('error_invalid_key'))
            return

        if '---' in dict_hotkey_key_var.get():
            messagebox.showerror("Error", msg('error_invalid_key'))
            return

        if '---' in speech_hotkey_key_var.get():
            messagebox.showerror("Error", msg('error_invalid_key'))
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

        # 翻訳言語設定 (v1.20)
        selected_lang_display = target_lang_var.get()
        config['Settings']['target_language'] = lang_code_map.get(selected_lang_display, 'EN')
        config['Settings']['auto_detect_source'] = str(auto_detect_var.get())

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

        # 家庭教師設定
        config['Settings']['tutor_enabled'] = str(tutor_enabled_var.get())
        config['Settings']['tutor_model'] = tutor_model_var.get()
        config['Settings']['tutor_system_prompt'] = tutor_prompt_text.get("1.0", tk.END).strip()
        config['Settings']['tutor_max_history'] = tutor_history_var.get()

        try:
            config_file = get_config_file_path()
            with open(config_file, 'w', encoding='utf-8') as f:
                config.write(f)

            app.restart_hotkey_listener()
            messagebox.showinfo(msg('settings_title'), msg('settings_saved'))
            app.update_status('settings_saved')
        except Exception as e:
            messagebox.showerror("Error", get_message('error_save', lang, error=str(e)))

        settings_window.destroy()

    # ボタン
    ttk.Button(button_frame, text=msg('save_button'), command=save_settings).pack(side="right", padx=5)
    ttk.Button(button_frame, text=msg('cancel_button'), command=settings_window.destroy).pack(side="right", padx=5)
