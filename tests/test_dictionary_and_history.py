# ClipboardTranslator v1.00 - Dictionary & History Test Script
# 辞書とSQLite履歴機能のテストスクリプト

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
    status = "✓ PASS" if success else "✗ FAIL"
    print(f"  {status}: {test_name}")
    if details:
        print(f"         {details}")


def test_database_initialization():
    """SQLiteデータベースの初期化テスト"""
    print_header("1. データベース初期化テスト")

    try:
        from core import dictionary_db as db

        data_dir = os.path.join(project_root, 'data')
        result = db.init_database(data_dir)
        print_result("データベース初期化", result, f"パス: {db.DB_PATH}")

        # 統計情報を取得
        stats = db.get_dictionary_stats()
        print_result("辞書統計取得", stats is not None, f"総単語数: {stats['total']}")

        if stats['sources']:
            print("  辞書ソース一覧:")
            for src in stats['sources']:
                print(f"    - {src['name']}: {src['word_count']}単語 (優先度: {src['priority']})")

        return True
    except Exception as e:
        print_result("データベース初期化", False, str(e))
        return False


def test_dictionary_lookup():
    """辞書検索テスト"""
    print_header("2. 辞書検索テスト")

    try:
        from core import dictionary_db as db

        # テスト単語リスト（存在が期待される単語）
        test_words = [
            ("hello", "こんにちは", "基本挨拶"),
            ("world", None, "一般名詞"),
            ("save", "保存", "コンピュータ用語"),
            ("open", None, "一般動詞"),
            ("file", None, "コンピュータ用語"),
            ("the", None, "NGSL基本語"),
            ("is", None, "NGSL基本語"),
            ("apple", None, "一般名詞"),
        ]

        found_count = 0
        for word, expected_meaning, category in test_words:
            result = db.lookup_word(word)
            if result:
                found_count += 1
                # 期待される意味がある場合は照合
                if expected_meaning:
                    match = expected_meaning in result
                    print_result(f"'{word}' ({category})", match, f"結果: {result[:50]}...")
                else:
                    print_result(f"'{word}' ({category})", True, f"結果: {result[:50]}...")
            else:
                print_result(f"'{word}' ({category})", False, "見つかりません")

        print(f"\n  検索結果: {found_count}/{len(test_words)} 単語が見つかりました")
        return found_count > 0

    except Exception as e:
        print_result("辞書検索", False, str(e))
        return False


def test_dictionary_sources():
    """辞書ソース別テスト"""
    print_header("3. 辞書ソース別テスト")

    try:
        from core import dictionary_db as db

        stats = db.get_dictionary_stats()

        # 各ソースのサンプル検索
        source_tests = {
            'custom_ja': ['保存', '開く', '閉じる'],
            'custom_en': ['save', 'open', 'close'],
            'ngsl': ['the', 'be', 'to', 'of', 'and'],
            'ejdict': ['abandon', 'ability', 'able'],
        }

        for source_name, test_words in source_tests.items():
            # ソースが存在するか確認
            source_exists = any(s['name'] == source_name for s in stats['sources'])
            if source_exists:
                found = 0
                for word in test_words:
                    result = db.lookup_word(word)
                    if result:
                        found += 1
                print_result(f"ソース '{source_name}'", found > 0, f"{found}/{len(test_words)} 単語発見")
            else:
                print_result(f"ソース '{source_name}'", False, "ソースが存在しません")

        return True

    except Exception as e:
        print_result("ソース別テスト", False, str(e))
        return False


def test_history_operations():
    """履歴操作テスト"""
    print_header("4. 履歴操作テスト")

    try:
        from core import dictionary_db as db

        # テスト用の履歴エントリを追加
        test_entries = [
            ("Hello, world!", "こんにちは、世界！", "EN", "JA", "normal"),
            ("テスト", "test", "JA", "EN", "normal"),
            ("Good morning", "おはようございます", "EN", "JA", "dictionary"),
        ]

        # 履歴追加テスト
        for original, translated, src, tgt, ttype in test_entries:
            db.add_history_entry(original, translated, src, tgt, ttype)
        print_result("履歴追加", True, f"{len(test_entries)}件追加")

        # 履歴取得テスト
        history = db.get_history(max_items=10)
        print_result("履歴取得", len(history) > 0, f"{len(history)}件取得")

        # 最新エントリを表示
        if history:
            latest = history[0]
            print(f"    最新: '{latest['original_text'][:20]}...' → '{latest['translated_text'][:20]}...'")

        # 履歴検索テスト
        search_result = db.search_history("Hello")
        print_result("履歴検索 ('Hello')", len(search_result) > 0, f"{len(search_result)}件ヒット")

        # キャッシュ検索テスト
        cached = db.find_cached_translation("Hello, world!", "EN")
        print_result("キャッシュ検索", cached is not None,
                    f"結果: {cached['translated_text'][:30] if cached else 'なし'}...")

        # フィルタリングテスト
        filtered = db.get_history(filter_type="dictionary")
        print_result("タイプフィルタリング", True, f"dictionary: {len(filtered)}件")

        # 履歴件数テスト
        count = db.get_history_count()
        print_result("履歴件数取得", count > 0, f"総件数: {count}")

        return True

    except Exception as e:
        print_result("履歴操作", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def test_legacy_fallback():
    """レガシーモードフォールバックテスト"""
    print_header("5. 辞書モジュール統合テスト")

    try:
        from core.dictionary import init_dictionaries, check_dictionary, get_dictionary_size

        data_dir = os.path.join(project_root, 'data')
        init_dictionaries(data_dir, use_sqlite=True)
        print_result("辞書初期化 (SQLiteモード)", True)

        # check_dictionary経由のテスト
        result_en = check_dictionary("hello", "EN")
        print_result("check_dictionary (EN→JA)", result_en is not None,
                    f"hello → {result_en[:30] if result_en else 'なし'}...")

        result_ja = check_dictionary("保存", "JA")
        print_result("check_dictionary (JA→EN)", result_ja is not None,
                    f"保存 → {result_ja if result_ja else 'なし'}")

        # サイズ取得
        size = get_dictionary_size()
        print_result("辞書サイズ取得", size['total'] > 0, f"総単語数: {size['total']}")

        return True

    except Exception as e:
        print_result("統合テスト", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def test_history_class():
    """TranslationHistoryクラステスト"""
    print_header("6. TranslationHistoryクラステスト")

    try:
        from core.history import TranslationHistory

        # インスタンス作成
        history = TranslationHistory()
        print_result("TranslationHistory初期化", True)

        # エントリ追加
        history.add_entry(
            "Integration test",
            "統合テスト",
            "EN", "JA", "normal"
        )
        print_result("add_entry", True)

        # 履歴取得
        entries = history.get_history(max_items=5)
        print_result("get_history", len(entries) > 0, f"{len(entries)}件取得")

        # 検索
        results = history.search_history("Integration")
        print_result("search_history", len(results) > 0, f"{len(results)}件ヒット")

        # キャッシュ検索
        cached = history.find_cached("Integration test", "EN")
        print_result("find_cached", cached is not None)

        return True

    except Exception as e:
        print_result("TranslationHistoryテスト", False, str(e))
        import traceback
        traceback.print_exc()
        return False


def run_all_tests():
    """全テストを実行"""
    print("\n" + "=" * 60)
    print(" ClipboardTranslator v1.00 - 辞書・履歴機能テスト")
    print(f" 実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    results = []

    # テスト実行
    results.append(("データベース初期化", test_database_initialization()))
    results.append(("辞書検索", test_dictionary_lookup()))
    results.append(("辞書ソース別", test_dictionary_sources()))
    results.append(("履歴操作", test_history_operations()))
    results.append(("辞書モジュール統合", test_legacy_fallback()))
    results.append(("TranslationHistoryクラス", test_history_class()))

    # 結果サマリー
    print_header("テスト結果サマリー")
    passed = sum(1 for _, r in results if r)
    total = len(results)

    for name, result in results:
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {status}: {name}")

    print(f"\n  合計: {passed}/{total} テスト成功")

    if passed == total:
        print("\n  🎉 全テスト成功！辞書と履歴システムは正常に動作しています。")
    else:
        print("\n  ⚠️  一部のテストが失敗しました。上記の詳細を確認してください。")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
