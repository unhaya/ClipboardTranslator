# ClipboardTranslator v1.00 - Language Detection Module
import langid


def detect_language(text):
    """テキストの言語を検出"""
    # 短いテキストの場合は文字種で判断
    if len(text.strip()) <= 5:
        # 日本語文字が含まれているかチェック
        if any(ord(c) > 127 for c in text):
            return 'JA'
        # 英数字のみの場合
        if all(ord(c) < 128 for c in text):
            return 'EN'

    # 長いテキストはlangidで検出
    try:
        detected_lang, confidence = langid.classify(text)
        if detected_lang == 'en':
            return 'EN'
        elif detected_lang == 'ja':
            return 'JA'
        else:
            # その他の言語の場合、文字種で再判定
            if any(ord(c) > 127 for c in text):
                return 'JA'
            return 'EN'
    except Exception as e:
        print(f"言語検出に失敗しました: {e}")
        # 文字種で判断
        if any(ord(c) > 127 for c in text):
            return 'JA'
        return 'EN'


def is_single_word(text):
    """テキストが単一の単語かどうかをチェック"""
    cleaned_text = text.strip()
    return ' ' not in cleaned_text and len(cleaned_text) <= 30
