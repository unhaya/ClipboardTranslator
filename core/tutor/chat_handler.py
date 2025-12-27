# ClipboardTranslator v1.00 - Tutor Chat Handler
"""
家庭教師モードのチャット処理を担当するモジュール
- 会話履歴管理（ハイブリッド方式）
- トピック抽出
- コンテキスト構築
- 翻訳履歴検索連携
"""
import re
from config.settings import config
from core.translation import query_claude_api
from core.network import is_connected


class TutorChatHandler:
    """家庭教師モードのチャット処理クラス"""

    def __init__(self, history_manager=None):
        """
        初期化

        Parameters:
        history_manager: TranslationHistoryインスタンス（履歴検索用）
        """
        self.conversation_history = []
        self.topics = []  # 過去の話題キーワード
        self.history_manager = history_manager

    def extract_topics_from_message(self, message):
        """
        メッセージからトピックキーワードを抽出（ローカル処理）

        Parameters:
        message (str): メッセージテキスト

        Returns:
        list: 抽出されたキーワードのリスト（最大5個）
        """
        # 英単語を抽出（3文字以上）
        english_words = re.findall(r'\b[a-zA-Z]{3,}\b', message)
        # 日本語のキーワード（カタカナ語、漢字を含む単語）
        japanese_keywords = re.findall(r'[ァ-ヶー]{2,}|[一-龥]{2,}', message)
        return list(set(english_words + japanese_keywords))[:5]

    def search_relevant_history(self, message, max_results=3):
        """
        ユーザーのメッセージに関連する翻訳履歴を検索

        Parameters:
        message (str): ユーザーのメッセージ
        max_results (int): 最大取得件数

        Returns:
        list: 関連する履歴エントリのリスト
        """
        if not self.history_manager:
            return []

        # メッセージからキーワードを抽出
        keywords = self.extract_topics_from_message(message)
        if not keywords:
            return []

        relevant_entries = []
        seen_texts = set()

        # 各キーワードで履歴を検索
        for keyword in keywords:
            results = self.history_manager.search_history(keyword)
            for entry in results:
                # 重複を避ける
                text_key = entry.get('original_text', '')
                if text_key not in seen_texts:
                    seen_texts.add(text_key)
                    relevant_entries.append(entry)

                    if len(relevant_entries) >= max_results:
                        break

            if len(relevant_entries) >= max_results:
                break

        return relevant_entries

    def build_context(self, user_message, max_recent=3):
        """
        ハイブリッド方式で会話コンテキストを構築
        - 過去の話題: キーワードのみ（ローカル生成、APIコストゼロ）
        - 翻訳履歴: 関連する履歴を検索して追加
        - 直近N件: そのまま送る

        Parameters:
        user_message (str): 現在のユーザーメッセージ
        max_recent (int): 直近の会話履歴数

        Returns:
        str: 構築されたコンテキスト文字列
        """
        context_parts = []

        # 1. 過去の話題キーワード
        if self.topics:
            unique_topics = list(dict.fromkeys(self.topics))[:15]
            context_parts.append(f"過去の話題: {', '.join(unique_topics)}")

        # 2. 関連する翻訳履歴
        relevant_history = self.search_relevant_history(user_message)
        if relevant_history:
            context_parts.append("\n関連する学習履歴:")
            for entry in relevant_history:
                original = entry.get('original_text', '')[:50]
                translated = entry.get('translated_text', '')[:100]
                entry_type = entry.get('translation_type', 'normal')
                if entry_type == 'dictionary':
                    context_parts.append(f"- 辞書検索: {original} → {translated}...")
                else:
                    context_parts.append(f"- 翻訳: {original} → {translated}...")

        # 3. 直近の会話（そのまま送る）
        recent_history = self.conversation_history[-max_recent * 2:]
        if recent_history:
            context_parts.append("\n直近の会話:")
            for entry in recent_history:
                role_label = "ユーザー" if entry['role'] == 'user' else "先生"
                content = entry['content'][:200] + "..." if len(entry['content']) > 200 else entry['content']
                context_parts.append(f"{role_label}: {content}")

        return "\n".join(context_parts)

    def add_to_history(self, role, content):
        """
        会話履歴に追加し、古い履歴からトピックを抽出

        Parameters:
        role (str): 'user' または 'assistant'
        content (str): メッセージ内容
        """
        max_history = int(config.get('Settings', 'tutor_max_history', fallback='10'))

        # 履歴に追加
        self.conversation_history.append({
            'role': role,
            'content': content
        })

        # トピックを抽出
        topics = self.extract_topics_from_message(content)
        self.topics.extend(topics)

        # 最大履歴数を超えた場合、古いものを削除
        max_entries = max_history * 2  # user + assistant
        if len(self.conversation_history) > max_entries:
            self.conversation_history = self.conversation_history[-max_entries:]

        # トピックリストも制限
        if len(self.topics) > 30:
            self.topics = self.topics[-30:]

    def process_message(self, message, on_success=None, on_error=None):
        """
        家庭教師モードのメッセージを処理

        Parameters:
        message (str): ユーザーのメッセージ
        on_success (callable): 成功時のコールバック(response)
        on_error (callable): エラー時のコールバック(error_message)

        Returns:
        str or None: 応答テキスト、エラーの場合はNone
        """
        try:
            # 家庭教師モードが無効な場合
            tutor_enabled = config.get('Settings', 'tutor_enabled', fallback='True')
            if tutor_enabled.lower() != 'true':
                error_msg = "家庭教師モードは無効に設定されています。設定画面で有効にしてください。"
                if on_error:
                    on_error(error_msg)
                return None

            claude_api_key = config.get('Settings', 'claude_api_key', fallback='')
            if not claude_api_key:
                error_msg = "Claude APIキーが設定されていません。設定画面で設定してください。"
                if on_error:
                    on_error(error_msg)
                return None

            if not is_connected():
                error_msg = "インターネット接続がありません。"
                if on_error:
                    on_error(error_msg)
                return None

            # ユーザーメッセージを履歴に追加
            self.add_to_history('user', message)

            # 設定から家庭教師用プロンプトを取得
            from config.constants import DEFAULT_SETTINGS
            default_prompt = DEFAULT_SETTINGS.get('tutor_system_prompt', '')
            system_prompt = config.get('Settings', 'tutor_system_prompt', fallback=default_prompt)

            # ハイブリッド方式でコンテキストを構築
            max_recent = int(config.get('Settings', 'tutor_max_history', fallback='10')) // 3
            max_recent = max(1, min(max_recent, 5))  # 1-5の範囲
            context = self.build_context(message, max_recent=max_recent)

            # プロンプトを構築
            if context:
                tutor_prompt = f"""{system_prompt}

{context}

ユーザーの発言：
{message}"""
            else:
                tutor_prompt = f"""{system_prompt}

ユーザーの発言：
{message}"""

            # 設定からモデルを取得
            tutor_model = config.get('Settings', 'tutor_model', fallback='sonnet')

            # 家庭教師モードで応答を取得
            response = query_claude_api(message, tutor_prompt, claude_api_key, model_type=tutor_model)

            if response:
                # 応答を履歴に追加
                self.add_to_history('assistant', response)
                if on_success:
                    on_success(response)
                return response
            else:
                error_msg = "申し訳ありません、応答を取得できませんでした。"
                if on_error:
                    on_error(error_msg)
                return None

        except Exception as e:
            error_msg = f"エラーが発生しました: {e}"
            if on_error:
                on_error(error_msg)
            return None

    def clear_history(self):
        """会話履歴とトピックをクリア"""
        self.conversation_history = []
        self.topics = []
