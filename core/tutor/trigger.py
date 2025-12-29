# ClipboardTranslator v1.00 - Trigger Detection
# トリガーフレーズ検出モジュール


class TriggerDetector:
    """起動・終了トリガーを検出するクラス"""

    # 起動トリガーフレーズ（部分一致）
    START_TRIGGERS = [
        'ちょっと聞きたい',
        '教えて',
        '質問していい',
        '相談なんだけど',
        '少し聞いてもいい',
        '聞いてもいい',
        'わからない',
        '分からない',
        'どういう意味',
        'なんで',
        '何で',
        'どうして',
        '説明して',
        'ヘルプ',
        'help',
    ]

    # 終了トリガーフレーズ（部分一致）
    END_TRIGGERS = [
        'ありがとう',
        'もう大丈夫',
        '分かった',
        'わかった',
        '今日はここまで',
        'おしまい',
        'さようなら',
        'じゃあね',
        'バイバイ',
        'またね',
        '終わり',
        'おわり',
    ]

    @classmethod
    def detect_start_trigger(cls, text: str) -> bool:
        """
        起動トリガーを検出する

        Parameters:
            text: 入力テキスト

        Returns:
            起動トリガーが含まれていればTrue
        """
        if not text:
            return False

        text_lower = text.lower().strip()

        for trigger in cls.START_TRIGGERS:
            if trigger.lower() in text_lower:
                return True

        return False

    @classmethod
    def detect_end_trigger(cls, text: str) -> bool:
        """
        終了トリガーを検出する

        Parameters:
            text: 入力テキスト

        Returns:
            終了トリガーが含まれていればTrue
        """
        if not text:
            return False

        text_lower = text.lower().strip()

        for trigger in cls.END_TRIGGERS:
            if trigger.lower() in text_lower:
                return True

        return False

    @classmethod
    def get_trigger_type(cls, text: str) -> str:
        """
        テキストのトリガータイプを判定

        Parameters:
            text: 入力テキスト

        Returns:
            'start', 'end', または 'none'
        """
        if cls.detect_end_trigger(text):
            return 'end'
        elif cls.detect_start_trigger(text):
            return 'start'
        else:
            return 'none'

    @classmethod
    def remove_trigger_phrase(cls, text: str) -> str:
        """
        トリガーフレーズを除去したテキストを返す
        （トリガー自体はRAGに渡さないため）

        Parameters:
            text: 入力テキスト

        Returns:
            トリガーフレーズを除去したテキスト
        """
        result = text
        all_triggers = cls.START_TRIGGERS + cls.END_TRIGGERS

        for trigger in all_triggers:
            result = result.replace(trigger, '')

        return result.strip()
