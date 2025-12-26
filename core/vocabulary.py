# ClipboardTranslator v1.00 - Vocabulary Manager Module
import os
import json
import random
import re
from datetime import datetime


def clean_word_text(text):
    """
    単語のテキストをクリーニングする関数
    - かっこ書きの説明文を削除
    - ハイフン以外の記号を削除
    - 前後の空白を削除
    """
    if not text:
        return ""

    # かっこ内の説明文を削除
    cleaned_text = re.sub(r'[\(（].*?[\)）]', '', text)

    # ハイフン以外の記号を削除
    pattern = r'[^\w\s\-\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]'
    cleaned_text = re.sub(pattern, '', cleaned_text, flags=re.UNICODE)

    # 連続する空白を1つにまとめる
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)

    return cleaned_text.strip()


class VocabularyManager:
    """単語帳を管理するクラス"""

    def __init__(self, app=None, vocab_file_path=None):
        """
        VocabularyManagerクラスの初期化

        Parameters:
        app: メインアプリケーションのインスタンス（オプション）
        vocab_file_path (str): 単語帳ファイルのパス。Noneの場合はデフォルトパスを使用
        """
        self.app = app

        if vocab_file_path is None:
            script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.vocab_file = os.path.join(script_dir, 'data', 'vocabulary.json')
        else:
            self.vocab_file = vocab_file_path

        self.vocabulary = {
            'words': [],
            'categories': ['基本', '重要', '難しい', 'ビジネス', 'IT', '医療', '法律']
        }

        self.test_results = []

        self.load_vocabulary()

    def load_vocabulary(self):
        """単語帳ファイルから単語データを読み込む"""
        try:
            if os.path.exists(self.vocab_file):
                with open(self.vocab_file, 'r', encoding='utf-8') as f:
                    self.vocabulary = json.load(f)
                    print(f"単語帳ファイルから{len(self.vocabulary['words'])}個の単語を読み込みました")
        except Exception as e:
            print(f"単語帳ファイルの読み込みに失敗しました: {e}")
            self.vocabulary = {
                'words': [],
                'categories': ['基本', '重要', '難しい', 'ビジネス', 'IT', '医療', '法律']
            }

    def save_vocabulary(self):
        """単語帳データをファイルに保存する"""
        try:
            vocab_dir = os.path.dirname(self.vocab_file)
            if not os.path.exists(vocab_dir):
                os.makedirs(vocab_dir)

            with open(self.vocab_file, 'w', encoding='utf-8') as f:
                json.dump(self.vocabulary, f, ensure_ascii=False, indent=2)

            print(f"単語帳ファイルに{len(self.vocabulary['words'])}個の単語を保存しました")
        except Exception as e:
            print(f"単語帳ファイルの保存に失敗しました: {e}")

    def add_word(self, word, meaning, source_lang, target_lang, example=None, note=None, category="基本"):
        """
        単語帳に単語を追加する

        Parameters:
        word (str): 単語
        meaning (str): 意味
        source_lang (str): 原文の言語コード
        target_lang (str): 翻訳先の言語コード
        example (str): 例文（オプション）
        note (str): メモ（オプション）
        category (str): カテゴリ
        """
        # 同じ単語が既に登録されていないかチェック
        for existing_word in self.vocabulary['words']:
            if existing_word['word'].lower() == word.lower() and existing_word['source_lang'] == source_lang:
                # 既存の単語を更新
                existing_word['meaning'] = meaning
                existing_word['example'] = example or existing_word.get('example', '')
                existing_word['note'] = note or existing_word.get('note', '')
                existing_word['category'] = category
                existing_word['updated_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.save_vocabulary()
                return

        new_word = {
            'word': word,
            'meaning': meaning,
            'source_lang': source_lang,
            'target_lang': target_lang,
            'example': example or '',
            'note': note or '',
            'category': category,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'test_count': 0,
            'correct_count': 0,
            'mastered': False
        }

        self.vocabulary['words'].append(new_word)
        self.save_vocabulary()

    def remove_word(self, word, source_lang=None):
        """単語を削除する"""
        self.vocabulary['words'] = [
            w for w in self.vocabulary['words']
            if not (w['word'].lower() == word.lower() and
                    (source_lang is None or w['source_lang'] == source_lang))
        ]
        self.save_vocabulary()

    def get_words(self, category=None, source_lang=None, mastered=None):
        """単語リストを取得"""
        words = self.vocabulary['words']

        if category:
            words = [w for w in words if w.get('category') == category]

        if source_lang:
            words = [w for w in words if w.get('source_lang') == source_lang]

        if mastered is not None:
            words = [w for w in words if w.get('mastered') == mastered]

        return words

    def get_random_words(self, count=10, category=None, source_lang=None):
        """ランダムに単語を取得（テスト用）"""
        words = self.get_words(category=category, source_lang=source_lang)
        if len(words) <= count:
            return words
        return random.sample(words, count)

    def update_test_result(self, word, source_lang, is_correct):
        """テスト結果を更新"""
        for w in self.vocabulary['words']:
            if w['word'].lower() == word.lower() and w['source_lang'] == source_lang:
                w['test_count'] = w.get('test_count', 0) + 1
                if is_correct:
                    w['correct_count'] = w.get('correct_count', 0) + 1

                # 正答率が80%以上かつ5回以上テストしていたら習得とみなす
                if w['test_count'] >= 5:
                    accuracy = w['correct_count'] / w['test_count']
                    w['mastered'] = accuracy >= 0.8

                self.save_vocabulary()
                return

    def get_statistics(self):
        """統計情報を取得"""
        words = self.vocabulary['words']
        total = len(words)
        mastered = len([w for w in words if w.get('mastered')])
        tested = len([w for w in words if w.get('test_count', 0) > 0])

        return {
            'total': total,
            'mastered': mastered,
            'tested': tested,
            'not_tested': total - tested
        }
