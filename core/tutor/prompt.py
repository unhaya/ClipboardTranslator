# ClipboardTranslator v1.00 - Tutor Prompt Builder
# 家庭教師用プロンプト生成モジュール


class TutorPromptBuilder:
    """家庭教師用のプロンプトを構築するクラス"""

    # システム指示（固定）
    SYSTEM_INSTRUCTION = """丁寧かつ親しみやすい家庭教師として回答。簡潔に。Markdown可。"""

    # 起動時の定型応答
    GREETING_RESPONSES = [
        "何かお聞きになりたいことはありますか？",
        "はい、何でもお聞きください。",
        "何かお困りのことはありますか？",
    ]

    # 終了時の定型応答
    FAREWELL_RESPONSES = [
        "どういたしまして。またいつでもお聞きください。",
        "お役に立てて良かったです。また何かあればお声がけください。",
        "また一緒に勉強しましょう。",
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
