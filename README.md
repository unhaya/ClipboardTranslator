# 🌐 ClipTrans - AI搭載クリップボード翻訳アシスタント

<div align="center">

![Version](https://img.shields.io/badge/version-1.10-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20Mac-lightgrey.svg)
![License](https://img.shields.io/badge/license-Custom-orange.svg)

**コピーするだけで即座に翻訳・辞書検索・発音確認ができる、あなた専用のAI学習パートナー**

[✨ 特徴](#-特徴) • [🚀 クイックスタート](#-クイックスタート) • [📖 使い方](#-使い方) • [🎓 家庭教師モード](#-家庭教師モード) • [⚙️ 設定](#%EF%B8%8F-設定)

</div>

---

## 💡 こんな悩みはありませんか？

- 📚 **英語の論文やドキュメント**を読んでいて、分からない単語が出てくるたびに翻訳サイトを開くのが面倒...
- 🎮 **海外のゲームやソフト**を使っていて、いちいちコピペして翻訳するのが億劫...
- 📖 **英語学習中**で、単語の意味だけでなく語源や使い方まで知りたい...
- 🗣️ **発音も確認したい**けど、別のサイトを開くのが手間...

### ✅ ClipTransがすべて解決します！

テキストを選択して`Ctrl+C`でコピー → ホットキーを押すだけ。**たった2秒で翻訳完了**。

---

## ✨ 特徴

### 🚀 爆速翻訳
- **ホットキー一発**で即座に翻訳（デフォルト: `Ctrl+Alt+D`）
- DeepL APIによる**高精度な翻訳**
- 翻訳結果は自動でクリップボードにコピー

### 📚 AI辞書検索
- Claude AIによる**詳細な単語解説**
- 語源・接頭辞・接尾辞の分解で**記憶に残る学習**
- 類義語・対義語も一緒に学べる

### 🔊 音声読み上げ
- ネイティブの発音を**ワンタッチで確認**
- 英語学習のリスニング練習に最適

### 🎓 AI家庭教師モード（NEW!）
- あなた専用の**AI学習パートナー**
- 過去の学習履歴を記憶して**パーソナライズされた指導**
- BM25アルゴリズムによる**高精度な文脈理解**

### 📊 学習履歴管理
- すべての翻訳履歴を**自動保存**
- キーワード検索で過去の学習内容を**即座に復習**

---

## 🚀 クイックスタート

### 必要なもの
- Python 3.8以上
- DeepL APIキー（無料プランでOK）
- Claude APIキー（家庭教師モード使用時）

### インストール

```bash
# リポジトリをクローン
git clone https://github.com/unhaya/ClipboardTranslator.git
cd ClipboardTranslator

# 依存パッケージをインストール
pip install -r requirements.txt

# 起動
python main.py
```

### 初期設定
1. アプリ起動後、設定画面を開く
2. DeepL APIキーを入力
3. （オプション）Claude APIキーを入力
4. 設定を保存して完了！

---

## 📖 使い方

### 基本操作

| 機能 | ホットキー | 説明 |
|------|-----------|------|
| 翻訳 | `Ctrl+Alt+D` | クリップボードのテキストを翻訳 |
| 辞書検索 | `Ctrl+Alt+J` | 単語の詳細な解説を表示 |
| 音声出力 | `Ctrl+Alt+T` | テキストを読み上げ |

### 操作の流れ

```
1. 翻訳したいテキストを選択
2. Ctrl+C でコピー
3. Ctrl+Alt+D で翻訳！
   → 結果がウィンドウに表示される
```

### 辞書検索の例

「alleviate」を辞書検索すると：

```
【意味】
（苦痛・問題などを）軽減する、和らげる

【語源分解】
al- (強調) + levi- (軽い) + -ate (動詞化)
→ 「強く軽くする」= 軽減する

【類義語】
relieve, ease, mitigate

【対義語】
aggravate, worsen
```

---

## 🎓 家庭教師モード

### あなただけのAI学習パートナー

家庭教師モードは、ただのAIチャットではありません。
**あなたの学習履歴を記憶し、過去に学んだ内容を踏まえて指導してくれる**、まさに専属家庭教師です。

### 特徴

- **学習履歴の活用**: 過去に翻訳・辞書検索した単語を記憶
- **パーソナライズ**: あなたの弱点を把握した上でアドバイス
- **高精度検索**: BM25 + 形態素解析で関連履歴を自動検出
- **時間的重み付け**: 最近学んだ内容を優先的に参照

### 使用例

```
あなた: "前に調べた alleviateって覚えてる？"

AI家庭教師: "もちろん覚えてますよ！12/27に調べた単語ですね。
al-(強調) + levi-(軽い) + -ate(動詞化) で「軽減する」でしたね。
類義語の relieve と一緒に覚えると効果的ですよ！"
```

### 対応モデル

| モデル | 特徴 | おすすめ |
|--------|------|----------|
| Claude Sonnet 4.5 | バランス型 | ⭐ 推奨 |
| Claude Haiku 4.5 | 高速・低コスト | 日常使い |
| Claude Opus 4.5 | 最高性能 | 深い学習 |

---

## ⚙️ 設定

### 設定項目一覧

| カテゴリ | 項目 | 説明 |
|---------|------|------|
| 翻訳 | DeepL有効/無効 | DeepL APIの使用 |
| 翻訳 | 文字数制限 | 翻訳対象の最大文字数 |
| API | DeepL APIキー | DeepLの認証キー |
| API | Claude APIキー | Claude AIの認証キー |
| 音声 | 音声出力有効/無効 | TTS機能の使用 |
| 音声 | 音量 | 読み上げ音量（0.0〜1.0） |
| 家庭教師 | モデル選択 | 使用するClaudeモデル |
| 家庭教師 | 履歴保持数 | 参照する会話履歴の件数 |
| ショートカット | 各機能のホットキー | カスタマイズ可能 |

### 設定ファイルの場所

- Windows: `%APPDATA%\ClipboardTranslator\config.ini`

---

## 🛠️ 技術仕様

### アーキテクチャ

```
ClipTrans/
├── main.py                 # エントリーポイント
├── config/                 # 設定管理
├── core/                   # コア機能
│   ├── translation.py      # DeepL/Claude翻訳
│   ├── dictionary.py       # 辞書機能
│   ├── text_to_speech.py   # 音声出力
│   ├── history.py          # 履歴管理
│   └── tutor/              # 家庭教師モード
│       ├── chat_handler.py # チャット処理
│       └── search.py       # BM25検索
├── ui/                     # ユーザーインターフェース
│   ├── main_window.py      # メインウィンドウ
│   ├── settings_dialog.py  # 設定画面
│   └── history_dialog.py   # 履歴画面
└── data/                   # データ保存
    └── dictionary.db       # SQLiteデータベース
```

### 使用技術

- **GUI**: tkinter
- **翻訳API**: DeepL API
- **AI**: Claude API (Anthropic)
- **音声合成**: pygame + gTTS
- **データベース**: SQLite
- **検索**: BM25アルゴリズム + 形態素解析

---

## 📋 必要要件

### 必須
- Python 3.8以上
- インターネット接続

### 依存パッケージ

```
requests
pynput
pyperclip
pygame
googletrans==4.0.0-rc1
```

### オプション（推奨）

```
janome  # 形態素解析の精度向上
```

---

## 🤝 コントリビューション

バグ報告や機能リクエストは[Issues](https://github.com/unhaya/ClipboardTranslator/issues)へお願いします。

---

## 📜 ライセンス

**Copyright (c) 2025 unhaya. All rights reserved.**

このソフトウェアはオープンソースですが、著作権は放棄していません。

| 利用形態 | 許可 |
|---------|------|
| 個人利用 | ✅ 自由に使用可能 |
| 学習目的 | ✅ 自由に使用可能 |
| 改変・フォーク | ✅ 可能（著作権表示を維持すること） |
| 商用利用 | ⚠️ 要問い合わせ |

商用利用をご希望の場合は、[Issues](https://github.com/unhaya/ClipboardTranslator/issues) からお問い合わせください。

---

## 🙏 謝辞

- [DeepL](https://www.deepl.com/) - 高精度な翻訳API
- [Anthropic](https://www.anthropic.com/) - Claude AI

---

<div align="center">

**⭐ このプロジェクトが役に立ったら、Starをお願いします！ ⭐**

Made with ❤️ for language learners

</div>
