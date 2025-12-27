# ClipboardTranslator v1.00 - Tutor Prompt Builder
# 家庭教師用プロンプト生成モジュール


class TutorPromptBuilder:
    """家庭教師用のプロンプトを構築するクラス"""

    # システム指示（固定）
    SYSTEM_INSTRUCTION = """あなたはユーザー専属の家庭教師です。
以下のルールに従って返答してください：

1. 教科書調にしない - フレンドリーに話す
2. 過去の履歴を「覚えている体」で話す
3. 共感を最初に入れる - ユーザーの気持ちに寄り添う
4. 長文説明は禁止 - 簡潔に、わかりやすく
5. 必要なら質問で返す - 理解度を確認する
6. 励ましの言葉を適度に入れる"""

    # 起動時の定型応答
    GREETING_RESPONSES = [
        "どうしたの？何について聞きたい？",
        "うん、なんでも聞いて！",
        "いいよ！何が気になってる？",
    ]

    # 終了時の定型応答
    FAREWELL_RESPONSES = [
        "どういたしまして。またいつでも聞いてね！",
        "よかった！また何かあったらいつでもどうぞ。",
        "うん、また一緒に勉強しよう！",
    ]

    @classmethod
    def build_prompt(cls, user_input: str, retrieved_chunks: str = "",
                     conversation_context: str = "") -> str:
        """
        家庭教師用プロンプトを構築

        Parameters:
            user_input: ユーザーの発言
            retrieved_chunks: RAGで取得した履歴チャンク
            conversation_context: 直近の会話コンテキスト

        Returns:
            構築されたプロンプト
        """
        parts = [cls.SYSTEM_INSTRUCTION]

        # 履歴情報がある場合
        if retrieved_chunks:
            parts.append(f"""
以下は、これまでのユーザーの学習履歴の一部です。
この情報を踏まえて返答してください。

--- 学習履歴 ---
{retrieved_chunks}
----------------""")

        # 会話コンテキストがある場合
        if conversation_context:
            parts.append(f"""
以下は直近の会話です：

{conversation_context}""")

        # ユーザーの発言
        parts.append(f"""
ユーザーの発言：
{user_input}

この発言に対して、雑談するように自然に返答してください。""")

        return "\n".join(parts)

    @classmethod
    def get_greeting(cls) -> str:
        """起動時の挨拶を取得"""
        import random
        return random.choice(cls.GREETING_RESPONSES)

    @classmethod
    def get_farewell(cls) -> str:
        """終了時の挨拶を取得"""
        import random
        return random.choice(cls.FAREWELL_RESPONSES)
