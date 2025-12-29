# ClipboardTranslator v1.00 - Smart Search Module
"""
高精度な履歴検索を提供するモジュール
- BM25アルゴリズム
- 形態素解析によるキーワード抽出
- 時間的重み付け
"""
import re
import math
from datetime import datetime
from collections import Counter

# 形態素解析ライブラリの遅延読み込み
_janome_available = None
_tokenizer = None


def _check_janome():
    """Janomeが利用可能かチェック"""
    global _janome_available, _tokenizer
    if _janome_available is None:
        try:
            from janome.tokenizer import Tokenizer
            _tokenizer = Tokenizer()
            _janome_available = True
        except ImportError:
            _janome_available = False
            print("Janome未インストール: 簡易トークナイザを使用します")
    return _janome_available


def tokenize_japanese(text):
    """
    日本語テキストをトークン化（名詞・動詞・形容詞を抽出）

    Parameters:
    text (str): 入力テキスト

    Returns:
    list: トークンのリスト
    """
    # 先に英単語を抽出（Janomeの有無に関わらず、日本語に隣接していてもOK）
    english_words = re.findall(r'[a-zA-Z]{3,}', text.lower())

    if _check_janome():
        tokens = list(english_words)  # 英単語を先に追加
        for token in _tokenizer.tokenize(text):
            # 名詞、動詞、形容詞のみ抽出
            pos = token.part_of_speech.split(',')[0]
            if pos in ('名詞', '動詞', '形容詞'):
                # 基本形があれば基本形を使用
                base = token.base_form if token.base_form != '*' else token.surface
                # 英単語は既に追加済みなのでスキップ
                if len(base) >= 2 and not re.match(r'^[a-zA-Z]+$', base):
                    tokens.append(base.lower())
        return tokens
    else:
        # Janomeがない場合は簡易トークナイザ
        return simple_tokenize(text)


def simple_tokenize(text):
    """
    簡易トークナイザ（Janomeなしで動作）

    Parameters:
    text (str): 入力テキスト

    Returns:
    list: トークンのリスト
    """
    tokens = []

    # 英単語を抽出（3文字以上、日本語に隣接していてもOK）
    english_words = re.findall(r'[a-zA-Z]{3,}', text.lower())
    tokens.extend(english_words)

    # カタカナ語を抽出（2文字以上）
    katakana = re.findall(r'[ァ-ヶー]{2,}', text)
    tokens.extend(katakana)

    # 漢字を含む単語を抽出（2文字以上）
    kanji = re.findall(r'[一-龥]{2,}', text)
    tokens.extend(kanji)

    # ひらがな連続（4文字以上、助詞などを除外）
    hiragana = re.findall(r'[ぁ-ん]{4,}', text)
    tokens.extend(hiragana)

    return tokens


class BM25Ranker:
    """
    BM25アルゴリズムによる文書ランキング

    BM25は検索精度の高いランキングアルゴリズムで、
    - 単語の出現頻度（TF）
    - 逆文書頻度（IDF）
    - 文書の長さの正規化
    を考慮してスコアを計算します。
    """

    def __init__(self, k1=1.5, b=0.75):
        """
        初期化

        Parameters:
        k1 (float): TFの飽和パラメータ（1.2-2.0が一般的）
        b (float): 文書長正規化パラメータ（0.75が標準）
        """
        self.k1 = k1
        self.b = b
        self.documents = []
        self.doc_lengths = []
        self.avg_doc_length = 0
        self.doc_freqs = Counter()  # 各単語が出現する文書数
        self.idf = {}
        self.doc_token_counts = []  # 各文書のトークン頻度

    def fit(self, documents):
        """
        文書コーパスでBM25を学習

        Parameters:
        documents (list): 文書リスト（各要素は辞書でoriginal_text, translated_textを含む）
        """
        self.documents = documents
        self.doc_token_counts = []
        self.doc_lengths = []

        # 各文書をトークン化
        for doc in documents:
            text = f"{doc.get('original_text', '')} {doc.get('translated_text', '')}"
            tokens = tokenize_japanese(text)
            token_counts = Counter(tokens)
            self.doc_token_counts.append(token_counts)
            self.doc_lengths.append(len(tokens))

            # 文書頻度を更新
            for token in set(tokens):
                self.doc_freqs[token] += 1

        # 平均文書長を計算
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)
        else:
            self.avg_doc_length = 1

        # IDFを計算
        n_docs = len(documents)
        for term, df in self.doc_freqs.items():
            # IDF = log((N - df + 0.5) / (df + 0.5) + 1)
            self.idf[term] = math.log((n_docs - df + 0.5) / (df + 0.5) + 1)

    def score(self, query_tokens, doc_index):
        """
        クエリと文書のBM25スコアを計算

        Parameters:
        query_tokens (list): クエリのトークンリスト
        doc_index (int): 文書インデックス

        Returns:
        float: BM25スコア
        """
        if doc_index >= len(self.doc_token_counts):
            return 0.0

        score = 0.0
        doc_length = self.doc_lengths[doc_index]
        token_counts = self.doc_token_counts[doc_index]

        for term in query_tokens:
            if term not in self.idf:
                continue

            tf = token_counts.get(term, 0)
            idf = self.idf[term]

            # BM25スコア計算
            # score = IDF * (tf * (k1 + 1)) / (tf + k1 * (1 - b + b * dl / avgdl))
            numerator = tf * (self.k1 + 1)
            denominator = tf + self.k1 * (1 - self.b + self.b * doc_length / self.avg_doc_length)

            if denominator > 0:
                score += idf * (numerator / denominator)

        return score

    def search(self, query, top_k=5):
        """
        クエリに最も関連する文書を検索

        Parameters:
        query (str): 検索クエリ
        top_k (int): 返す文書数

        Returns:
        list: (スコア, 文書インデックス, 文書)のタプルリスト
        """
        query_tokens = tokenize_japanese(query)
        if not query_tokens:
            return []

        # 全文書のスコアを計算
        scores = []
        for i in range(len(self.documents)):
            score = self.score(query_tokens, i)
            if score > 0:
                scores.append((score, i, self.documents[i]))

        # スコアでソート（降順）
        scores.sort(key=lambda x: x[0], reverse=True)

        return scores[:top_k]


def calculate_recency_weight(timestamp_str, decay_days=30):
    """
    時間的重み付けを計算（新しい履歴ほど高スコア）

    Parameters:
    timestamp_str (str): タイムスタンプ文字列 (YYYY-MM-DD HH:MM:SS)
    decay_days (int): 重みが半減するまでの日数

    Returns:
    float: 重み（0.0-1.0）
    """
    try:
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
        now = datetime.now()
        days_ago = (now - timestamp).days

        # 指数減衰: weight = e^(-days / decay_days)
        weight = math.exp(-days_ago / decay_days)
        return max(0.1, weight)  # 最小0.1を保証
    except (ValueError, TypeError):
        return 0.5  # パースできない場合はデフォルト値


class SmartHistorySearcher:
    """
    高精度な履歴検索クラス
    BM25 + 時間的重み付けを組み合わせた検索
    """

    def __init__(self, recency_weight=0.3, decay_days=30):
        """
        初期化

        Parameters:
        recency_weight (float): 時間的重みの影響度（0.0-1.0）
        decay_days (int): 重みが半減するまでの日数
        """
        self.bm25 = BM25Ranker()
        self.recency_weight = recency_weight
        self.decay_days = decay_days
        self.is_fitted = False

    def fit(self, history_entries):
        """
        履歴データで検索エンジンを学習

        Parameters:
        history_entries (list): 履歴エントリのリスト
        """
        if not history_entries:
            self.is_fitted = False
            return

        self.bm25.fit(history_entries)
        self.is_fitted = True

    def search(self, query, top_k=3):
        """
        クエリに最も関連する履歴を検索

        Parameters:
        query (str): 検索クエリ
        top_k (int): 返す結果数

        Returns:
        list: 関連する履歴エントリのリスト
        """
        if not self.is_fitted:
            return []

        # BM25で検索
        bm25_results = self.bm25.search(query, top_k=top_k * 2)  # 多めに取得

        if not bm25_results:
            return []

        # 時間的重み付けを適用
        weighted_results = []
        for bm25_score, idx, doc in bm25_results:
            timestamp = doc.get('timestamp', '')
            recency = calculate_recency_weight(timestamp, self.decay_days)

            # 最終スコア = BM25スコア * (1 - recency_weight) + 時間スコア * recency_weight
            final_score = bm25_score * (1 - self.recency_weight) + recency * self.recency_weight * bm25_score

            weighted_results.append((final_score, doc))

        # スコアでソート
        weighted_results.sort(key=lambda x: x[0], reverse=True)

        # 上位k件を返す
        return [doc for _, doc in weighted_results[:top_k]]


def extract_keywords(text, max_keywords=10):
    """
    テキストから重要なキーワードを抽出

    Parameters:
    text (str): 入力テキスト
    max_keywords (int): 最大キーワード数

    Returns:
    list: キーワードのリスト
    """
    tokens = tokenize_japanese(text)

    # 頻度でソート
    token_counts = Counter(tokens)
    top_tokens = token_counts.most_common(max_keywords)

    return [token for token, _ in top_tokens]
