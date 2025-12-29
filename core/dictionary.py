# ClipboardTranslator v1.00 - Dictionary Module
import os
import pickle
import csv

# 辞書データのグローバル変数（レガシー互換用）
COMMON_JA_WORDS = {}
COMMON_EN_WORDS = {}
NGSL_DICTIONARY = {}
EJDICT_DICTIONARY = {}

# SQLiteモードのフラグ
USE_SQLITE = False
_db_initialized = False


def init_dictionaries(data_dir, use_sqlite=True):
    """
    辞書データを初期化

    Parameters:
    data_dir (str): データディレクトリのパス
    use_sqlite (bool): SQLiteモードを使用するか
    """
    global COMMON_JA_WORDS, COMMON_EN_WORDS, NGSL_DICTIONARY, USE_SQLITE, _db_initialized

    USE_SQLITE = use_sqlite

    if use_sqlite:
        # SQLiteモード
        try:
            from . import dictionary_db as db
            if db.init_database(data_dir):
                _db_initialized = True

                # 既存データがなければインポート
                stats = db.get_dictionary_stats()
                if stats['total'] == 0:
                    print("初回起動: 辞書データをSQLiteにインポートします...")
                    _import_all_dictionaries(data_dir)
                else:
                    print(f"SQLite辞書を読み込みました: {stats['total']}単語")
                    for src in stats['sources']:
                        print(f"  - {src['name']}: {src['word_count']}単語")
                return
        except Exception as e:
            print(f"SQLite初期化エラー: {e}")
            print("レガシーモードにフォールバックします")
            USE_SQLITE = False

    # レガシーモード（従来の辞書読み込み）
    dict_data_path = os.path.join(data_dir, 'dictionary_data.py')
    if os.path.exists(dict_data_path):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("dictionary_data", dict_data_path)
            dict_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dict_module)
            COMMON_JA_WORDS = dict_module.COMMON_JA_WORDS
            COMMON_EN_WORDS = {v: k for k, v in COMMON_JA_WORDS.items()}
            print(f"辞書データを読み込みました: {len(COMMON_JA_WORDS)}単語")
        except Exception as e:
            print(f"辞書データ読み込みエラー: {e}")
            _init_basic_dictionary()
    else:
        _init_basic_dictionary()


def _import_all_dictionaries(data_dir):
    """全辞書データをSQLiteにインポート"""
    from . import dictionary_db as db

    total = 0

    # 1. カスタム辞書 (dictionary_data.py)
    dict_data_path = os.path.join(data_dir, 'dictionary_data.py')
    if os.path.exists(dict_data_path):
        try:
            import importlib.util
            spec = importlib.util.spec_from_file_location("dictionary_data", dict_data_path)
            dict_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(dict_module)
            if hasattr(dict_module, 'COMMON_JA_WORDS'):
                count = db.import_from_dict(
                    dict_module.COMMON_JA_WORDS,
                    source="custom_ja",
                    description="カスタム日本語→英語辞書",
                    priority=100
                )
                total += count
                # 逆引きもインポート
                en_words = {v: k for k, v in dict_module.COMMON_JA_WORDS.items()}
                count = db.import_from_dict(
                    en_words,
                    source="custom_en",
                    description="カスタム英語→日本語辞書",
                    priority=100
                )
                total += count
        except Exception as e:
            print(f"カスタム辞書インポートエラー: {e}")

    # 2. NGSL辞書
    ngsl_path = os.path.join(data_dir, 'ngsl-1.2-ja.csv')
    if os.path.exists(ngsl_path):
        count = db.import_from_csv_ngsl(ngsl_path, source="ngsl", priority=50)
        total += count

    # 3. ejdict
    ejdict_path = os.path.join(data_dir, 'ejdict-hand-utf8.txt')
    if os.path.exists(ejdict_path):
        count = db.import_from_ejdict(ejdict_path, source="ejdict", priority=40)
        total += count

    print(f"合計 {total} 単語をインポートしました")


def _init_basic_dictionary():
    """基本辞書を初期化"""
    global COMMON_JA_WORDS, COMMON_EN_WORDS
    COMMON_JA_WORDS = {
        '保存': 'save', '開く': 'open', '閉じる': 'close', '終了': 'exit', '削除': 'delete',
        'ファイル': 'file', 'フォルダ': 'folder', '設定': 'settings', '編集': 'edit',
    }
    COMMON_EN_WORDS = {v: k for k, v in COMMON_JA_WORDS.items()}


def save_dictionary_cache(dictionary, cache_file_path):
    """
    辞書データをキャッシュファイルに保存する

    Parameters:
    dictionary (dict): 保存する辞書データ
    cache_file_path (str): キャッシュファイルのパス

    Returns:
    bool: 保存が成功したかどうか
    """
    try:
        cache_dir = os.path.dirname(cache_file_path)
        if not os.path.exists(cache_dir):
            os.makedirs(cache_dir)

        with open(cache_file_path, 'wb') as f:
            pickle.dump(dictionary, f)
        return True
    except Exception as e:
        print(f"辞書キャッシュの保存に失敗しました: {e}")
        return False


def load_dictionary_cache(cache_file_path, source_file_path=None):
    """
    キャッシュファイルから辞書データを読み込む

    Parameters:
    cache_file_path (str): キャッシュファイルのパス
    source_file_path (str): 元のCSVファイルのパス（更新チェック用）

    Returns:
    dict or None: 読み込んだ辞書データ、またはNone（キャッシュが無効な場合）
    """
    try:
        if not os.path.exists(cache_file_path):
            return None

        if source_file_path and os.path.exists(source_file_path):
            cache_mtime = os.path.getmtime(cache_file_path)
            source_mtime = os.path.getmtime(source_file_path)
            if source_mtime > cache_mtime:
                print(f"ソースファイルがキャッシュよりも新しいため、キャッシュを更新します")
                return None

        with open(cache_file_path, 'rb') as f:
            return pickle.load(f)
    except Exception as e:
        print(f"辞書キャッシュの読み込みに失敗しました: {e}")
        return None


def load_ngsl_dictionary(file_path, use_cache=True):
    """
    NGSL形式のCSVファイルから英和辞書データを読み込む

    Parameters:
    file_path (str): NGSLのCSVファイルパス
    use_cache (bool): キャッシュを使用するかどうか

    Returns:
    tuple: (読み込んだ単語数, 読み込んだ辞書データ)
    """
    global NGSL_DICTIONARY

    cache_dir = os.path.join(os.path.dirname(file_path), "cache")
    cache_file = os.path.join(cache_dir, os.path.basename(file_path) + ".cache")

    if use_cache:
        cached_dict = load_dictionary_cache(cache_file, file_path)
        if cached_dict:
            print(f"キャッシュから{len(cached_dict)}個の単語を読み込みました")
            NGSL_DICTIONARY = cached_dict
            return len(cached_dict), cached_dict

    try:
        new_dict = {}
        counter = 0

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    if 'entry' in row and 'meaning' in row:
                        english_word = row['entry'].strip().lower()
                        japanese_meaning = row['meaning'].strip()

                        if english_word and japanese_meaning:
                            new_dict[english_word] = japanese_meaning
                            counter += 1
                except Exception as e:
                    print(f"行の処理中にエラー: {e}")
                    continue

        if use_cache and counter > 0:
            save_dictionary_cache(new_dict, cache_file)

        NGSL_DICTIONARY = new_dict
        print(f"NGSLから{counter}個の単語を読み込みました")
        return counter, new_dict
    except Exception as e:
        print(f"辞書ファイル読み込みエラー: {e}")
        return 0, {}


def load_ejdict(file_path, use_cache=True):
    """
    ejdict-hand形式のテキストファイルから英和辞書データを読み込む

    Parameters:
    file_path (str): ejdict-hand-utf8.txtのパス
    use_cache (bool): キャッシュを使用するかどうか

    Returns:
    tuple: (読み込んだ単語数, 読み込んだ辞書データ)
    """
    global EJDICT_DICTIONARY

    cache_dir = os.path.join(os.path.dirname(file_path), "cache")
    cache_file = os.path.join(cache_dir, os.path.basename(file_path) + ".cache")

    if use_cache:
        cached_dict = load_dictionary_cache(cache_file, file_path)
        if cached_dict:
            print(f"EJDictキャッシュから{len(cached_dict)}個の単語を読み込みました")
            EJDICT_DICTIONARY = cached_dict
            return len(cached_dict), cached_dict

    try:
        new_dict = {}
        counter = 0

        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or '\t' not in line:
                    continue
                parts = line.split('\t', 1)
                if len(parts) == 2:
                    english_word = parts[0].strip().lower()
                    japanese_meaning = parts[1].strip()
                    if english_word and japanese_meaning:
                        new_dict[english_word] = japanese_meaning
                        counter += 1

        if use_cache and counter > 0:
            save_dictionary_cache(new_dict, cache_file)

        EJDICT_DICTIONARY = new_dict
        print(f"EJDictから{counter}個の単語を読み込みました")
        return counter, new_dict
    except Exception as e:
        print(f"EJDict読み込みエラー: {e}")
        return 0, {}


def check_dictionary(text, source_lang):
    """
    ローカル辞書に登録されている単語かチェックして、あれば対応する翻訳を返す

    Parameters:
    text (str): 検索する単語
    source_lang (str): 原文の言語 ('JA' or 'EN')

    Returns:
    str or None: 翻訳結果（見つからない場合はNone）
    """
    text = text.strip().lower()

    # SQLiteモードの場合
    if USE_SQLITE and _db_initialized:
        try:
            from . import dictionary_db as db
            result = db.lookup_word(text)
            if result:
                return result
        except Exception as e:
            print(f"SQLite検索エラー: {e}")

    # レガシーモード（フォールバック）
    if source_lang == 'JA' and text in COMMON_JA_WORDS:
        return COMMON_JA_WORDS[text]
    elif source_lang == 'EN':
        if text in COMMON_EN_WORDS:
            return COMMON_EN_WORDS[text]
        if text in NGSL_DICTIONARY:
            return NGSL_DICTIONARY[text]
        if text in EJDICT_DICTIONARY:
            return EJDICT_DICTIONARY[text]

    return None


def get_dictionary_size():
    """辞書のサイズを取得"""
    # SQLiteモードの場合
    if USE_SQLITE and _db_initialized:
        try:
            from . import dictionary_db as db
            stats = db.get_dictionary_stats()
            result = {'total': stats['total']}
            for src in stats['sources']:
                result[src['name']] = src['word_count']
            return result
        except Exception as e:
            print(f"辞書サイズ取得エラー: {e}")

    # レガシーモード
    return {
        'ja': len(COMMON_JA_WORDS),
        'en': len(COMMON_EN_WORDS),
        'ngsl': len(NGSL_DICTIONARY),
        'ejdict': len(EJDICT_DICTIONARY),
        'total': len(COMMON_JA_WORDS) + len(COMMON_EN_WORDS) + len(NGSL_DICTIONARY) + len(EJDICT_DICTIONARY)
    }


def close_dictionary():
    """辞書リソースを解放（終了時に呼び出し）"""
    if USE_SQLITE and _db_initialized:
        try:
            from . import dictionary_db as db
            db.close_database()
        except Exception as e:
            print(f"辞書終了エラー: {e}")
