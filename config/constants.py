# ClipboardTranslator v1.10 - Constants
# 定数定義

# API Endpoints
DEEPL_URL = 'https://api-free.deepl.com/v2/translate'
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# Default Settings
DEFAULT_SETTINGS = {
    'use_deepl': 'True',
    'response_language': 'JA',
    'deepl_api_key': '',
    'claude_api_key': '',
    'claude_prompt_template': '''単語:{word}
1.意味（簡潔な辞書的定義）
2.学習者の理解を深める（英単語の場合、単語の分解[例:al-levi-ate、
接頭辞:「al-」、強調や方向を示す接頭辞（ここでは「～へ、強く」の意味）
語幹:「levi-」、「lev」 はラテン語の levis（軽い）に由来し、「軽くする、持ち上げる」の意味を持つ
接尾辞:「-ate」、動詞を作る接尾辞（「～する」という意味）]）
3.語法（基本の使い方）
4.類義語、対義語の紹介と簡潔な辞書的意味
出力は簡潔に。
''',
    'hotkey_ctrl': 'True',
    'hotkey_alt': 'True',
    'hotkey_shift': 'False',
    'hotkey_key': 'd',
    'dict_hotkey_ctrl': 'True',
    'dict_hotkey_alt': 'True',
    'dict_hotkey_shift': 'False',
    'dict_hotkey_key': 'j',
    'use_speech': 'True',
    'speech_volume': '1.0',
    'speech_hotkey_ctrl': 'True',
    'speech_hotkey_alt': 'True',
    'speech_hotkey_shift': 'False',
    'speech_hotkey_key': 't',
    'max_translation_length': '1000',
    'auto_add_to_vocabulary': 'False',
    # 家庭教師モード設定
    'tutor_enabled': 'True',
    'tutor_model': 'sonnet',
    'tutor_system_prompt': '''あなたはユーザー専属の家庭教師です。
以下のルールに従って返答してください：

1. 教科書調にしない - フレンドリーに話す
2. 過去の履歴を「覚えている体」で話す
3. 共感を最初に入れる - ユーザーの気持ちに寄り添う
4. 長文説明は禁止 - 簡潔に、わかりやすく
5. 必要なら質問で返す - 理解度を確認する
6. 励ましの言葉を適度に入れる''',
    'tutor_max_history': '10',
}

# 家庭教師モデル選択肢
TUTOR_MODEL_OPTIONS = [
    ('sonnet', 'Claude Sonnet 4.5 (推奨・バランス型)'),
    ('haiku', 'Claude Haiku 4.5 (高速・低コスト)'),
    ('opus', 'Claude Opus 4.5 (最高性能・高コスト)'),
]

# UI Messages (Multi-language)
MESSAGES = {
    'JA': {
        'clipboard_empty': 'クリップボードが空です',
        'waiting': '待機中...',
        'translation_in_progress': '翻訳中...',
        'offline_dict_used': 'オフライン辞書を使用しました',
        'local_dict_used': 'ローカル辞書を使用しました',
        'claude_api_used': 'Claude APIを使用しました',
        'no_internet': 'インターネット接続がありません',
        'translation_complete': '翻訳完了',
        'translation_failed': '翻訳に失敗しました',
        'service_disabled': '翻訳サービスが無効です',
        'error_occurred': 'エラーが発生しました',
        'deepl_failed_offline': 'DeepL失敗 - オフライン辞書を使用',
        'deepl_failed_local': 'DeepL失敗 - ローカル辞書を使用',
        'no_conversion': '変換なし',
        'settings_saved': '設定を保存しました',
        'text_copied': 'テキストをコピーしました',
        'no_text_selected': 'テキストが選択されていません',
        'all_text_selected': 'すべてのテキストを選択しました',
        'text_cleared': 'テキストをクリアしました',
        'font_size': 'フォントサイズ:',
        'script_running': 'スクリプトが実行中です...',
        'input_label': '【入力】',
        'translated_label': '【翻訳結果】',
        'dict_api_label': '【翻訳結果】',
        'local_dict_label': '【翻訳結果 (ローカル辞書)】',
        'no_conversion_label': '【翻訳結果 (変換なし)】',
        'dictionary_lookup_complete': '辞書検索完了',
        'word_not_in_dictionary': '辞書に登録されていません',
        'dict_meaning_label': '【意味】',
        'dict_only_for_words': '辞書検索は単語のみ対応しています。通常の翻訳ホットキーをご使用ください。',
        'claude_lookup_complete': 'Claude検索完了',
        'text_too_long': '文字数制限（{max_length}文字）を超えています。翻訳を中止しました。',
        'claude_api_error': 'APIが機能していないため辞書検索に失敗しました。',
        'cache_used': '[キャッシュから]'
    },
    'EN': {
        'clipboard_empty': 'Clipboard is empty',
        'waiting': 'Waiting...',
        'translation_in_progress': 'Translating...',
        'offline_dict_used': 'Used offline dictionary',
        'local_dict_used': 'Used local dictionary',
        'claude_api_used': 'Used Claude API',
        'no_internet': 'No internet connection',
        'translation_complete': 'Translation complete',
        'translation_failed': 'Translation failed',
        'service_disabled': 'Translation service is disabled',
        'error_occurred': 'An error occurred',
        'deepl_failed_offline': 'DeepL failed - Using offline dictionary',
        'deepl_failed_local': 'DeepL failed - Using local dictionary',
        'no_conversion': 'No conversion',
        'settings_saved': 'Settings saved',
        'text_copied': 'Text copied',
        'no_text_selected': 'No text selected',
        'all_text_selected': 'All text selected',
        'text_cleared': 'Text cleared',
        'font_size': 'Font size:',
        'script_running': 'Script is running...',
        'input_label': '【Input】',
        'translated_label': '【Translated】',
        'dict_api_label': '【Translated】',
        'local_dict_label': '【Translated (Local Dictionary)】',
        'no_conversion_label': '【Translated (No Conversion)】',
        'dictionary_lookup_complete': 'Dictionary lookup complete',
        'word_not_in_dictionary': 'Word not found in dictionary',
        'dict_meaning_label': '【Meaning】',
        'dict_only_for_words': 'Dictionary lookup is only for single words. Please use the normal translation hotkey.',
        'claude_lookup_complete': 'Claude lookup complete',
        'text_too_long': 'Character limit ({max_length}) exceeded. Translation aborted.',
        'claude_api_error': 'Dictionary lookup failed because the API is not functioning.',
        'cache_used': '[From cache]'
    }
}

# Hotkey Options
KEY_OPTIONS = [
    '--- アルファベット ---',
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
    'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
    '--- 数字 ---',
    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
    '--- ファンクションキー ---',
    'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7', 'f8', 'f9', 'f10', 'f11', 'f12'
]

# Version Info
VERSION = "1.10"
APP_TITLE = "ClipTrans"
