# ClipboardTranslator v1.00 - Dictionary Module
import os
import pickle
import csv

# 辞書データのグローバル変数
COMMON_JA_WORDS = {}
COMMON_EN_WORDS = {}
NGSL_DICTIONARY = {}


def init_dictionaries(data_dir):
    """辞書データを初期化"""
    global COMMON_JA_WORDS, COMMON_EN_WORDS, NGSL_DICTIONARY

    # dictionary_data.pyから基本辞書を読み込み
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


def check_dictionary(text, source_lang):
    """ローカル辞書に登録されている単語かチェックして、あれば対応する翻訳を返す"""
    text = text.strip().lower()

    if source_lang == 'JA' and text in COMMON_JA_WORDS:
        return COMMON_JA_WORDS[text]
    elif source_lang == 'EN':
        if text in COMMON_EN_WORDS:
            return COMMON_EN_WORDS[text]
        if text in NGSL_DICTIONARY:
            return NGSL_DICTIONARY[text]

    return None


def get_dictionary_size():
    """辞書のサイズを取得"""
    return {
        'ja': len(COMMON_JA_WORDS),
        'en': len(COMMON_EN_WORDS),
        'ngsl': len(NGSL_DICTIONARY),
        'total': len(COMMON_JA_WORDS) + len(COMMON_EN_WORDS) + len(NGSL_DICTIONARY)
    }
