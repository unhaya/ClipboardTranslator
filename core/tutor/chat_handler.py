# ClipboardTranslator v1.00 - Tutor Chat Handler
"""
家庭教師モードのチャット処理を担当するモジュール
- 会話履歴管理（ハイブリッド方式）
- トピック抽出（形態素解析対応）
- コンテキスト構築
- 高精度履歴検索（BM25 + 時間的重み付け）
"""
from config.settings import config
from config.constants import get_message
from core.translation import query_claude_api
from core.network import is_connected
from .search import SmartHistorySearcher, extract_keywords


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
        self.searcher = SmartHistorySearcher(recency_weight=0.3, decay_days=30)
        self._last_history_count = 0  # 履歴の変更検知用

    def extract_topics_from_message(self, message):
        """
        メッセージからトピックキーワードを抽出（形態素解析対応）

        Parameters:
        message (str): メッセージテキスト

        Returns:
        list: 抽出されたキーワードのリスト（最大5個）
        """
        return extract_keywords(message, max_keywords=5)

    def _refresh_searcher_if_needed(self):
        """履歴が更新されていればSearcherを再学習"""
        if not self.history_manager:
            return

        try:
            # 全履歴を取得
            all_history = self.history_manager.get_history()
            current_count = len(all_history) if all_history else 0

            # 履歴が変更されていれば再学習
            if current_count != self._last_history_count:
                self.searcher.fit(all_history)
                self._last_history_count = current_count
        except Exception as e:
            print(f"Searcher更新エラー: {e}")

    def search_relevant_history(self, message, max_results=3):
        """
        ユーザーのメッセージに関連する翻訳履歴を検索（BM25 + 時間的重み付け）

        Parameters:
        message (str): ユーザーのメッセージ
        max_results (int): 最大取得件数

        Returns:
        tuple: (関連する履歴エントリのリスト, 検索メタデータ)
               メタデータ: {'count': int, 'dates': list[str]}
        """
        if not self.history_manager:
            return [], {'count': 0, 'dates': []}

        # Searcherを最新状態に更新
        self._refresh_searcher_if_needed()

        # BM25 + 時間的重み付けで検索
        results = self.searcher.search(message, top_k=max_results)

        # メタデータを構築
        metadata = {
            'count': len(results),
            'dates': []
        }

        for entry in results:
            timestamp = entry.get('timestamp', '')
            if timestamp:
                # YYYY-MM-DD HH:MM:SS から MM/DD を抽出
                try:
                    date_part = timestamp.split(' ')[0]  # YYYY-MM-DD
                    parts = date_part.split('-')
                    if len(parts) == 3:
                        formatted_date = f"{int(parts[1])}/{int(parts[2])}"
                        if formatted_date not in metadata['dates']:
                            metadata['dates'].append(formatted_date)
                except (ValueError, IndexError):
                    pass

        return results, metadata

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
        tuple: (構築されたコンテキスト文字列, 検索メタデータ)
        """
        context_parts = []
        search_metadata = {'count': 0, 'dates': []}

        # 1. 過去の話題キーワード
        if self.topics:
            unique_topics = list(dict.fromkeys(self.topics))[:15]
            context_parts.append(f"過去の話題: {', '.join(unique_topics)}")

        # 2. 関連する翻訳履歴
        relevant_history, search_metadata = self.search_relevant_history(user_message)
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
                lang = config.get("response_language", "EN")
                role_label = get_message("tutor_user_label", lang) if entry['role'] == 'user' else get_message("tutor_ai_label", lang)
                content = entry['content'][:200] + "..." if len(entry['content']) > 200 else entry['content']
                context_parts.append(f"{role_label}: {content}")

        return "\n".join(context_parts), search_metadata

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

    def process_message(self, message, on_success=None, on_error=None, on_search_info=None):
        """
        家庭教師モードのメッセージを処理

        Parameters:
        message (str): ユーザーのメッセージ
        on_success (callable): 成功時のコールバック(response)
        on_error (callable): エラー時のコールバック(error_message)
        on_search_info (callable): 検索情報コールバック(metadata)
                                   metadata: {'count': int, 'dates': list[str]}

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
            context, search_metadata = self.build_context(message, max_recent=max_recent)

            # 検索情報をコールバックで通知
            if on_search_info:
                on_search_info(search_metadata)

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
