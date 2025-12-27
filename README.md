# ClipTrans v1.00

クリップボードの単語を自動的に翻訳・辞書検索・音声出力するデスクトップアプリケーション

## 機能概要

- **翻訳機能**: DeepL APIを使用した高精度な翻訳
- **辞書検索機能**: Claude AIを使用した詳細な単語解説
- **音声出力機能**: テキスト読み上げ（TTS）
- **家庭教師モード**: Claude AIによるインタラクティブな学習サポート
- **翻訳履歴**: 過去の翻訳結果の保存・検索
- **重複起動防止**: Windowsミューテックスによる単一インスタンス制限

## ディレクトリ構造

```
v1.00/
├── main.py                     # アプリケーションエントリーポイント
├── requirements.txt            # 依存パッケージ（Windows）
├── requirements_mac.txt        # 依存パッケージ（Mac）
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
│   └── tutor/                  # 家庭教師モード（RAG対応予定）
│       ├── __init__.py
│       ├── prompt.py           # プロンプト生成
│       ├── session.py          # 会話セッション管理
│       ├── state.py            # 状態管理
│       └── trigger.py          # トリガー検出
│
├── ui/                         # UIモジュール
│   ├── __init__.py
│   ├── main_window.py          # メインウィンドウ（tkinter）
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
│   └── test_dictionary_and_history.py
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

### 家庭教師設定（新規追加）
- 家庭教師モードの有効/無効
- 使用モデル選択（Sonnet/Haiku/Opus）
- システムプロンプトのカスタマイズ
- 会話コンテキスト保持数

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
- [x] 翻訳履歴管理
- [x] 設定画面
- [x] ホットキーカスタマイズ
- [x] 家庭教師モード（基本実装）
- [x] 家庭教師設定タブ
- [x] 重複起動防止
- [x] チャットパネル（フッター固定表示）

### 今後の開発予定
- [ ] RAG（Retrieval-Augmented Generation）の本格実装
- [ ] 学習履歴のベクトルDB保存
- [ ] 履歴を活用したパーソナライズ応答

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
