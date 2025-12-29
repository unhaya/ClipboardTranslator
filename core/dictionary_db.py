# ClipboardTranslator v1.00 - SQLite Dictionary Module
import os
import sqlite3
import csv
from typing import Optional, Dict, List, Tuple

# データベースファイルパス
DB_PATH = None
_connection = None


def get_db_path(data_dir: str) -> str:
    """データベースファイルのパスを取得"""
    return os.path.join(data_dir, "dictionary.db")


def get_connection() -> sqlite3.Connection:
    """データベース接続を取得（シングルトン）"""
    global _connection
    if _connection is None:
        if DB_PATH is None:
            raise RuntimeError("Database not initialized. Call init_database() first.")
        _connection = sqlite3.connect(DB_PATH, check_same_thread=False)
        _connection.row_factory = sqlite3.Row
    return _connection


def init_database(data_dir: str) -> bool:
    """
    データベースを初期化する

    Parameters:
    data_dir (str): データディレクトリのパス

    Returns:
    bool: 初期化が成功したかどうか
    """
    global DB_PATH, _connection

    try:
        DB_PATH = get_db_path(data_dir)

        # 既存の接続を閉じる
        if _connection is not None:
            _connection.close()
            _connection = None

        conn = get_connection()
        cursor = conn.cursor()

        # 辞書テーブルを作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dictionary (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                meaning TEXT NOT NULL,
                source TEXT NOT NULL,
                priority INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # インデックスを作成
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_word ON dictionary(word)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_source ON dictionary(source)')
        cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_word_source ON dictionary(word, source)')

        # メタデータテーブルを作成（辞書ソースの管理用）
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dictionary_sources (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                word_count INTEGER DEFAULT 0,
                priority INTEGER DEFAULT 0,
                enabled INTEGER DEFAULT 1,
                imported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 翻訳履歴テーブルを作成
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS translation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                original_text TEXT NOT NULL,
                translated_text TEXT NOT NULL,
                source_lang TEXT NOT NULL,
                target_lang TEXT NOT NULL,
                translation_type TEXT DEFAULT 'normal',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 履歴用インデックス
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_original ON translation_history(original_text)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_type ON translation_history(translation_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_history_created ON translation_history(created_at DESC)')

        conn.commit()
        print(f"データベースを初期化しました: {DB_PATH}")
        return True

    except Exception as e:
        print(f"データベース初期化エラー: {e}")
        return False


def close_database():
    """データベース接続を閉じる"""
    global _connection
    if _connection is not None:
        _connection.close()
        _connection = None


def get_source_info(source_name: str) -> Optional[Dict]:
    """辞書ソースの情報を取得"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'SELECT * FROM dictionary_sources WHERE name = ?',
            (source_name,)
        )
        row = cursor.fetchone()
        if row:
            return dict(row)
        return None
    except Exception as e:
        print(f"ソース情報取得エラー: {e}")
        return None


def register_source(name: str, description: str = "", priority: int = 0) -> bool:
    """辞書ソースを登録"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO dictionary_sources (name, description, priority)
            VALUES (?, ?, ?)
        ''', (name, description, priority))
        conn.commit()
        return True
    except Exception as e:
        print(f"ソース登録エラー: {e}")
        return False


def update_source_count(source_name: str, count: int) -> bool:
    """辞書ソースの単語数を更新"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE dictionary_sources SET word_count = ? WHERE name = ?',
            (count, source_name)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"ソース更新エラー: {e}")
        return False


def import_dictionary_data(words: Dict[str, str], source: str, priority: int = 0) -> int:
    """
    辞書データをインポートする

    Parameters:
    words (dict): {単語: 意味} の辞書
    source (str): 辞書ソース名 (例: 'custom', 'ngsl', 'ejdict')
    priority (int): 優先度（高いほど優先）

    Returns:
    int: インポートした単語数
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        count = 0
        for word, meaning in words.items():
            try:
                cursor.execute('''
                    INSERT OR REPLACE INTO dictionary (word, meaning, source, priority)
                    VALUES (?, ?, ?, ?)
                ''', (word.lower().strip(), meaning.strip(), source, priority))
                count += 1
            except Exception as e:
                print(f"単語インポートエラー ({word}): {e}")
                continue

        conn.commit()

        # ソース情報を更新
        update_source_count(source, count)

        print(f"[{source}] {count}件の単語をインポートしました")
        return count

    except Exception as e:
        print(f"辞書インポートエラー: {e}")
        return 0


def import_from_csv_ngsl(file_path: str, source: str = "ngsl", priority: int = 50) -> int:
    """
    NGSL形式のCSVファイルからインポート
    フォーマット: entry,meaning
    """
    try:
        if not os.path.exists(file_path):
            print(f"ファイルが見つかりません: {file_path}")
            return 0

        # ソースを登録
        register_source(source, "NGSL (New General Service List)", priority)

        words = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if 'entry' in row and 'meaning' in row:
                    word = row['entry'].strip().lower()
                    meaning = row['meaning'].strip()
                    if word and meaning:
                        words[word] = meaning

        return import_dictionary_data(words, source, priority)

    except Exception as e:
        print(f"NGSL CSVインポートエラー: {e}")
        return 0


def import_from_ejdict(file_path: str, source: str = "ejdict", priority: int = 40) -> int:
    """
    ejdict-hand形式のテキストファイルからインポート
    フォーマット: word\tmeaning
    """
    try:
        if not os.path.exists(file_path):
            print(f"ファイルが見つかりません: {file_path}")
            return 0

        # ソースを登録
        register_source(source, "ejdict-hand (パブリックドメイン英和辞書)", priority)

        words = {}
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '\t' not in line:
                    continue
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    word = parts[0].strip().lower()
                    meaning = parts[1].strip()
                    if word and meaning:
                        words[word] = meaning

        return import_dictionary_data(words, source, priority)

    except Exception as e:
        print(f"ejdictインポートエラー: {e}")
        return 0


def import_from_dict(words: Dict[str, str], source: str = "custom",
                     description: str = "カスタム辞書", priority: int = 100) -> int:
    """
    Pythonの辞書からインポート
    """
    try:
        register_source(source, description, priority)
        return import_dictionary_data(words, source, priority)
    except Exception as e:
        print(f"辞書インポートエラー: {e}")
        return 0


def lookup_word(word: str) -> Optional[str]:
    """
    単語を検索する（優先度の高い順）

    Parameters:
    word (str): 検索する単語

    Returns:
    str or None: 意味（見つからない場合はNone）
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 優先度の高い順に検索
        cursor.execute('''
            SELECT d.meaning FROM dictionary d
            JOIN dictionary_sources s ON d.source = s.name
            WHERE d.word = ? AND s.enabled = 1
            ORDER BY d.priority DESC, s.priority DESC
            LIMIT 1
        ''', (word.lower().strip(),))

        row = cursor.fetchone()
        if row:
            return row['meaning']
        return None

    except Exception as e:
        print(f"単語検索エラー: {e}")
        return None


def lookup_word_all(word: str) -> List[Dict]:
    """
    単語を全ソースから検索する

    Returns:
    list: [{source, meaning, priority}, ...]
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute('''
            SELECT d.source, d.meaning, d.priority FROM dictionary d
            JOIN dictionary_sources s ON d.source = s.name
            WHERE d.word = ? AND s.enabled = 1
            ORDER BY d.priority DESC, s.priority DESC
        ''', (word.lower().strip(),))

        results = []
        for row in cursor.fetchall():
            results.append({
                'source': row['source'],
                'meaning': row['meaning'],
                'priority': row['priority']
            })
        return results

    except Exception as e:
        print(f"単語検索エラー: {e}")
        return []


def get_dictionary_stats() -> Dict:
    """辞書の統計情報を取得"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 総単語数
        cursor.execute('SELECT COUNT(*) as count FROM dictionary')
        total = cursor.fetchone()['count']

        # ソース別の統計
        cursor.execute('''
            SELECT name, word_count, enabled, priority
            FROM dictionary_sources
            ORDER BY priority DESC
        ''')
        sources = []
        for row in cursor.fetchall():
            sources.append({
                'name': row['name'],
                'word_count': row['word_count'],
                'enabled': bool(row['enabled']),
                'priority': row['priority']
            })

        return {
            'total': total,
            'sources': sources
        }

    except Exception as e:
        print(f"統計取得エラー: {e}")
        return {'total': 0, 'sources': []}


def enable_source(source_name: str, enabled: bool = True) -> bool:
    """辞書ソースの有効/無効を切り替え"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            'UPDATE dictionary_sources SET enabled = ? WHERE name = ?',
            (1 if enabled else 0, source_name)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"ソース切り替えエラー: {e}")
        return False


def delete_source(source_name: str) -> bool:
    """辞書ソースとその単語を削除"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 単語を削除
        cursor.execute('DELETE FROM dictionary WHERE source = ?', (source_name,))

        # ソース情報を削除
        cursor.execute('DELETE FROM dictionary_sources WHERE name = ?', (source_name,))

        conn.commit()
        print(f"辞書ソース '{source_name}' を削除しました")
        return True

    except Exception as e:
        print(f"ソース削除エラー: {e}")
        return False


def add_word(word: str, meaning: str, source: str = "user") -> bool:
    """単語を追加"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # ユーザー辞書がなければ作成
        if source == "user":
            register_source("user", "ユーザー辞書", priority=200)

        cursor.execute('''
            INSERT OR REPLACE INTO dictionary (word, meaning, source, priority)
            VALUES (?, ?, ?, ?)
        ''', (word.lower().strip(), meaning.strip(), source, 200))

        conn.commit()
        return True

    except Exception as e:
        print(f"単語追加エラー: {e}")
        return False


def remove_word(word: str, source: str = None) -> bool:
    """単語を削除"""
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if source:
            cursor.execute(
                'DELETE FROM dictionary WHERE word = ? AND source = ?',
                (word.lower().strip(), source)
            )
        else:
            cursor.execute(
                'DELETE FROM dictionary WHERE word = ?',
                (word.lower().strip(),)
            )

        conn.commit()
        return True

    except Exception as e:
        print(f"単語削除エラー: {e}")
        return False


# ========== 翻訳履歴関連 ==========

def add_history_entry(original_text: str, translated_text: str,
                      source_lang: str, target_lang: str,
                      translation_type: str = "normal") -> bool:
    """
    翻訳履歴を追加する（同じ原文・言語・タイプの既存エントリは更新）

    Parameters:
    original_text (str): 原文
    translated_text (str): 翻訳されたテキスト
    source_lang (str): 原文の言語コード
    target_lang (str): 翻訳先の言語コード
    translation_type (str): 翻訳タイプ ('normal', 'dictionary', 'speech')

    Returns:
    bool: 成功したかどうか
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # 同じ原文、ソース言語、タイプの既存エントリを削除
        cursor.execute('''
            DELETE FROM translation_history
            WHERE original_text = ? AND source_lang = ? AND translation_type = ?
        ''', (original_text, source_lang, translation_type))

        # 新しいエントリを追加
        cursor.execute('''
            INSERT INTO translation_history
            (original_text, translated_text, source_lang, target_lang, translation_type)
            VALUES (?, ?, ?, ?, ?)
        ''', (original_text, translated_text, source_lang, target_lang, translation_type))

        conn.commit()
        return True

    except Exception as e:
        print(f"履歴追加エラー: {e}")
        return False


def get_history(max_items: int = None, filter_type: str = None) -> List[Dict]:
    """
    翻訳履歴を取得する

    Parameters:
    max_items (int): 取得する最大数（Noneで無制限）
    filter_type (str): フィルタリングするタイプ（Noneで全て）

    Returns:
    list: 履歴エントリのリスト
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if filter_type:
            query = '''
                SELECT * FROM translation_history
                WHERE translation_type = ?
                ORDER BY created_at DESC
            '''
            params = [filter_type]
        else:
            query = '''
                SELECT * FROM translation_history
                ORDER BY created_at DESC
            '''
            params = []

        if max_items:
            query += ' LIMIT ?'
            params.append(max_items)

        cursor.execute(query, params)

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['id'],
                'timestamp': row['created_at'],
                'original_text': row['original_text'],
                'translated_text': row['translated_text'],
                'source_lang': row['source_lang'],
                'target_lang': row['target_lang'],
                'translation_type': row['translation_type']
            })
        return results

    except Exception as e:
        print(f"履歴取得エラー: {e}")
        return []


def search_history(query: str) -> List[Dict]:
    """
    翻訳履歴を検索する

    Parameters:
    query (str): 検索クエリ

    Returns:
    list: 検索結果のリスト
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        search_pattern = f'%{query}%'
        cursor.execute('''
            SELECT * FROM translation_history
            WHERE original_text LIKE ? OR translated_text LIKE ?
            ORDER BY created_at DESC
        ''', (search_pattern, search_pattern))

        results = []
        for row in cursor.fetchall():
            results.append({
                'id': row['id'],
                'timestamp': row['created_at'],
                'original_text': row['original_text'],
                'translated_text': row['translated_text'],
                'source_lang': row['source_lang'],
                'target_lang': row['target_lang'],
                'translation_type': row['translation_type']
            })
        return results

    except Exception as e:
        print(f"履歴検索エラー: {e}")
        return []


def find_cached_translation(original_text: str, source_lang: str,
                            translation_type: str = None) -> Optional[Dict]:
    """
    キャッシュから翻訳を検索する

    Parameters:
    original_text (str): 原文
    source_lang (str): 原文の言語
    translation_type (str): 翻訳タイプ（Noneで全タイプ検索）

    Returns:
    dict or None: キャッシュされた翻訳
    """
    try:
        conn = get_connection()
        cursor = conn.cursor()

        if translation_type:
            cursor.execute('''
                SELECT * FROM translation_history
                WHERE original_text = ? AND source_lang = ? AND translation_type = ?
                ORDER BY created_at DESC LIMIT 1
            ''', (original_text, source_lang, translation_type))
        else:
            cursor.execute('''
                SELECT * FROM translation_history
                WHERE original_text = ? AND source_lang = ?
                ORDER BY created_at DESC LIMIT 1
            ''', (original_text, source_lang))

        row = cursor.fetchone()
        if row:
            return {
                'id': row['id'],
                'timestamp': row['created_at'],
                'original_text': row['original_text'],
                'translated_text': row['translated_text'],
                'source_lang': row['source_lang'],
                'target_lang': row['target_lang'],
                'translation_type': row['translation_type']
            }
        return None

    except Exception as e:
        print(f"キャッシュ検索エラー: {e}")
        return None


def clear_history() -> bool:
    """翻訳履歴をすべてクリアする"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM translation_history')
        conn.commit()
        print("翻訳履歴をクリアしました")
        return True
    except Exception as e:
        print(f"履歴クリアエラー: {e}")
        return False


def delete_history_entry(entry_id: int) -> bool:
    """特定の履歴エントリを削除"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM translation_history WHERE id = ?', (entry_id,))
        conn.commit()
        return True
    except Exception as e:
        print(f"履歴削除エラー: {e}")
        return False


def get_history_count() -> int:
    """履歴の件数を取得"""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT COUNT(*) as count FROM translation_history')
        return cursor.fetchone()['count']
    except Exception as e:
        print(f"履歴件数取得エラー: {e}")
        return 0


def import_history_from_json(history_list: List[Dict]) -> int:
    """
    JSONから履歴をインポートする

    Parameters:
    history_list (list): 履歴エントリのリスト

    Returns:
    int: インポートした件数
    """
    try:
        count = 0
        for entry in history_list:
            if add_history_entry(
                entry.get('original_text', ''),
                entry.get('translated_text', ''),
                entry.get('source_lang', 'EN'),
                entry.get('target_lang', 'JA'),
                entry.get('translation_type', 'normal')
            ):
                count += 1
        print(f"{count}件の履歴をインポートしました")
        return count
    except Exception as e:
        print(f"履歴インポートエラー: {e}")
        return 0
