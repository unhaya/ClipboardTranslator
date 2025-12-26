# ClipboardTranslator v1.00 - Translation History Module
import os
import json
from datetime import datetime


class TranslationHistory:
    """翻訳履歴を管理するクラス"""

    def __init__(self, app=None, history_file_path=None):
        """
        TranslationHistoryクラスの初期化

        Parameters:
        app: メインアプリケーションのインスタンス（オプション）
        history_file_path (str): 履歴ファイルのパス。Noneの場合はデフォルトパスを使用
        """
        self.app = app

        if history_file_path is None:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.history_file = os.path.join(script_dir, 'data', 'translation_history.json')
        else:
            self.history_file = history_file_path

        self.history = []
        self.max_history_size = 100

        self.load_history()

    def load_history(self):
        """履歴ファイルから翻訳履歴を読み込む"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                    print(f"履歴ファイルから{len(self.history)}件の翻訳履歴を読み込みました")
        except Exception as e:
            print(f"履歴ファイルの読み込みに失敗しました: {e}")
            self.history = []

    def save_history(self):
        """翻訳履歴をファイルに保存する"""
        try:
            history_dir = os.path.dirname(self.history_file)
            if not os.path.exists(history_dir):
                os.makedirs(history_dir)

            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)

            print(f"履歴ファイルに{len(self.history)}件の翻訳履歴を保存しました")
        except Exception as e:
            print(f"履歴ファイルの保存に失敗しました: {e}")

    def add_entry(self, original_text, translated_text, source_lang, target_lang, translation_type="normal"):
        """
        新しい翻訳履歴を追加する（既存の同じソーステキストと同じタイプのエントリは上書き）

        Parameters:
        original_text (str): 原文
        translated_text (str): 翻訳されたテキスト
        source_lang (str): 原文の言語コード ('JA', 'EN', etc.)
        target_lang (str): 翻訳先の言語コード ('JA', 'EN', etc.)
        translation_type (str): 翻訳タイプ ('normal', 'dictionary', 'speech')
        """
        # 同じ原文、同じソース言語、同じ翻訳タイプのエントリが既にある場合は削除
        self.history = [entry for entry in self.history
                        if not (entry['original_text'] == original_text and
                                entry['source_lang'] == source_lang and
                                entry['translation_type'] == translation_type)]

        new_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'original_text': original_text,
            'translated_text': translated_text,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'translation_type': translation_type
        }

        self.history.insert(0, new_entry)

        if len(self.history) > self.max_history_size:
            self.history = self.history[:self.max_history_size]

        self.save_history()

    def get_history(self, max_items=None, filter_type=None):
        """
        翻訳履歴を取得する

        Parameters:
        max_items (int): 取得する履歴の最大数。Noneの場合はすべて取得
        filter_type (str): フィルタリングする翻訳タイプ。Noneの場合はフィルタリングしない

        Returns:
        list: 翻訳履歴のリスト
        """
        if filter_type:
            filtered_history = [entry for entry in self.history if entry['translation_type'] == filter_type]
        else:
            filtered_history = self.history

        if max_items:
            return filtered_history[:max_items]
        else:
            return filtered_history

    def search_history(self, query):
        """
        翻訳履歴を検索する

        Parameters:
        query (str): 検索クエリ

        Returns:
        list: 検索結果のリスト
        """
        query = query.lower()
        return [entry for entry in self.history
                if query in entry['original_text'].lower() or
                   query in entry['translated_text'].lower()]

    def clear_history(self):
        """翻訳履歴をすべてクリアする"""
        self.history = []
        self.save_history()
