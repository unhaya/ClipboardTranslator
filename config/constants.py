# ClipboardTranslator v1.20 - Constants
# 定数定義

# API Endpoints
DEEPL_URL = 'https://api-free.deepl.com/v2/translate'
CLAUDE_API_URL = "https://api.anthropic.com/v1/messages"

# Default Settings
DEFAULT_SETTINGS = {
    'use_deepl': 'True',
    'response_language': 'EN',  # v1.20: デフォルトUI言語を英語に
    'target_language': 'EN',  # v1.20: デフォルト翻訳先言語
    'auto_detect_source': 'True',  # v1.20: ソース言語自動検出
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
※出力は簡潔に。Markdown形式（見出し、リスト、太字、テーブル等）使用可。
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
    'tutor_system_prompt': '''丁寧かつ親しみやすい家庭教師として回答。簡潔に。Markdown可。''',
    'tutor_max_history': '10',
}

# 家庭教師モデル選択肢
TUTOR_MODEL_OPTIONS = [
    ('sonnet', 'Claude Sonnet 4.5 (推奨・バランス型)'),
    ('haiku', 'Claude Haiku 4.5 (高速・低コスト)'),
    ('opus', 'Claude Opus 4.5 (最高性能・高コスト)'),
]

# 多言語対応デフォルトプロンプト（辞書検索用）
DEFAULT_CLAUDE_PROMPTS = {
    'JA': '''単語:{word}
1.意味（簡潔な辞書的定義）
2.学習者の理解を深める（英単語の場合、単語の分解[例:al-levi-ate、
接頭辞:「al-」、強調や方向を示す接頭辞（ここでは「～へ、強く」の意味）
語幹:「levi-」、「lev」 はラテン語の levis（軽い）に由来し、「軽くする、持ち上げる」の意味を持つ
接尾辞:「-ate」、動詞を作る接尾辞（「～する」という意味）]）
3.語法（基本の使い方）
4.類義語、対義語の紹介と簡潔な辞書的意味
※出力は簡潔に。Markdown形式（見出し、リスト、太字、テーブル等）使用可。
''',
    'EN': '''Word: {word}
1. Meaning (concise dictionary definition)
2. Deepen understanding (for English words, break down the word [e.g., al-levi-ate:
prefix: "al-" - intensifying prefix meaning "to, toward"
root: "levi-" - from Latin levis (light), meaning "to lighten, lift"
suffix: "-ate" - verb-forming suffix meaning "to do"])
3. Usage (basic usage patterns)
4. Synonyms and antonyms with brief definitions
Keep output concise. Markdown formatting (headings, lists, bold, tables) is allowed.
''',
    'ZH': '''单词: {word}
1. 含义（简洁的词典定义）
2. 加深理解（对于英语单词，分解词汇[例:al-levi-ate，
前缀:"al-"，强调或方向前缀（这里表示"向、强烈地"）
词根:"levi-"，源自拉丁语levis（轻的），表示"减轻、举起"
后缀:"-ate"，动词后缀（表示"做某事"）]）
3. 用法（基本用法）
4. 同义词和反义词及其简要含义
输出要简洁。可使用Markdown格式（标题、列表、粗体、表格等）。
''',
    'KO': '''단어: {word}
1. 의미 (간결한 사전적 정의)
2. 이해 심화 (영어 단어의 경우, 단어 분해 [예: al-levi-ate,
접두사: "al-" - 강조 또는 방향을 나타내는 접두사 ("~로, 강하게")
어근: "levi-" - 라틴어 levis(가벼운)에서 유래, "가볍게 하다, 들어올리다"
접미사: "-ate" - 동사를 만드는 접미사 ("~하다")])
3. 용법 (기본 사용법)
4. 동의어와 반의어 및 간단한 의미
출력은 간결하게. Markdown 형식(제목, 목록, 굵은 글씨, 표 등) 사용 가능.
''',
    'ES': '''Palabra: {word}
1. Significado (definición concisa de diccionario)
2. Profundizar comprensión (para palabras en inglés, desglose [ej: al-levi-ate,
prefijo: "al-" - prefijo intensificador que significa "hacia, fuertemente"
raíz: "levi-" - del latín levis (ligero), significa "aligerar, levantar"
sufijo: "-ate" - sufijo que forma verbos ("hacer")])
3. Uso (patrones básicos de uso)
4. Sinónimos y antónimos con definiciones breves
Mantener salida concisa. Se permite formato Markdown (títulos, listas, negrita, tablas).
''',
    'FR': '''Mot: {word}
1. Signification (définition concise du dictionnaire)
2. Approfondir la compréhension (pour les mots anglais, décomposition [ex: al-levi-ate,
préfixe: "al-" - préfixe intensifiant signifiant "vers, fortement"
racine: "levi-" - du latin levis (léger), signifiant "alléger, soulever"
suffixe: "-ate" - suffixe formant des verbes ("faire")])
3. Usage (modèles d'utilisation de base)
4. Synonymes et antonymes avec définitions brèves
Gardez la sortie concise. Le format Markdown (titres, listes, gras, tableaux) est autorisé.
''',
    'DE': '''Wort: {word}
1. Bedeutung (knappe Wörterbuchdefinition)
2. Verständnis vertiefen (bei englischen Wörtern, Wortzerlegung [z.B.: al-levi-ate,
Präfix: "al-" - verstärkendes Präfix, bedeutet "zu, stark"
Stamm: "levi-" - vom lateinischen levis (leicht), bedeutet "erleichtern, heben"
Suffix: "-ate" - verbbildendes Suffix ("tun")])
3. Verwendung (grundlegende Verwendungsmuster)
4. Synonyme und Antonyme mit kurzen Definitionen
Ausgabe knapp halten. Markdown-Format (Überschriften, Listen, Fett, Tabellen) erlaubt.
''',
    'PT-BR': '''Palavra: {word}
1. Significado (definição concisa de dicionário)
2. Aprofundar compreensão (para palavras em inglês, decomposição [ex: al-levi-ate,
prefixo: "al-" - prefixo intensificador significando "para, fortemente"
raiz: "levi-" - do latim levis (leve), significando "aliviar, levantar"
sufixo: "-ate" - sufixo formador de verbos ("fazer")])
3. Uso (padrões básicos de uso)
4. Sinônimos e antônimos com definições breves
Manter saída concisa. Formato Markdown (títulos, listas, negrito, tabelas) é permitido.
''',
    'RU': '''Слово: {word}
1. Значение (краткое словарное определение)
2. Углубление понимания (для английских слов, разбор [пр: al-levi-ate,
приставка: "al-" - усилительная приставка, означающая "к, сильно"
корень: "levi-" - от латинского levis (лёгкий), означает "облегчать, поднимать"
суффикс: "-ate" - глаголообразующий суффикс ("делать")])
3. Употребление (основные модели использования)
4. Синонимы и антонимы с краткими определениями
Вывод должен быть кратким. Разрешён формат Markdown (заголовки, списки, жирный, таблицы).
''',
}

# 多言語対応デフォルトプロンプト（家庭教師用）
DEFAULT_TUTOR_PROMPTS = {
    'JA': '''丁寧かつ親しみやすい家庭教師として回答。簡潔に。Markdown可。''',
    'EN': '''Respond as a polite, approachable tutor. Be concise. Markdown allowed.''',
    'ZH': '''以礼貌友好的家教身份回答。简洁。可用Markdown。''',
    'KO': '''정중하고 친근한 가정교사로 답변. 간결하게. Markdown 가능.''',
    'ES': '''Responde como tutor cortés y accesible. Sé conciso. Markdown permitido.''',
    'FR': '''Répondez en tuteur poli et accessible. Soyez concis. Markdown autorisé.''',
    'DE': '''Antworten Sie als höflicher, zugänglicher Tutor. Kurz und prägnant. Markdown erlaubt.''',
    'PT-BR': '''Responda como tutor educado e acessível. Seja conciso. Markdown permitido.''',
    'RU': '''Отвечайте как вежливый, доступный репетитор. Кратко. Markdown разрешён.''',
}


def get_default_claude_prompt(lang: str = 'EN') -> str:
    """指定言語のデフォルト辞書検索プロンプトを取得"""
    return DEFAULT_CLAUDE_PROMPTS.get(lang, DEFAULT_CLAUDE_PROMPTS['EN'])


def get_default_tutor_prompt(lang: str = 'EN') -> str:
    """指定言語のデフォルト家庭教師プロンプトを取得"""
    return DEFAULT_TUTOR_PROMPTS.get(lang, DEFAULT_TUTOR_PROMPTS['EN'])

# 翻訳対応言語（DeepL API）
# キー: DeepL APIの言語コード, 値: 表示名
TRANSLATION_LANGUAGES = {
    'JA': '日本語',
    'EN': '英語 / English',
    'ZH': '中国語(簡体) / Chinese',
    'KO': '韓国語 / Korean',
    'FR': 'フランス語 / French',
    'DE': 'ドイツ語 / German',
    'ES': 'スペイン語 / Spanish',
    'PT-BR': 'ポルトガル語(BR) / Portuguese',
    'IT': 'イタリア語 / Italian',
    'NL': 'オランダ語 / Dutch',
    'PL': 'ポーランド語 / Polish',
    'RU': 'ロシア語 / Russian',
}

# 翻訳先言語選択用のリスト（UIで使用）
LANGUAGE_OPTIONS = [
    ('JA', '日本語'),
    ('EN', '英語 / English'),
    ('ZH', '中国語(簡体) / Chinese'),
    ('KO', '韓国語 / Korean'),
    ('FR', 'フランス語 / French'),
    ('DE', 'ドイツ語 / German'),
    ('ES', 'スペイン語 / Spanish'),
    ('PT-BR', 'ポルトガル語(BR) / Portuguese'),
    ('IT', 'イタリア語 / Italian'),
    ('NL', 'オランダ語 / Dutch'),
    ('PL', 'ポーランド語 / Polish'),
    ('RU', 'ロシア語 / Russian'),
]

# UI言語選択用のリスト（母国語表示）
UI_LANGUAGE_OPTIONS = [
    ('EN', 'English'),
    ('JA', '日本語'),
    ('ZH', '中文（简体）'),
    ('KO', '한국어'),
    ('ES', 'Español'),
    ('FR', 'Français'),
    ('DE', 'Deutsch'),
    ('PT-BR', 'Português'),
    ('RU', 'Русский'),
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
        'cache_used': '[キャッシュから]',
        'ui_language_label': 'UI言語:',
        'ui_language_changed': 'UI言語を変更しました',
        # 設定ダイアログ
        'settings_title': '設定',
        'tab_translation': '翻訳設定',
        'tab_api': 'API設定',
        'tab_shortcut': 'ショートカット',
        'tab_speech': '音声設定',
        'tab_tutor': '家庭教師',
        'tab_display': '表示設定',
        'translation_options': '翻訳オプション',
        'use_deepl': 'DeepL APIを使用',
        'auto_add_vocab': '翻訳した単語を自動的に単語帳に追加',
        'target_language_section': '翻訳先言語',
        'target_language_label': '翻訳先言語:',
        'auto_detect_source': 'ソース言語を自動検出（翻訳先言語と同じ場合は日英自動切替）',
        'deepl_api_settings': 'DeepL API設定',
        'deepl_api_key': 'DeepL APIキー:',
        'claude_api_settings': 'Claude API設定',
        'claude_api_key': 'Claude APIキー:',
        'prompt_template': 'プロンプトテンプレート:',
        'hotkey_translation': '翻訳ホットキー設定',
        'hotkey_dictionary': '辞書検索ホットキー設定',
        'hotkey_speech': '音声出力ホットキー設定',
        'modifier_keys': '修飾キー:',
        'key_label': 'キー:',
        'speech_output': '音声出力機能',
        'enable_speech': '音声出力機能を有効にする',
        'volume_label': '音量:',
        'tutor_mode': '家庭教師モード',
        'enable_tutor': '家庭教師モードを有効にする',
        'model_label': '使用モデル:',
        'system_prompt': 'システムプロンプト',
        'context_history': '会話コンテキスト保持数:',
        'context_history_suffix': '件（直近の会話をAPIに送信）',
        'tutor_prompt_desc': '家庭教師の振る舞いを定義するプロンプト:',
        'reset_default': 'デフォルトに戻す',
        'display_language': '表示言語設定',
        'char_limit_section': '翻訳文字数制限',
        'char_limit_label': '一度に翻訳できる最大文字数:',
        'save_button': '保存',
        'cancel_button': 'キャンセル',
        'error_modifier_translation': '翻訳用に少なくとも1つの修飾キーを選択してください。',
        'error_modifier_dictionary': '辞書検索用に少なくとも1つの修飾キーを選択してください。',
        'error_modifier_speech': '音声出力用に少なくとも1つの修飾キーを選択してください。',
        'error_invalid_key': '有効なキーを選択してください。',
        'error_save': '設定の保存中にエラーが発生しました: {error}',
        # メニューバー
        'menu_file': 'ファイル',
        'menu_settings': '設定',
        'menu_exit': '終了',
        'menu_edit': '編集',
        'menu_copy': 'コピー',
        'menu_select_all': 'すべて選択',
        'menu_clear': 'クリア',
        'menu_history': '履歴',
        'menu_show_history': '翻訳履歴を表示',
        'menu_clear_history': '履歴をクリア',
        'menu_help': 'ヘルプ',
        'menu_usage': '使い方',
        'menu_about': 'バージョン情報',
        # チャットパネル
        'chat_toggle': '▲ 質問・相談する',
        'chat_toggle_close': '▼ 閉じる',
        'chat_placeholder': '質問を入力してください...',
        'chat_send': '送信',
        # ヘルプダイアログ
        'help_title': '使い方',
        'help_content': '''使い方:

1. 翻訳したいテキストをコピー（Ctrl+C）
2. Ctrl+Alt+D を押す（標準ショートカット）
3. 翻訳結果が自動的にクリップボードにコピーされます

辞書機能:
1. 単語を辞書検索するには Ctrl+Alt+J を押す
2. 辞書検索は単語のみに対応しています

音声出力機能:
1. テキストを音声出力するには Ctrl+Alt+T を押す
2. この機能を使うには gTTS と pygame モジュールが必要です

家庭教師機能:
1. 画面下部の「▲ 質問・相談する」をクリック
2. 翻訳履歴を参考に質問に回答してくれます

その他:
- Ctrl+マウスホイール: フォントサイズの変更''',
        'close_button': '閉じる',
        # バージョン情報
        'about_title': 'バージョン情報',
        'about_content': '''クリップボード翻訳ツール
Version {version}

DeepL API とClaude APIを使用して、
クリップボードのテキストを翻訳・解説します。
音声出力機能も搭載しています。''',
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
        'cache_used': '[From cache]',
        'ui_language_label': 'UI Language:',
        'ui_language_changed': 'UI language changed',
        # Settings Dialog
        'settings_title': 'Settings',
        'tab_translation': 'Translation',
        'tab_api': 'API Settings',
        'tab_shortcut': 'Shortcuts',
        'tab_speech': 'Speech',
        'tab_tutor': 'Tutor',
        'tab_display': 'Display',
        'translation_options': 'Translation Options',
        'use_deepl': 'Use DeepL API',
        'auto_add_vocab': 'Auto-add translated words to vocabulary',
        'target_language_section': 'Target Language',
        'target_language_label': 'Target Language:',
        'auto_detect_source': 'Auto-detect source language (auto-switch JA/EN if same as target)',
        'deepl_api_settings': 'DeepL API Settings',
        'deepl_api_key': 'DeepL API Key:',
        'claude_api_settings': 'Claude API Settings',
        'claude_api_key': 'Claude API Key:',
        'prompt_template': 'Prompt Template:',
        'hotkey_translation': 'Translation Hotkey',
        'hotkey_dictionary': 'Dictionary Hotkey',
        'hotkey_speech': 'Speech Hotkey',
        'modifier_keys': 'Modifier Keys:',
        'key_label': 'Key:',
        'speech_output': 'Speech Output',
        'enable_speech': 'Enable speech output',
        'volume_label': 'Volume:',
        'tutor_mode': 'Tutor Mode',
        'enable_tutor': 'Enable tutor mode',
        'model_label': 'Model:',
        'system_prompt': 'System Prompt',
        'context_history': 'Context History:',
        'context_history_suffix': 'messages (sent to API)',
        'tutor_prompt_desc': 'Prompt defining tutor behavior:',
        'reset_default': 'Reset to Default',
        'display_language': 'Display Language',
        'char_limit_section': 'Character Limit',
        'char_limit_label': 'Max characters per translation:',
        'save_button': 'Save',
        'cancel_button': 'Cancel',
        'error_modifier_translation': 'Select at least one modifier key for translation.',
        'error_modifier_dictionary': 'Select at least one modifier key for dictionary.',
        'error_modifier_speech': 'Select at least one modifier key for speech.',
        'error_invalid_key': 'Please select a valid key.',
        'error_save': 'Error saving settings: {error}',
        # Menu Bar
        'menu_file': 'File',
        'menu_settings': 'Settings',
        'menu_exit': 'Exit',
        'menu_edit': 'Edit',
        'menu_copy': 'Copy',
        'menu_select_all': 'Select All',
        'menu_clear': 'Clear',
        'menu_history': 'History',
        'menu_show_history': 'Show Translation History',
        'menu_clear_history': 'Clear History',
        'menu_help': 'Help',
        'menu_usage': 'How to Use',
        'menu_about': 'About',
        # Chat Panel
        'chat_toggle': '▲ Ask a Question',
        'chat_toggle_close': '▼ Close',
        'chat_placeholder': 'Enter your question...',
        'chat_send': 'Send',
        # Help Dialog
        'help_title': 'How to Use',
        'help_content': '''How to Use:

1. Copy text you want to translate (Ctrl+C)
2. Press Ctrl+Alt+D (default shortcut)
3. Translation is automatically copied to clipboard

Dictionary:
1. Press Ctrl+Alt+J to look up a word
2. Dictionary lookup works for single words only

Speech:
1. Press Ctrl+Alt+T for text-to-speech
2. Requires gTTS and pygame modules

Tutor:
1. Click "▲ Ask a Question" at the bottom
2. Get answers based on your translation history

Other:
- Ctrl+Mouse wheel: Change font size''',
        'close_button': 'Close',
        # About Dialog
        'about_title': 'About',
        'about_content': '''Clipboard Translation Tool
Version {version}

Uses DeepL API and Claude API to
translate and explain clipboard text.
Also includes text-to-speech feature.''',
    },
    'ZH': {
        'clipboard_empty': '剪贴板为空',
        'waiting': '等待中...',
        'translation_in_progress': '翻译中...',
        'offline_dict_used': '使用了离线词典',
        'local_dict_used': '使用了本地词典',
        'claude_api_used': '使用了Claude API',
        'no_internet': '无网络连接',
        'translation_complete': '翻译完成',
        'translation_failed': '翻译失败',
        'service_disabled': '翻译服务已禁用',
        'error_occurred': '发生错误',
        'deepl_failed_offline': 'DeepL失败 - 使用离线词典',
        'deepl_failed_local': 'DeepL失败 - 使用本地词典',
        'no_conversion': '无转换',
        'settings_saved': '设置已保存',
        'text_copied': '文本已复制',
        'no_text_selected': '未选择文本',
        'all_text_selected': '已选择全部文本',
        'text_cleared': '文本已清除',
        'font_size': '字体大小:',
        'script_running': '脚本运行中...',
        'input_label': '【输入】',
        'translated_label': '【翻译结果】',
        'dict_api_label': '【翻译结果】',
        'local_dict_label': '【翻译结果（本地词典）】',
        'no_conversion_label': '【翻译结果（无转换）】',
        'dictionary_lookup_complete': '词典查询完成',
        'word_not_in_dictionary': '词典中未找到',
        'dict_meaning_label': '【释义】',
        'dict_only_for_words': '词典查询仅支持单词。请使用普通翻译热键。',
        'claude_lookup_complete': 'Claude查询完成',
        'text_too_long': '超出字符限制（{max_length}字符）。翻译已中止。',
        'claude_api_error': 'API无法正常工作，词典查询失败。',
        'cache_used': '[来自缓存]',
        'ui_language_label': '界面语言:',
        'ui_language_changed': '界面语言已更改',
        # 设置对话框
        'settings_title': '设置',
        'tab_translation': '翻译设置',
        'tab_api': 'API设置',
        'tab_shortcut': '快捷键',
        'tab_speech': '语音设置',
        'tab_tutor': '家庭教师',
        'tab_display': '显示设置',
        'translation_options': '翻译选项',
        'use_deepl': '使用DeepL API',
        'auto_add_vocab': '自动将翻译的单词添加到词汇表',
        'target_language_section': '目标语言',
        'target_language_label': '目标语言:',
        'auto_detect_source': '自动检测源语言（如果与目标相同则自动切换日英）',
        'deepl_api_settings': 'DeepL API设置',
        'deepl_api_key': 'DeepL API密钥:',
        'claude_api_settings': 'Claude API设置',
        'claude_api_key': 'Claude API密钥:',
        'prompt_template': '提示模板:',
        'hotkey_translation': '翻译快捷键',
        'hotkey_dictionary': '词典快捷键',
        'hotkey_speech': '语音快捷键',
        'modifier_keys': '修饰键:',
        'key_label': '按键:',
        'speech_output': '语音输出',
        'enable_speech': '启用语音输出',
        'volume_label': '音量:',
        'tutor_mode': '家庭教师模式',
        'enable_tutor': '启用家庭教师模式',
        'model_label': '模型:',
        'system_prompt': '系统提示',
        'context_history': '上下文历史:',
        'context_history_suffix': '条消息（发送至API）',
        'tutor_prompt_desc': '定义家庭教师行为的提示:',
        'reset_default': '重置为默认',
        'display_language': '显示语言',
        'char_limit_section': '字符限制',
        'char_limit_label': '每次翻译最大字符数:',
        'save_button': '保存',
        'cancel_button': '取消',
        'error_modifier_translation': '请至少选择一个翻译修饰键。',
        'error_modifier_dictionary': '请至少选择一个词典修饰键。',
        'error_modifier_speech': '请至少选择一个语音修饰键。',
        'error_invalid_key': '请选择有效的按键。',
        'error_save': '保存设置时出错: {error}',
        # 菜单栏
        'menu_file': '文件',
        'menu_settings': '设置',
        'menu_exit': '退出',
        'menu_edit': '编辑',
        'menu_copy': '复制',
        'menu_select_all': '全选',
        'menu_clear': '清除',
        'menu_history': '历史',
        'menu_show_history': '显示翻译历史',
        'menu_clear_history': '清除历史',
        'menu_help': '帮助',
        'menu_usage': '使用方法',
        'menu_about': '关于',
        # 聊天面板
        'chat_toggle': '▲ 提问咨询',
        'chat_toggle_close': '▼ 关闭',
        'chat_placeholder': '请输入您的问题...',
        'chat_send': '发送',
        # 帮助对话框
        'help_title': '使用方法',
        'help_content': '''使用方法:

1. 复制要翻译的文本 (Ctrl+C)
2. 按 Ctrl+Alt+D（默认快捷键）
3. 翻译结果将自动复制到剪贴板

词典功能:
1. 按 Ctrl+Alt+J 查词
2. 词典查询仅支持单词

语音功能:
1. 按 Ctrl+Alt+T 进行语音播放
2. 需要 gTTS 和 pygame 模块

家庭教师功能:
1. 点击屏幕底部的"▲ 提问咨询"
2. 根据翻译历史回答您的问题

其他:
- Ctrl+鼠标滚轮: 调整字体大小''',
        'close_button': '关闭',
        # 关于对话框
        'about_title': '关于',
        'about_content': '''剪贴板翻译工具
Version {version}

使用 DeepL API 和 Claude API
翻译和解释剪贴板文本。
还包含语音播放功能。''',
    },
    'KO': {
        'clipboard_empty': '클립보드가 비어 있습니다',
        'waiting': '대기 중...',
        'translation_in_progress': '번역 중...',
        'offline_dict_used': '오프라인 사전 사용',
        'local_dict_used': '로컬 사전 사용',
        'claude_api_used': 'Claude API 사용',
        'no_internet': '인터넷 연결 없음',
        'translation_complete': '번역 완료',
        'translation_failed': '번역 실패',
        'service_disabled': '번역 서비스 비활성화',
        'error_occurred': '오류 발생',
        'deepl_failed_offline': 'DeepL 실패 - 오프라인 사전 사용',
        'deepl_failed_local': 'DeepL 실패 - 로컬 사전 사용',
        'no_conversion': '변환 없음',
        'settings_saved': '설정 저장됨',
        'text_copied': '텍스트 복사됨',
        'no_text_selected': '선택된 텍스트 없음',
        'all_text_selected': '모든 텍스트 선택됨',
        'text_cleared': '텍스트 삭제됨',
        'font_size': '글꼴 크기:',
        'script_running': '스크립트 실행 중...',
        'input_label': '【입력】',
        'translated_label': '【번역 결과】',
        'dict_api_label': '【번역 결과】',
        'local_dict_label': '【번역 결과 (로컬 사전)】',
        'no_conversion_label': '【번역 결과 (변환 없음)】',
        'dictionary_lookup_complete': '사전 검색 완료',
        'word_not_in_dictionary': '사전에 없음',
        'dict_meaning_label': '【의미】',
        'dict_only_for_words': '사전 검색은 단어만 지원합니다. 일반 번역 단축키를 사용하세요.',
        'claude_lookup_complete': 'Claude 검색 완료',
        'text_too_long': '문자 제한({max_length}자) 초과. 번역이 중단되었습니다.',
        'claude_api_error': 'API가 작동하지 않아 사전 검색에 실패했습니다.',
        'cache_used': '[캐시에서]',
        'ui_language_label': 'UI 언어:',
        'ui_language_changed': 'UI 언어가 변경되었습니다',
        # 설정 대화상자
        'settings_title': '설정',
        'tab_translation': '번역 설정',
        'tab_api': 'API 설정',
        'tab_shortcut': '단축키',
        'tab_speech': '음성 설정',
        'tab_tutor': '튜터',
        'tab_display': '표시 설정',
        'translation_options': '번역 옵션',
        'use_deepl': 'DeepL API 사용',
        'auto_add_vocab': '번역된 단어를 자동으로 단어장에 추가',
        'target_language_section': '대상 언어',
        'target_language_label': '대상 언어:',
        'auto_detect_source': '소스 언어 자동 감지 (대상과 같으면 일/영 자동 전환)',
        'deepl_api_settings': 'DeepL API 설정',
        'deepl_api_key': 'DeepL API 키:',
        'claude_api_settings': 'Claude API 설정',
        'claude_api_key': 'Claude API 키:',
        'prompt_template': '프롬프트 템플릿:',
        'hotkey_translation': '번역 단축키',
        'hotkey_dictionary': '사전 단축키',
        'hotkey_speech': '음성 단축키',
        'modifier_keys': '수정 키:',
        'key_label': '키:',
        'speech_output': '음성 출력',
        'enable_speech': '음성 출력 활성화',
        'volume_label': '볼륨:',
        'tutor_mode': '튜터 모드',
        'enable_tutor': '튜터 모드 활성화',
        'model_label': '모델:',
        'system_prompt': '시스템 프롬프트',
        'context_history': '대화 기록:',
        'context_history_suffix': '개 메시지 (API에 전송)',
        'tutor_prompt_desc': '튜터 동작을 정의하는 프롬프트:',
        'reset_default': '기본값으로 재설정',
        'display_language': '표시 언어',
        'char_limit_section': '문자 제한',
        'char_limit_label': '번역당 최대 문자 수:',
        'save_button': '저장',
        'cancel_button': '취소',
        'error_modifier_translation': '번역용 수정 키를 하나 이상 선택하세요.',
        'error_modifier_dictionary': '사전용 수정 키를 하나 이상 선택하세요.',
        'error_modifier_speech': '음성용 수정 키를 하나 이상 선택하세요.',
        'error_invalid_key': '유효한 키를 선택하세요.',
        'error_save': '설정 저장 오류: {error}',
        # 메뉴바
        'menu_file': '파일',
        'menu_settings': '설정',
        'menu_exit': '종료',
        'menu_edit': '편집',
        'menu_copy': '복사',
        'menu_select_all': '모두 선택',
        'menu_clear': '지우기',
        'menu_history': '기록',
        'menu_show_history': '번역 기록 보기',
        'menu_clear_history': '기록 지우기',
        'menu_help': '도움말',
        'menu_usage': '사용법',
        'menu_about': '정보',
        # 채팅 패널
        'chat_toggle': '▲ 질문하기',
        'chat_toggle_close': '▼ 닫기',
        'chat_placeholder': '질문을 입력하세요...',
        'chat_send': '전송',
        # 도움말 대화상자
        'help_title': '사용법',
        'help_content': '''사용법:

1. 번역할 텍스트 복사 (Ctrl+C)
2. Ctrl+Alt+D 누르기 (기본 단축키)
3. 번역 결과가 자동으로 클립보드에 복사됩니다

사전 기능:
1. Ctrl+Alt+J를 눌러 단어 검색
2. 사전 검색은 단어만 지원

음성 기능:
1. Ctrl+Alt+T를 눌러 음성 출력
2. gTTS 및 pygame 모듈 필요

튜터 기능:
1. 화면 하단의 "▲ 질문하기" 클릭
2. 번역 기록을 바탕으로 답변합니다

기타:
- Ctrl+마우스 휠: 글꼴 크기 변경''',
        'close_button': '닫기',
        # 정보 대화상자
        'about_title': '정보',
        'about_content': '''클립보드 번역 도구
Version {version}

DeepL API와 Claude API를 사용하여
클립보드 텍스트를 번역하고 설명합니다.
음성 출력 기능도 포함되어 있습니다.''',
    },
    'ES': {
        'clipboard_empty': 'El portapapeles está vacío',
        'waiting': 'Esperando...',
        'translation_in_progress': 'Traduciendo...',
        'offline_dict_used': 'Diccionario sin conexión usado',
        'local_dict_used': 'Diccionario local usado',
        'claude_api_used': 'Claude API usado',
        'no_internet': 'Sin conexión a Internet',
        'translation_complete': 'Traducción completa',
        'translation_failed': 'Traducción fallida',
        'service_disabled': 'Servicio de traducción deshabilitado',
        'error_occurred': 'Ocurrió un error',
        'deepl_failed_offline': 'DeepL falló - Usando diccionario sin conexión',
        'deepl_failed_local': 'DeepL falló - Usando diccionario local',
        'no_conversion': 'Sin conversión',
        'settings_saved': 'Configuración guardada',
        'text_copied': 'Texto copiado',
        'no_text_selected': 'Ningún texto seleccionado',
        'all_text_selected': 'Todo el texto seleccionado',
        'text_cleared': 'Texto borrado',
        'font_size': 'Tamaño de fuente:',
        'script_running': 'Script en ejecución...',
        'input_label': '【Entrada】',
        'translated_label': '【Traducido】',
        'dict_api_label': '【Traducido】',
        'local_dict_label': '【Traducido (Diccionario local)】',
        'no_conversion_label': '【Traducido (Sin conversión)】',
        'dictionary_lookup_complete': 'Búsqueda en diccionario completa',
        'word_not_in_dictionary': 'Palabra no encontrada',
        'dict_meaning_label': '【Significado】',
        'dict_only_for_words': 'La búsqueda solo funciona con palabras individuales.',
        'claude_lookup_complete': 'Búsqueda Claude completa',
        'text_too_long': 'Límite de caracteres ({max_length}) excedido.',
        'claude_api_error': 'La búsqueda falló porque la API no funciona.',
        'cache_used': '[Desde caché]',
        'ui_language_label': 'Idioma de la interfaz:',
        'ui_language_changed': 'Idioma de la interfaz cambiado',
        # Diálogo de configuración
        'settings_title': 'Configuración',
        'tab_translation': 'Traducción',
        'tab_api': 'API',
        'tab_shortcut': 'Atajos',
        'tab_speech': 'Voz',
        'tab_tutor': 'Tutor',
        'tab_display': 'Pantalla',
        'translation_options': 'Opciones de traducción',
        'use_deepl': 'Usar DeepL API',
        'auto_add_vocab': 'Agregar palabras traducidas al vocabulario',
        'target_language_section': 'Idioma destino',
        'target_language_label': 'Idioma destino:',
        'auto_detect_source': 'Detectar idioma origen (cambio auto JA/EN si es igual al destino)',
        'deepl_api_settings': 'Configuración DeepL API',
        'deepl_api_key': 'Clave DeepL API:',
        'claude_api_settings': 'Configuración Claude API',
        'claude_api_key': 'Clave Claude API:',
        'prompt_template': 'Plantilla de prompt:',
        'hotkey_translation': 'Atajo de traducción',
        'hotkey_dictionary': 'Atajo de diccionario',
        'hotkey_speech': 'Atajo de voz',
        'modifier_keys': 'Teclas modificadoras:',
        'key_label': 'Tecla:',
        'speech_output': 'Salida de voz',
        'enable_speech': 'Habilitar salida de voz',
        'volume_label': 'Volumen:',
        'tutor_mode': 'Modo tutor',
        'enable_tutor': 'Habilitar modo tutor',
        'model_label': 'Modelo:',
        'system_prompt': 'Prompt del sistema',
        'context_history': 'Historial de contexto:',
        'context_history_suffix': 'mensajes (enviados a API)',
        'tutor_prompt_desc': 'Prompt que define el comportamiento del tutor:',
        'reset_default': 'Restablecer',
        'display_language': 'Idioma de pantalla',
        'char_limit_section': 'Límite de caracteres',
        'char_limit_label': 'Máx. caracteres por traducción:',
        'save_button': 'Guardar',
        'cancel_button': 'Cancelar',
        'error_modifier_translation': 'Seleccione al menos una tecla modificadora para traducción.',
        'error_modifier_dictionary': 'Seleccione al menos una tecla modificadora para diccionario.',
        'error_modifier_speech': 'Seleccione al menos una tecla modificadora para voz.',
        'error_invalid_key': 'Seleccione una tecla válida.',
        'error_save': 'Error al guardar: {error}',
        # Barra de menú
        'menu_file': 'Archivo',
        'menu_settings': 'Configuración',
        'menu_exit': 'Salir',
        'menu_edit': 'Editar',
        'menu_copy': 'Copiar',
        'menu_select_all': 'Seleccionar todo',
        'menu_clear': 'Borrar',
        'menu_history': 'Historial',
        'menu_show_history': 'Ver historial de traducción',
        'menu_clear_history': 'Borrar historial',
        'menu_help': 'Ayuda',
        'menu_usage': 'Cómo usar',
        'menu_about': 'Acerca de',
        # Panel de chat
        'chat_toggle': '▲ Hacer pregunta',
        'chat_toggle_close': '▼ Cerrar',
        'chat_placeholder': 'Escriba su pregunta...',
        'chat_send': 'Enviar',
        # Diálogo de ayuda
        'help_title': 'Cómo usar',
        'help_content': '''Cómo usar:

1. Copie el texto a traducir (Ctrl+C)
2. Presione Ctrl+Alt+D (atajo predeterminado)
3. La traducción se copia automáticamente al portapapeles

Diccionario:
1. Presione Ctrl+Alt+J para buscar una palabra
2. Solo funciona con palabras individuales

Voz:
1. Presione Ctrl+Alt+T para texto a voz
2. Requiere módulos gTTS y pygame

Tutor:
1. Haga clic en "▲ Hacer pregunta" abajo
2. Responde según su historial de traducción

Otros:
- Ctrl+rueda del mouse: Cambiar tamaño de fuente''',
        'close_button': 'Cerrar',
        # Diálogo Acerca de
        'about_title': 'Acerca de',
        'about_content': '''Herramienta de traducción del portapapeles
Version {version}

Utiliza DeepL API y Claude API para
traducir y explicar texto del portapapeles.
También incluye función de texto a voz.''',
    },
    'FR': {
        'clipboard_empty': 'Le presse-papiers est vide',
        'waiting': 'En attente...',
        'translation_in_progress': 'Traduction en cours...',
        'offline_dict_used': 'Dictionnaire hors ligne utilisé',
        'local_dict_used': 'Dictionnaire local utilisé',
        'claude_api_used': 'Claude API utilisé',
        'no_internet': 'Pas de connexion Internet',
        'translation_complete': 'Traduction terminée',
        'translation_failed': 'Échec de la traduction',
        'service_disabled': 'Service de traduction désactivé',
        'error_occurred': 'Une erreur est survenue',
        'deepl_failed_offline': 'DeepL échoué - Dictionnaire hors ligne utilisé',
        'deepl_failed_local': 'DeepL échoué - Dictionnaire local utilisé',
        'no_conversion': 'Pas de conversion',
        'settings_saved': 'Paramètres enregistrés',
        'text_copied': 'Texte copié',
        'no_text_selected': 'Aucun texte sélectionné',
        'all_text_selected': 'Tout le texte sélectionné',
        'text_cleared': 'Texte effacé',
        'font_size': 'Taille de police:',
        'script_running': 'Script en cours...',
        'input_label': '【Entrée】',
        'translated_label': '【Traduit】',
        'dict_api_label': '【Traduit】',
        'local_dict_label': '【Traduit (Dictionnaire local)】',
        'no_conversion_label': '【Traduit (Pas de conversion)】',
        'dictionary_lookup_complete': 'Recherche terminée',
        'word_not_in_dictionary': 'Mot non trouvé',
        'dict_meaning_label': '【Signification】',
        'dict_only_for_words': 'La recherche ne fonctionne que pour les mots individuels.',
        'claude_lookup_complete': 'Recherche Claude terminée',
        'text_too_long': 'Limite de caractères ({max_length}) dépassée.',
        'claude_api_error': 'Échec car l\'API ne fonctionne pas.',
        'cache_used': '[Depuis le cache]',
        'ui_language_label': 'Langue de l\'interface:',
        'ui_language_changed': 'Langue de l\'interface modifiée',
        # Dialogue de paramètres
        'settings_title': 'Paramètres',
        'tab_translation': 'Traduction',
        'tab_api': 'API',
        'tab_shortcut': 'Raccourcis',
        'tab_speech': 'Voix',
        'tab_tutor': 'Tuteur',
        'tab_display': 'Affichage',
        'translation_options': 'Options de traduction',
        'use_deepl': 'Utiliser DeepL API',
        'auto_add_vocab': 'Ajouter les mots traduits au vocabulaire',
        'target_language_section': 'Langue cible',
        'target_language_label': 'Langue cible:',
        'auto_detect_source': 'Détecter la langue source (bascule auto JA/EN si identique à cible)',
        'deepl_api_settings': 'Paramètres DeepL API',
        'deepl_api_key': 'Clé DeepL API:',
        'claude_api_settings': 'Paramètres Claude API',
        'claude_api_key': 'Clé Claude API:',
        'prompt_template': 'Modèle de prompt:',
        'hotkey_translation': 'Raccourci traduction',
        'hotkey_dictionary': 'Raccourci dictionnaire',
        'hotkey_speech': 'Raccourci voix',
        'modifier_keys': 'Touches de modification:',
        'key_label': 'Touche:',
        'speech_output': 'Sortie vocale',
        'enable_speech': 'Activer la sortie vocale',
        'volume_label': 'Volume:',
        'tutor_mode': 'Mode tuteur',
        'enable_tutor': 'Activer le mode tuteur',
        'model_label': 'Modèle:',
        'system_prompt': 'Prompt système',
        'context_history': 'Historique du contexte:',
        'context_history_suffix': 'messages (envoyés à l\'API)',
        'tutor_prompt_desc': 'Prompt définissant le comportement du tuteur:',
        'reset_default': 'Réinitialiser',
        'display_language': 'Langue d\'affichage',
        'char_limit_section': 'Limite de caractères',
        'char_limit_label': 'Caractères max par traduction:',
        'save_button': 'Enregistrer',
        'cancel_button': 'Annuler',
        'error_modifier_translation': 'Sélectionnez au moins une touche de modification pour la traduction.',
        'error_modifier_dictionary': 'Sélectionnez au moins une touche de modification pour le dictionnaire.',
        'error_modifier_speech': 'Sélectionnez au moins une touche de modification pour la voix.',
        'error_invalid_key': 'Sélectionnez une touche valide.',
        'error_save': 'Erreur lors de l\'enregistrement: {error}',
        # Barre de menu
        'menu_file': 'Fichier',
        'menu_settings': 'Paramètres',
        'menu_exit': 'Quitter',
        'menu_edit': 'Édition',
        'menu_copy': 'Copier',
        'menu_select_all': 'Tout sélectionner',
        'menu_clear': 'Effacer',
        'menu_history': 'Historique',
        'menu_show_history': 'Afficher l\'historique',
        'menu_clear_history': 'Effacer l\'historique',
        'menu_help': 'Aide',
        'menu_usage': 'Mode d\'emploi',
        'menu_about': 'À propos',
        # Panneau de chat
        'chat_toggle': '▲ Poser une question',
        'chat_toggle_close': '▼ Fermer',
        'chat_placeholder': 'Entrez votre question...',
        'chat_send': 'Envoyer',
        # Dialogue d'aide
        'help_title': 'Mode d\'emploi',
        'help_content': '''Mode d'emploi:

1. Copiez le texte à traduire (Ctrl+C)
2. Appuyez sur Ctrl+Alt+D (raccourci par défaut)
3. La traduction est automatiquement copiée

Dictionnaire:
1. Appuyez sur Ctrl+Alt+J pour chercher un mot
2. Fonctionne uniquement pour les mots individuels

Voix:
1. Appuyez sur Ctrl+Alt+T pour la synthèse vocale
2. Nécessite les modules gTTS et pygame

Tuteur:
1. Cliquez sur "▲ Poser une question" en bas
2. Répond selon votre historique de traduction

Autres:
- Ctrl+molette souris: Changer la taille de police''',
        'close_button': 'Fermer',
        # Dialogue À propos
        'about_title': 'À propos',
        'about_content': '''Outil de traduction du presse-papiers
Version {version}

Utilise DeepL API et Claude API pour
traduire et expliquer le texte du presse-papiers.
Inclut également la synthèse vocale.''',
    },
    'DE': {
        'clipboard_empty': 'Zwischenablage ist leer',
        'waiting': 'Warten...',
        'translation_in_progress': 'Übersetze...',
        'offline_dict_used': 'Offline-Wörterbuch verwendet',
        'local_dict_used': 'Lokales Wörterbuch verwendet',
        'claude_api_used': 'Claude API verwendet',
        'no_internet': 'Keine Internetverbindung',
        'translation_complete': 'Übersetzung abgeschlossen',
        'translation_failed': 'Übersetzung fehlgeschlagen',
        'service_disabled': 'Übersetzungsdienst deaktiviert',
        'error_occurred': 'Ein Fehler ist aufgetreten',
        'deepl_failed_offline': 'DeepL fehlgeschlagen - Offline-Wörterbuch verwendet',
        'deepl_failed_local': 'DeepL fehlgeschlagen - Lokales Wörterbuch verwendet',
        'no_conversion': 'Keine Konvertierung',
        'settings_saved': 'Einstellungen gespeichert',
        'text_copied': 'Text kopiert',
        'no_text_selected': 'Kein Text ausgewählt',
        'all_text_selected': 'Gesamter Text ausgewählt',
        'text_cleared': 'Text gelöscht',
        'font_size': 'Schriftgröße:',
        'script_running': 'Skript läuft...',
        'input_label': '【Eingabe】',
        'translated_label': '【Übersetzt】',
        'dict_api_label': '【Übersetzt】',
        'local_dict_label': '【Übersetzt (Lokales Wörterbuch)】',
        'no_conversion_label': '【Übersetzt (Keine Konvertierung)】',
        'dictionary_lookup_complete': 'Wörterbuchsuche abgeschlossen',
        'word_not_in_dictionary': 'Wort nicht gefunden',
        'dict_meaning_label': '【Bedeutung】',
        'dict_only_for_words': 'Die Suche funktioniert nur für einzelne Wörter.',
        'claude_lookup_complete': 'Claude-Suche abgeschlossen',
        'text_too_long': 'Zeichenlimit ({max_length}) überschritten.',
        'claude_api_error': 'Suche fehlgeschlagen, da die API nicht funktioniert.',
        'cache_used': '[Aus Cache]',
        'ui_language_label': 'Oberflächensprache:',
        'ui_language_changed': 'Oberflächensprache geändert',
        # Einstellungsdialog
        'settings_title': 'Einstellungen',
        'tab_translation': 'Übersetzung',
        'tab_api': 'API',
        'tab_shortcut': 'Tastenkürzel',
        'tab_speech': 'Sprache',
        'tab_tutor': 'Tutor',
        'tab_display': 'Anzeige',
        'translation_options': 'Übersetzungsoptionen',
        'use_deepl': 'DeepL API verwenden',
        'auto_add_vocab': 'Übersetzte Wörter zum Vokabular hinzufügen',
        'target_language_section': 'Zielsprache',
        'target_language_label': 'Zielsprache:',
        'auto_detect_source': 'Quellsprache erkennen (auto JA/EN wenn gleich Ziel)',
        'deepl_api_settings': 'DeepL API Einstellungen',
        'deepl_api_key': 'DeepL API-Schlüssel:',
        'claude_api_settings': 'Claude API Einstellungen',
        'claude_api_key': 'Claude API-Schlüssel:',
        'prompt_template': 'Prompt-Vorlage:',
        'hotkey_translation': 'Übersetzungs-Tastenkürzel',
        'hotkey_dictionary': 'Wörterbuch-Tastenkürzel',
        'hotkey_speech': 'Sprach-Tastenkürzel',
        'modifier_keys': 'Modifikatortasten:',
        'key_label': 'Taste:',
        'speech_output': 'Sprachausgabe',
        'enable_speech': 'Sprachausgabe aktivieren',
        'volume_label': 'Lautstärke:',
        'tutor_mode': 'Tutor-Modus',
        'enable_tutor': 'Tutor-Modus aktivieren',
        'model_label': 'Modell:',
        'system_prompt': 'System-Prompt',
        'context_history': 'Kontextverlauf:',
        'context_history_suffix': 'Nachrichten (an API gesendet)',
        'tutor_prompt_desc': 'Prompt für Tutor-Verhalten:',
        'reset_default': 'Zurücksetzen',
        'display_language': 'Anzeigesprache',
        'char_limit_section': 'Zeichenlimit',
        'char_limit_label': 'Max. Zeichen pro Übersetzung:',
        'save_button': 'Speichern',
        'cancel_button': 'Abbrechen',
        'error_modifier_translation': 'Wählen Sie mindestens eine Modifikatortaste für Übersetzung.',
        'error_modifier_dictionary': 'Wählen Sie mindestens eine Modifikatortaste für Wörterbuch.',
        'error_modifier_speech': 'Wählen Sie mindestens eine Modifikatortaste für Sprache.',
        'error_invalid_key': 'Wählen Sie eine gültige Taste.',
        'error_save': 'Fehler beim Speichern: {error}',
        # Menüleiste
        'menu_file': 'Datei',
        'menu_settings': 'Einstellungen',
        'menu_exit': 'Beenden',
        'menu_edit': 'Bearbeiten',
        'menu_copy': 'Kopieren',
        'menu_select_all': 'Alles auswählen',
        'menu_clear': 'Löschen',
        'menu_history': 'Verlauf',
        'menu_show_history': 'Übersetzungsverlauf anzeigen',
        'menu_clear_history': 'Verlauf löschen',
        'menu_help': 'Hilfe',
        'menu_usage': 'Anleitung',
        'menu_about': 'Über',
        # Chat-Panel
        'chat_toggle': '▲ Frage stellen',
        'chat_toggle_close': '▼ Schließen',
        'chat_placeholder': 'Geben Sie Ihre Frage ein...',
        'chat_send': 'Senden',
        # Hilfe-Dialog
        'help_title': 'Anleitung',
        'help_content': '''Anleitung:

1. Text zum Übersetzen kopieren (Strg+C)
2. Strg+Alt+D drücken (Standardtaste)
3. Übersetzung wird automatisch kopiert

Wörterbuch:
1. Strg+Alt+J für Wortsuche drücken
2. Funktioniert nur für einzelne Wörter

Sprache:
1. Strg+Alt+T für Sprachausgabe drücken
2. Erfordert gTTS und pygame Module

Tutor:
1. Klicken Sie unten auf "▲ Frage stellen"
2. Antwortet basierend auf Ihrem Übersetzungsverlauf

Sonstiges:
- Strg+Mausrad: Schriftgröße ändern''',
        'close_button': 'Schließen',
        # Über-Dialog
        'about_title': 'Über',
        'about_content': '''Zwischenablage-Übersetzungstool
Version {version}

Verwendet DeepL API und Claude API um
Zwischenablage-Text zu übersetzen und erklären.
Enthält auch Sprachausgabe-Funktion.''',
    },
    'PT-BR': {
        'clipboard_empty': 'A área de transferência está vazia',
        'waiting': 'Aguardando...',
        'translation_in_progress': 'Traduzindo...',
        'offline_dict_used': 'Dicionário offline usado',
        'local_dict_used': 'Dicionário local usado',
        'claude_api_used': 'Claude API usado',
        'no_internet': 'Sem conexão com a Internet',
        'translation_complete': 'Tradução concluída',
        'translation_failed': 'Falha na tradução',
        'service_disabled': 'Serviço de tradução desativado',
        'error_occurred': 'Ocorreu um erro',
        'deepl_failed_offline': 'DeepL falhou - Usando dicionário offline',
        'deepl_failed_local': 'DeepL falhou - Usando dicionário local',
        'no_conversion': 'Sem conversão',
        'settings_saved': 'Configurações salvas',
        'text_copied': 'Texto copiado',
        'no_text_selected': 'Nenhum texto selecionado',
        'all_text_selected': 'Todo o texto selecionado',
        'text_cleared': 'Texto apagado',
        'font_size': 'Tamanho da fonte:',
        'script_running': 'Script em execução...',
        'input_label': '【Entrada】',
        'translated_label': '【Traduzido】',
        'dict_api_label': '【Traduzido】',
        'local_dict_label': '【Traduzido (Dicionário local)】',
        'no_conversion_label': '【Traduzido (Sem conversão)】',
        'dictionary_lookup_complete': 'Pesquisa concluída',
        'word_not_in_dictionary': 'Palavra não encontrada',
        'dict_meaning_label': '【Significado】',
        'dict_only_for_words': 'A pesquisa funciona apenas para palavras individuais.',
        'claude_lookup_complete': 'Pesquisa Claude concluída',
        'text_too_long': 'Limite de caracteres ({max_length}) excedido.',
        'claude_api_error': 'Pesquisa falhou porque a API não está funcionando.',
        'cache_used': '[Do cache]',
        'ui_language_label': 'Idioma da interface:',
        'ui_language_changed': 'Idioma da interface alterado',
        # Diálogo de configurações
        'settings_title': 'Configurações',
        'tab_translation': 'Tradução',
        'tab_api': 'API',
        'tab_shortcut': 'Atalhos',
        'tab_speech': 'Voz',
        'tab_tutor': 'Tutor',
        'tab_display': 'Exibição',
        'translation_options': 'Opções de tradução',
        'use_deepl': 'Usar DeepL API',
        'auto_add_vocab': 'Adicionar palavras traduzidas ao vocabulário',
        'target_language_section': 'Idioma destino',
        'target_language_label': 'Idioma destino:',
        'auto_detect_source': 'Detectar idioma origem (troca auto JA/EN se igual ao destino)',
        'deepl_api_settings': 'Configurações DeepL API',
        'deepl_api_key': 'Chave DeepL API:',
        'claude_api_settings': 'Configurações Claude API',
        'claude_api_key': 'Chave Claude API:',
        'prompt_template': 'Modelo de prompt:',
        'hotkey_translation': 'Atalho de tradução',
        'hotkey_dictionary': 'Atalho de dicionário',
        'hotkey_speech': 'Atalho de voz',
        'modifier_keys': 'Teclas modificadoras:',
        'key_label': 'Tecla:',
        'speech_output': 'Saída de voz',
        'enable_speech': 'Ativar saída de voz',
        'volume_label': 'Volume:',
        'tutor_mode': 'Modo tutor',
        'enable_tutor': 'Ativar modo tutor',
        'model_label': 'Modelo:',
        'system_prompt': 'Prompt do sistema',
        'context_history': 'Histórico de contexto:',
        'context_history_suffix': 'mensagens (enviadas à API)',
        'tutor_prompt_desc': 'Prompt que define o comportamento do tutor:',
        'reset_default': 'Redefinir',
        'display_language': 'Idioma de exibição',
        'char_limit_section': 'Limite de caracteres',
        'char_limit_label': 'Máx. caracteres por tradução:',
        'save_button': 'Salvar',
        'cancel_button': 'Cancelar',
        'error_modifier_translation': 'Selecione pelo menos uma tecla modificadora para tradução.',
        'error_modifier_dictionary': 'Selecione pelo menos uma tecla modificadora para dicionário.',
        'error_modifier_speech': 'Selecione pelo menos uma tecla modificadora para voz.',
        'error_invalid_key': 'Selecione uma tecla válida.',
        'error_save': 'Erro ao salvar: {error}',
        # Barra de menu
        'menu_file': 'Arquivo',
        'menu_settings': 'Configurações',
        'menu_exit': 'Sair',
        'menu_edit': 'Editar',
        'menu_copy': 'Copiar',
        'menu_select_all': 'Selecionar tudo',
        'menu_clear': 'Limpar',
        'menu_history': 'Histórico',
        'menu_show_history': 'Ver histórico de tradução',
        'menu_clear_history': 'Limpar histórico',
        'menu_help': 'Ajuda',
        'menu_usage': 'Como usar',
        'menu_about': 'Sobre',
        # Painel de chat
        'chat_toggle': '▲ Fazer pergunta',
        'chat_toggle_close': '▼ Fechar',
        'chat_placeholder': 'Digite sua pergunta...',
        'chat_send': 'Enviar',
        # Diálogo de ajuda
        'help_title': 'Como usar',
        'help_content': '''Como usar:

1. Copie o texto a traduzir (Ctrl+C)
2. Pressione Ctrl+Alt+D (atalho padrão)
3. A tradução é copiada automaticamente

Dicionário:
1. Pressione Ctrl+Alt+J para buscar uma palavra
2. Funciona apenas para palavras individuais

Voz:
1. Pressione Ctrl+Alt+T para texto em voz
2. Requer módulos gTTS e pygame

Tutor:
1. Clique em "▲ Fazer pergunta" abaixo
2. Responde com base no seu histórico de tradução

Outros:
- Ctrl+roda do mouse: Alterar tamanho da fonte''',
        'close_button': 'Fechar',
        # Diálogo Sobre
        'about_title': 'Sobre',
        'about_content': '''Ferramenta de tradução da área de transferência
Version {version}

Usa DeepL API e Claude API para
traduzir e explicar texto da área de transferência.
Também inclui função de texto em voz.''',
    },
    'RU': {
        'clipboard_empty': 'Буфер обмена пуст',
        'waiting': 'Ожидание...',
        'translation_in_progress': 'Перевод...',
        'offline_dict_used': 'Использован офлайн-словарь',
        'local_dict_used': 'Использован локальный словарь',
        'claude_api_used': 'Использован Claude API',
        'no_internet': 'Нет подключения к Интернету',
        'translation_complete': 'Перевод завершён',
        'translation_failed': 'Ошибка перевода',
        'service_disabled': 'Служба перевода отключена',
        'error_occurred': 'Произошла ошибка',
        'deepl_failed_offline': 'DeepL не удался - Используется офлайн-словарь',
        'deepl_failed_local': 'DeepL не удался - Используется локальный словарь',
        'no_conversion': 'Без преобразования',
        'settings_saved': 'Настройки сохранены',
        'text_copied': 'Текст скопирован',
        'no_text_selected': 'Текст не выбран',
        'all_text_selected': 'Весь текст выбран',
        'text_cleared': 'Текст удалён',
        'font_size': 'Размер шрифта:',
        'script_running': 'Скрипт выполняется...',
        'input_label': '【Ввод】',
        'translated_label': '【Переведено】',
        'dict_api_label': '【Переведено】',
        'local_dict_label': '【Переведено (Локальный словарь)】',
        'no_conversion_label': '【Переведено (Без преобразования)】',
        'dictionary_lookup_complete': 'Поиск завершён',
        'word_not_in_dictionary': 'Слово не найдено',
        'dict_meaning_label': '【Значение】',
        'dict_only_for_words': 'Поиск работает только для отдельных слов.',
        'claude_lookup_complete': 'Поиск Claude завершён',
        'text_too_long': 'Превышен лимит символов ({max_length}).',
        'claude_api_error': 'Поиск не удался, API не работает.',
        'cache_used': '[Из кэша]',
        'ui_language_label': 'Язык интерфейса:',
        'ui_language_changed': 'Язык интерфейса изменён',
        # Диалог настроек
        'settings_title': 'Настройки',
        'tab_translation': 'Перевод',
        'tab_api': 'API',
        'tab_shortcut': 'Горячие клавиши',
        'tab_speech': 'Голос',
        'tab_tutor': 'Репетитор',
        'tab_display': 'Отображение',
        'translation_options': 'Параметры перевода',
        'use_deepl': 'Использовать DeepL API',
        'auto_add_vocab': 'Добавлять переведённые слова в словарь',
        'target_language_section': 'Целевой язык',
        'target_language_label': 'Целевой язык:',
        'auto_detect_source': 'Определять исходный язык (авто JA/EN если совпадает с целевым)',
        'deepl_api_settings': 'Настройки DeepL API',
        'deepl_api_key': 'Ключ DeepL API:',
        'claude_api_settings': 'Настройки Claude API',
        'claude_api_key': 'Ключ Claude API:',
        'prompt_template': 'Шаблон запроса:',
        'hotkey_translation': 'Клавиша перевода',
        'hotkey_dictionary': 'Клавиша словаря',
        'hotkey_speech': 'Клавиша голоса',
        'modifier_keys': 'Модификаторы:',
        'key_label': 'Клавиша:',
        'speech_output': 'Голосовой вывод',
        'enable_speech': 'Включить голосовой вывод',
        'volume_label': 'Громкость:',
        'tutor_mode': 'Режим репетитора',
        'enable_tutor': 'Включить режим репетитора',
        'model_label': 'Модель:',
        'system_prompt': 'Системный запрос',
        'context_history': 'История контекста:',
        'context_history_suffix': 'сообщений (отправляется в API)',
        'tutor_prompt_desc': 'Запрос, определяющий поведение репетитора:',
        'reset_default': 'Сбросить',
        'display_language': 'Язык отображения',
        'char_limit_section': 'Лимит символов',
        'char_limit_label': 'Макс. символов на перевод:',
        'save_button': 'Сохранить',
        'cancel_button': 'Отмена',
        'error_modifier_translation': 'Выберите хотя бы одну клавишу-модификатор для перевода.',
        'error_modifier_dictionary': 'Выберите хотя бы одну клавишу-модификатор для словаря.',
        'error_modifier_speech': 'Выберите хотя бы одну клавишу-модификатор для голоса.',
        'error_invalid_key': 'Выберите корректную клавишу.',
        'error_save': 'Ошибка сохранения: {error}',
        # Строка меню
        'menu_file': 'Файл',
        'menu_settings': 'Настройки',
        'menu_exit': 'Выход',
        'menu_edit': 'Редактирование',
        'menu_copy': 'Копировать',
        'menu_select_all': 'Выбрать всё',
        'menu_clear': 'Очистить',
        'menu_history': 'История',
        'menu_show_history': 'Показать историю переводов',
        'menu_clear_history': 'Очистить историю',
        'menu_help': 'Справка',
        'menu_usage': 'Инструкция',
        'menu_about': 'О программе',
        # Панель чата
        'chat_toggle': '▲ Задать вопрос',
        'chat_toggle_close': '▼ Закрыть',
        'chat_placeholder': 'Введите ваш вопрос...',
        'chat_send': 'Отправить',
        # Диалог справки
        'help_title': 'Инструкция',
        'help_content': '''Инструкция:

1. Скопируйте текст для перевода (Ctrl+C)
2. Нажмите Ctrl+Alt+D (клавиша по умолчанию)
3. Перевод автоматически скопируется

Словарь:
1. Нажмите Ctrl+Alt+J для поиска слова
2. Работает только для отдельных слов

Голос:
1. Нажмите Ctrl+Alt+T для озвучки текста
2. Требуются модули gTTS и pygame

Репетитор:
1. Нажмите "▲ Задать вопрос" внизу
2. Отвечает на основе истории переводов

Прочее:
- Ctrl+колесо мыши: Изменить размер шрифта''',
        'close_button': 'Закрыть',
        # Диалог О программе
        'about_title': 'О программе',
        'about_content': '''Инструмент перевода буфера обмена
Version {version}

Использует DeepL API и Claude API для
перевода и объяснения текста из буфера.
Также включает функцию озвучки текста.''',
    },
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
VERSION = "1.20"
APP_TITLE = "ClipTrans"


def get_message(key: str, lang: str = 'EN', **kwargs) -> str:
    """
    指定されたキーとUI言語に対応するメッセージを取得する
    フォールバック: 指定言語にない場合は英語、英語にもない場合はキーを返す

    Args:
        key: メッセージキー
        lang: UI言語コード (デフォルト: 'EN')
        **kwargs: メッセージ内の変数置換用

    Returns:
        ローカライズされたメッセージ文字列
    """
    # 指定言語のメッセージを試行
    if lang in MESSAGES and key in MESSAGES[lang]:
        msg = MESSAGES[lang][key]
    # フォールバック: 英語
    elif key in MESSAGES.get('EN', {}):
        msg = MESSAGES['EN'][key]
    # 最終フォールバック: キーをそのまま返す
    else:
        return key

    # 変数置換
    if kwargs:
        try:
            msg = msg.format(**kwargs)
        except KeyError:
            pass

    return msg
