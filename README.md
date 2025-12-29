# ClipTrans v1.00

クリップボードの単語を自動的に翻訳・辞書検索・音声出力するデスクトップアプリケーション

## 機能概要

- **翻訳機能**: DeepL APIを使用した高精度な翻訳
- **辞書検索機能**: Claude AIを使用した詳細な単語解説
- **音声出力機能**: テキスト読み上げ（TTS）
- **家庭教師モード**: Claude AIによるインタラクティブな学習サポート（RAG対応）
- **翻訳履歴**: 過去の翻訳結果の保存・検索（SQLite）
- **重複起動防止**: Windowsミューテックスによる単一インスタンス制限

## ディレクトリ構造

```
v1.00/
├── main.py                     # アプリケーションエントリーポイント
├── requirements.txt            # 依存パッケージ（Windows）
├── requirements_mac.txt        # 依存パッケージ（Mac）
├── README.md                   # このファイル
│
├── config/                     # 設定モジュール
│   ├── __init__.py
│   ├── constants.py            # 定数定義（API URL、デフォルト設定、メッセージ）
│   └── settings.py             # ConfigParser設定管理
│
├── core/                       # コア機能モジュール
│   ├── __init__.py
│   ├── translation.py          # DeepL/Claude API翻訳処理
│   ├── dictionary.py           # オフライン辞書
│   ├── dictionary_db.py        # SQLite辞書データベース
│   ├── language_detection.py   # 言語検出
│   ├── text_to_speech.py       # 音声出力（pygame使用）
│   ├── history.py              # 翻訳履歴管理
│   ├── network.py              # ネットワーク接続確認
│   └── tutor/                  # 家庭教師モード（RAG実装済み）
│       ├── __init__.py
│       ├── chat_handler.py     # チャット処理（履歴検索連携）
│       ├── search.py           # 高精度検索（BM25 + 時間的重み付け）★新規
│       ├── prompt.py           # プロンプト生成
│       ├── session.py          # 会話セッション管理
│       ├── state.py            # 状態管理
│       └── trigger.py          # トリガー検出
│
├── ui/                         # UIモジュール
│   ├── __init__.py
│   ├── main_window.py          # メインウィンドウ（tkinter）715行
│   ├── settings_dialog.py      # 設定ダイアログ
│   └── history_dialog.py       # 履歴ダイアログ
│
├── data/                       # データファイル
│   └── dictionary.db           # SQLite辞書データベース
│
├── icon/                       # アイコン
│   ├── DeepL.png
│   └── 翻訳.ico
│
├── tests/                      # テスト
│   ├── test_dictionary_and_history.py  # 辞書・履歴テスト
│   └── test_bm25_search.py             # BM25検索テスト★新規
│
└── utils/                      # ユーティリティ
    └── __init__.py
```

## ホットキー

| 機能 | デフォルトキー |
|------|---------------|
| 翻訳 | Ctrl + Alt + D |
| 辞書検索 | Ctrl + Alt + J |
| 音声出力 | Ctrl + Alt + T |

※設定画面から変更可能

## 家庭教師モード（RAG実装）

### ハイブリッド方式
コスト削減のため、以下のハイブリッド方式を採用：

1. **過去の話題キーワード**: ローカルで抽出（APIコストゼロ）
2. **翻訳履歴検索**: ユーザーの質問に関連する履歴を自動検索
3. **直近N件の会話**: 設定で指定した件数のみAPIに送信

### 高精度検索アルゴリズム（search.py）

履歴検索には以下のアルゴリズムを組み合わせて使用：

| アルゴリズム | 説明 |
|-------------|------|
| **BM25** | キーワードの重要度を考慮したランキング（TF-IDF改良版） |
| **形態素解析** | Janome使用時は名詞・動詞・形容詞を抽出（未インストール時は簡易トークナイザ） |
| **時間的重み付け** | 新しい履歴ほど高スコア（指数減衰、decay_days=30） |

```python
# スコア計算式
final_score = bm25_score * 0.7 + recency_score * 0.3
```

### 処理フロー
```
ユーザー入力
    ↓
キーワード抽出（形態素解析/簡易トークナイザ）
    ↓
BM25 + 時間的重み付けで履歴検索
    ↓
ステータスバーに検索情報表示（例: 「履歴3件を参照中 (12/27, 12/20)」）
    ↓
コンテキスト構築
    ↓
Claude APIに送信
    ↓
応答を表示・履歴に保存
```

### 検索コンテキスト表示
家庭教師モードでは、AIが何を参照しているかをステータスバーに表示：
- `履歴3件を参照中 (12/27, 12/20)` - 関連履歴が見つかった場合
- `履歴2件を参照中...` - 日付情報がない場合
- `考え中...` - 関連履歴がない場合

### オプション: Janomeインストール
形態素解析の精度を上げるには：
```bash
pip install janome
```

## Claude APIモデル（2025年12月時点）

```python
CLAUDE_MODELS = {
    'sonnet': 'claude-sonnet-4-5-20250929',   # 推奨: バランス型
    'haiku': 'claude-haiku-4-5-20251001',     # 高速・低コスト
    'opus': 'claude-opus-4-5-20251101',       # 最高性能・高コスト
}
```

## 設定項目

### 翻訳設定
- DeepL APIの有効/無効
- 翻訳文字数制限

### API設定
- DeepL APIキー
- Claude APIキー
- Claudeプロンプトテンプレート

### 家庭教師設定
- 家庭教師モードの有効/無効
- 使用モデル選択（Sonnet/Haiku/Opus）
- 会話コンテキスト保持数（3/5/10/15/20件）
- システムプロンプトのカスタマイズ

### 音声設定
- 音声出力の有効/無効
- 音量調整

### ショートカット設定
- 各機能のホットキーカスタマイズ

## コンパイル

PyInstallerを使用してEXEにコンパイル:

```bash
cd D:\OneDrive\python_cord\ClipboardTranslator\compile_file
pyinstaller ClipboardTranslator.spec --noconfirm
```

出力先: `compile_file/dist/ClipTrans/ClipTrans.exe`

## 重複起動防止

`main.py`でWindowsミューテックスを使用:

```python
MUTEX_NAME = "ClipboardTranslator_v1.00_SingleInstance"
```

2回目の起動時は警告ダイアログを表示して終了。

## 開発状況（2025年12月27日）

### 完了した機能
- [x] 基本翻訳機能（DeepL API）
- [x] 辞書検索機能（Claude API）
- [x] 音声出力機能
- [x] 翻訳履歴管理（SQLite）
- [x] 設定画面
- [x] ホットキーカスタマイズ
- [x] 家庭教師モード（ハイブリッドRAG実装）
- [x] 家庭教師設定タブ
- [x] 重複起動防止
- [x] チャットパネル（フッター固定表示）
- [x] 翻訳履歴検索連携（家庭教師モード）
- [x] モジュール分離（TutorChatHandler）
- [x] 高精度検索（BM25 + 形態素解析 + 時間的重み付け）
- [x] BM25検索テストスクリプト（7テスト全合格）
- [x] 検索コンテキスト表示（ステータスバーに参照履歴を表示）

### テスト実行方法
```bash
# 辞書・履歴テスト
python tests/test_dictionary_and_history.py

# BM25検索テスト
python tests/test_bm25_search.py
```

### モジュール行数管理
| モジュール | 行数 | 状況 |
|-----------|------|------|
| main_window.py | 908行 | ステータス表示機能追加 |
| settings_dialog.py | 382行 | OK |
| search.py | 331行 | BM25 + メタデータ返却 |
| chat_handler.py | 243行 | 検索情報コールバック追加 |
| history.py | 229行 | OK |
| translation.py | 155行 | OK |

### 今後の開発予定
- [ ] Janome形態素解析のオプション導入
- [ ] さらなるモジュール分離（500行目標）

## 依存パッケージ

主要パッケージ:
- `tkinter` - GUI
- `requests` - HTTP通信
- `pynput` - ホットキー監視
- `pyperclip` - クリップボード操作
- `pygame` - 音声出力
- `googletrans` - Google翻訳（フォールバック）

## 設定ファイル

設定はユーザーディレクトリに保存:
- Windows: `%APPDATA%\ClipboardTranslator\config.ini`

## ライセンス

Private use
