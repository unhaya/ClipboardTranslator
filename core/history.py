# ClipboardTranslator v1.00 - Translation History Module
import os
import json
from datetime import datetime

# SQLiteモードフラグ
USE_SQLITE = False
_db_available = False


def init_history_db():
    """SQLiteモードを初期化"""
    global USE_SQLITE, _db_available
    try:
        from . import dictionary_db as db
        # DBが初期化済みかチェック
        if db.DB_PATH is not None:
            USE_SQLITE = True
            _db_available = True
            return True
    except Exception as e:
        print(f"履歴SQLite初期化エラー: {e}")
    return False


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

        self.history = []  # レガシー互換用

        # SQLiteモードを試行
        init_history_db()

        if USE_SQLITE and _db_available:
            self._migrate_json_to_sqlite()
            print("履歴: SQLiteモードで動作中")
        else:
            self.load_history()
            print("履歴: JSONモードで動作中")

    def _migrate_json_to_sqlite(self):
        """既存のJSON履歴をSQLiteに移行"""
        try:
            if not os.path.exists(self.history_file):
                return

            from . import dictionary_db as db

            # 既にSQLiteに履歴があればスキップ
            if db.get_history_count() > 0:
                return

            with open(self.history_file, 'r', encoding='utf-8') as f:
                json_history = json.load(f)

            if json_history:
                count = db.import_history_from_json(json_history)
                if count > 0:
                    # 移行成功したらJSONファイルをバックアップ
                    backup_file = self.history_file + '.backup'
                    os.rename(self.history_file, backup_file)
                    print(f"JSON履歴をSQLiteに移行しました ({count}件)")

        except Exception as e:
            print(f"履歴移行エラー: {e}")

    def load_history(self):
        """履歴ファイルから翻訳履歴を読み込む（レガシーモード用）"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
                    print(f"履歴ファイルから{len(self.history)}件の翻訳履歴を読み込みました")
        except Exception as e:
            print(f"履歴ファイルの読み込みに失敗しました: {e}")
            self.history = []

    def save_history(self):
        """翻訳履歴をファイルに保存する（レガシーモード用）"""
        # SQLiteモードでは何もしない
        if USE_SQLITE and _db_available:
            return

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
        # SQLiteモード
        if USE_SQLITE and _db_available:
            from . import dictionary_db as db
            db.add_history_entry(original_text, translated_text, source_lang, target_lang, translation_type)
            return

        # レガシーモード
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
        # SQLiteモード
        if USE_SQLITE and _db_available:
            from . import dictionary_db as db
            return db.get_history(max_items, filter_type)

        # レガシーモード
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
        # SQLiteモード
        if USE_SQLITE and _db_available:
            from . import dictionary_db as db
            return db.search_history(query)

        # レガシーモード
        query = query.lower()
        return [entry for entry in self.history
                if query in entry['original_text'].lower() or
                   query in entry['translated_text'].lower()]

    def find_cached(self, original_text, source_lang, translation_type=None):
        """
        キャッシュから翻訳を検索する

        Parameters:
        original_text (str): 原文
        source_lang (str): 原文の言語
        translation_type (str): 翻訳タイプ

        Returns:
        dict or None: キャッシュされた翻訳
        """
        # SQLiteモード
        if USE_SQLITE and _db_available:
            from . import dictionary_db as db
            return db.find_cached_translation(original_text, source_lang, translation_type)

        # レガシーモード
        for entry in self.history:
            if entry['original_text'] == original_text and entry['source_lang'] == source_lang:
                if translation_type is None or entry['translation_type'] == translation_type:
                    return entry
        return None

    def clear_history(self):
        """翻訳履歴をすべてクリアする"""
        # SQLiteモード
        if USE_SQLITE and _db_available:
            from . import dictionary_db as db
            db.clear_history()
            return

        # レガシーモード
        self.history = []
        self.save_history()
