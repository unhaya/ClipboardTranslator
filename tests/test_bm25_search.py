# ClipboardTranslator v1.00 - BM25 Search Test Script
# BM25検索・形態素解析・時間的重み付けのテストスクリプト

import os
import sys
import io

# Windows環境でのUnicodeサポート
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# プロジェクトルートをパスに追加
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from datetime import datetime


def print_header(title):
    """セクションヘッダーを表示"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_result(test_name, success, details=""):
    """テスト結果を表示"""
    status = "PASS" if success else "FAIL"
    print(f"  [{status}] {test_name}")
    if details:
        print(f"         {details}")


def test_simple_tokenize():
    """簡易トークナイザのテスト"""
    print_header("1. 簡易トークナイザテスト")

    try:
        from core.tutor.search import simple_tokenize

        test_cases = [
            # (入力, 期待される英単語, 説明)
            ("alleviate", ["alleviate"], "英単語のみ"),
            ("alleviateの意味", ["alleviate"], "日本語に隣接した英単語"),
            ("Hello World", ["hello", "world"], "複数英単語"),
            ("勉強している", [], "日本語のみ（漢字）"),
            ("テスト", [], "カタカナのみ（2文字以上）"),
            ("英語のstudyを頑張る", ["study"], "混在テキスト"),
        ]

        all_passed = True
        for text, expected_english, desc in test_cases:
            tokens = simple_tokenize(text)
            # 英単語のみチェック（日本語トークンは環境依存なので）
            english_tokens = [t for t in tokens if t.isascii()]
            passed = set(expected_english) <= set(english_tokens)
            print_result(f"'{text}' ({desc})", passed, f"トークン: {tokens}")
            if not passed:
                all_passed = False

        return all_passed

    except Exception as e:
        print_result("簡易トークナイザ", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def test_extract_keywords():
    """キーワード抽出テスト"""
    print_header("2. キーワード抽出テスト")

    try:
        from core.tutor.search import extract_keywords

        test_cases = [
            ("alleviateという単語の意味を教えて", ["alleviate"]),
            ("英語の勉強をしていてexacerbateがわからない", ["exacerbate"]),
            ("Hello and Goodbye", ["hello", "goodbye"]),
        ]

        all_passed = True
        for text, expected_words in test_cases:
            keywords = extract_keywords(text, max_keywords=10)
            # 期待される英単語がキーワードに含まれているか
            keywords_lower = [k.lower() for k in keywords]
            passed = all(w.lower() in keywords_lower for w in expected_words)
            print_result(f"'{text[:30]}...'", passed, f"キーワード: {keywords}")
            if not passed:
                all_passed = False

        return all_passed

    except Exception as e:
        print_result("キーワード抽出", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def test_bm25_ranker():
    """BM25ランキングテスト"""
    print_header("3. BM25ランキングテスト")

    try:
        from core.tutor.search import BM25Ranker

        # テスト用文書
        documents = [
            {'original_text': 'alleviate', 'translated_text': '和らげる、軽減する'},
            {'original_text': 'exacerbate', 'translated_text': '悪化させる'},
            {'original_text': 'mitigate', 'translated_text': '緩和する、軽減する'},
            {'original_text': 'aggravate', 'translated_text': '悪化させる、怒らせる'},
            {'original_text': 'ameliorate', 'translated_text': '改善する'},
        ]

        bm25 = BM25Ranker()
        bm25.fit(documents)
        print_result("BM25学習", True, f"{len(documents)}件の文書を学習")

        # 検索テスト1: 完全一致
        results1 = bm25.search("alleviate", top_k=3)
        passed1 = len(results1) > 0 and results1[0][2]['original_text'] == 'alleviate'
        print_result("検索 'alleviate'", passed1,
                    f"1位: {results1[0][2]['original_text'] if results1 else 'なし'}")

        # 検索テスト2: 意味での検索
        results2 = bm25.search("軽減する", top_k=3)
        passed2 = len(results2) > 0
        top_words = [r[2]['original_text'] for r in results2[:2]]
        # alleviate か mitigate が上位にくるはず
        passed2 = 'alleviate' in top_words or 'mitigate' in top_words
        print_result("検索 '軽減する'", passed2, f"上位: {top_words}")

        # 検索テスト3: 悪化
        results3 = bm25.search("悪化させる", top_k=3)
        passed3 = len(results3) > 0
        top_words3 = [r[2]['original_text'] for r in results3[:2]]
        # exacerbate か aggravate が上位にくるはず
        passed3 = 'exacerbate' in top_words3 or 'aggravate' in top_words3
        print_result("検索 '悪化させる'", passed3, f"上位: {top_words3}")

        return passed1 and passed2 and passed3

    except Exception as e:
        print_result("BM25ランキング", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def test_recency_weight():
    """時間的重み付けテスト"""
    print_header("4. 時間的重み付けテスト")

    try:
        from core.tutor.search import calculate_recency_weight

        # 今日
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        weight_today = calculate_recency_weight(today)
        passed1 = weight_today > 0.9
        print_result("今日の重み", passed1, f"weight={weight_today:.3f} (期待: >0.9)")

        # 30日前
        from datetime import timedelta
        days_30_ago = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        weight_30 = calculate_recency_weight(days_30_ago)
        passed2 = 0.3 < weight_30 < 0.5  # 約0.37になるはず
        print_result("30日前の重み", passed2, f"weight={weight_30:.3f} (期待: 0.3-0.5)")

        # 90日前
        days_90_ago = (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d %H:%M:%S')
        weight_90 = calculate_recency_weight(days_90_ago)
        passed3 = weight_90 < 0.2
        print_result("90日前の重み", passed3, f"weight={weight_90:.3f} (期待: <0.2)")

        # 重みの順序確認
        passed4 = weight_today > weight_30 > weight_90
        print_result("重みの順序", passed4, "今日 > 30日前 > 90日前")

        return passed1 and passed2 and passed3 and passed4

    except Exception as e:
        print_result("時間的重み付け", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def test_smart_history_searcher():
    """SmartHistorySearcher統合テスト"""
    print_header("5. SmartHistorySearcher統合テスト")

    try:
        from core.tutor.search import SmartHistorySearcher
        from datetime import timedelta

        # テスト用履歴データ（時間差あり）
        now = datetime.now()
        history = [
            {
                'original_text': 'alleviate',
                'translated_text': '和らげる、軽減する',
                'timestamp': now.strftime('%Y-%m-%d %H:%M:%S')  # 今日
            },
            {
                'original_text': 'mitigate',
                'translated_text': '緩和する、軽減する',
                'timestamp': (now - timedelta(days=7)).strftime('%Y-%m-%d %H:%M:%S')  # 1週間前
            },
            {
                'original_text': 'reduce',
                'translated_text': '減らす、軽減する',
                'timestamp': (now - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')  # 1ヶ月前
            },
        ]

        searcher = SmartHistorySearcher(recency_weight=0.3, decay_days=30)
        searcher.fit(history)
        print_result("Searcher初期化", True, f"{len(history)}件の履歴を学習")

        # 検索テスト: 「軽減する」で検索
        results = searcher.search("軽減する", top_k=3)
        passed1 = len(results) == 3
        print_result("検索 '軽減する'", passed1, f"{len(results)}件ヒット")

        # 順序確認: 新しいものが上位にくるか
        if results:
            result_words = [r['original_text'] for r in results]
            print(f"    順序: {result_words}")
            # alleviateが最も新しいので1位になるはず
            passed2 = result_words[0] == 'alleviate'
            print_result("時間的重み付けの効果", passed2,
                        f"1位: {result_words[0]} (期待: alleviate)")
        else:
            passed2 = False

        return passed1 and passed2

    except Exception as e:
        print_result("SmartHistorySearcher", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def test_tutor_chat_handler_integration():
    """TutorChatHandler統合テスト"""
    print_header("6. TutorChatHandler統合テスト")

    try:
        from core.tutor import TutorChatHandler
        from core.history import TranslationHistory

        # 履歴マネージャーを初期化
        history = TranslationHistory()

        # テスト用履歴を追加
        history.add_entry("alleviate", "和らげる、軽減する", "EN", "JA", "dictionary")
        history.add_entry("exacerbate", "悪化させる", "EN", "JA", "dictionary")
        print_result("テスト履歴追加", True, "2件追加")

        # TutorChatHandlerを初期化
        handler = TutorChatHandler(history_manager=history)
        print_result("TutorChatHandler初期化", True)

        # キーワード抽出テスト
        keywords = handler.extract_topics_from_message("alleviateの意味を教えて")
        passed1 = 'alleviate' in [k.lower() for k in keywords]
        print_result("キーワード抽出", passed1, f"キーワード: {keywords}")

        # 履歴検索テスト（タプル形式で返る: (results, metadata)）
        results, metadata = handler.search_relevant_history("軽減する", max_results=3)
        passed2 = len(results) > 0
        print_result("履歴検索", passed2, f"{len(results)}件ヒット")

        # メタデータテスト
        passed2a = 'count' in metadata and 'dates' in metadata
        print_result("検索メタデータ", passed2a, f"メタデータ: {metadata}")

        # コンテキスト構築テスト（タプル形式で返る: (context, metadata)）
        handler.add_to_history('user', 'alleviateってどういう意味？')
        context, context_metadata = handler.build_context('教えて', max_recent=1)
        passed3 = len(context) > 0
        print_result("コンテキスト構築", passed3, f"長さ: {len(context)}文字")

        return passed1 and passed2 and passed2a and passed3

    except Exception as e:
        print_result("TutorChatHandler統合", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def test_janome_availability():
    """Janome形態素解析の利用可否確認"""
    print_header("7. Janome形態素解析チェック")

    try:
        from core.tutor.search import _check_janome, tokenize_japanese

        janome_available = _check_janome()
        print_result("Janome利用可否", True,
                    f"{'利用可能' if janome_available else '未インストール（簡易トークナイザ使用）'}")

        # トークナイズテスト
        text = "英語の勉強は大切です"
        tokens = tokenize_japanese(text)
        print_result("日本語トークナイズ", len(tokens) > 0, f"トークン: {tokens}")

        return True  # Janomeの有無に関わらず成功

    except Exception as e:
        print_result("Janomeチェック", False, str(e))
        return False


def run_all_tests():
    """全テストを実行"""
    print("\n" + "=" * 60)
    print(" ClipboardTranslator v1.00 - BM25検索機能テスト")
    print(f" 実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = []

    # テスト実行
    results.append(("簡易トークナイザ", test_simple_tokenize()))
    results.append(("キーワード抽出", test_extract_keywords()))
    results.append(("BM25ランキング", test_bm25_ranker()))
    results.append(("時間的重み付け", test_recency_weight()))
    results.append(("SmartHistorySearcher", test_smart_history_searcher()))
    results.append(("TutorChatHandler統合", test_tutor_chat_handler_integration()))
    results.append(("Janome形態素解析", test_janome_availability()))

    # 結果サマリー
    print_header("テスト結果サマリー")
    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"  [{status}] {name}")

    print(f"\n  合計: {passed}/{total} テスト成功")

    if passed == total:
        print("\n  全テスト成功！BM25検索システムは正常に動作しています。")
    else:
        print("\n  一部のテストが失敗しました。上記の詳細を確認してください。")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
