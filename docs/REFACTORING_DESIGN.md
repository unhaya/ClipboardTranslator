# main_window.py リファクタリング設計書

## 1. 概要

### 1.1 目的
main_window.py（908行）を責務ごとに分割し、保守性・テスト容易性・拡張性を向上させる。

### 1.2 現状の問題点

| 問題 | 行数 | 詳細 |
|------|------|------|
| 単一ファイルに複数責務が混在 | 908行 | UI、ビジネスロジック、状態管理が密結合 |
| 翻訳処理の重複 | 約150行 | `perform_translation()` と `perform_dictionary_translation()` が類似 |
| ホットキー管理がUIに埋め込み | 約80行 | 設定変更時の再起動ロジックが分散 |
| チャットパネルがメインクラスに内包 | 約100行 | UIコンポーネントとして独立すべき |
| 初期化処理が長大 | 約120行 | `__init__` が肥大化 |

### 1.3 目標
- 各ファイルを **300行以下** に抑える
- 責務の明確な分離（単一責任の原則）
- 依存関係の明確化
- テスト容易性の向上

### 1.4 リファクタリング方針：フォールバックなし

**重要**: このリファクタリングは「フォールバックなし」で実施する。

```
❌ やらないこと
- 旧コードを「念のため」残す
- try-except で旧ロジックにフォールバック
- 新旧どちらも動く「移行期間」を設ける
- 「あとで消す」コメント付きの旧コード

✅ やること
- 旧コードは即座に削除
- 新モジュールが動かなければアプリが落ちる（それでいい）
- 各Phaseで完全に動作確認してから次へ
- 壊れたら git revert で戻す
```

**理由**:
- フォールバックを残すと、いつまでも旧ロジックが使われ続ける
- 「動いているから」と新コードのバグに気づかない
- 技術的負債が増える一方になる

---

## 2. 新ディレクトリ構造

```
ui/
├── __init__.py
├── main_window.py           # 300行以下：UIレイアウト・イベントバインディングのみ
├── app_state.py             # 100行以下：アプリケーション状態管理
│
├── components/              # UIコンポーネント（独立したウィジェット）
│   ├── __init__.py
│   ├── text_display.py      # 150行以下：テキスト表示エリア
│   ├── chat_panel.py        # 150行以下：チャットパネル
│   └── status_bar.py        # 50行以下：ステータスバー
│
├── controllers/             # ビジネスロジック（UIから分離）
│   ├── __init__.py
│   ├── translation_controller.py  # 200行以下：翻訳処理
│   ├── dictionary_controller.py   # 100行以下：辞書検索処理
│   ├── speech_controller.py       # 80行以下：音声出力処理
│   └── tutor_controller.py        # 100行以下：家庭教師処理
│
├── services/                # 外部サービス・ユーティリティ
│   ├── __init__.py
│   ├── hotkey_service.py    # 100行以下：ホットキー管理
│   ├── clipboard_service.py # 50行以下：クリップボード操作
│   └── window_service.py    # 80行以下：ウィンドウ位置管理
│
├── settings_dialog.py       # 既存（変更なし）
└── history_dialog.py        # 既存（変更なし）
```

---

## 3. モジュール詳細設計

### 3.1 main_window.py（リファクタリング後）

**責務**: UIレイアウト構築、イベントバインディング、コントローラー/サービスの統合

```python
# main_window.py - 概要設計
"""
TranslationApp クラス
- __init__: 初期化（サービス・コントローラーのインスタンス化、UIレイアウト構築）
- UIレイアウトメソッド: create_menu(), _setup_layout()
- イベントハンドラ: on_closing()
- コントローラーへの委譲: 翻訳・辞書・音声・家庭教師処理
"""

class TranslationApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # 1. 状態管理の初期化
        self.state = AppState()

        # 2. サービスの初期化
        self.hotkey_service = HotkeyService(self._on_hotkey_triggered)
        self.clipboard_service = ClipboardService()
        self.window_service = WindowService(self)

        # 3. コントローラーの初期化
        self.translation_ctrl = TranslationController(self.state, self.clipboard_service)
        self.dictionary_ctrl = DictionaryController(self.state, self.clipboard_service)
        self.speech_ctrl = SpeechController(self.state)
        self.tutor_ctrl = TutorController(self.state)

        # 4. UIコンポーネントの初期化
        self.status_bar = StatusBar(self)
        self.text_display = TextDisplay(self)
        self.chat_panel = ChatPanel(self, on_send=self._on_chat_send)

        # 5. レイアウト構築
        self._setup_layout()
        self.create_menu()

        # 6. ホットキー開始
        self.hotkey_service.start()
```

**行数目標**: 250-300行

---

### 3.2 app_state.py

**責務**: アプリケーションの共有状態を管理

```python
# app_state.py - 概要設計
"""
AppState クラス
- 設定値の読み込み・キャッシュ
- 辞書・履歴インスタンスの保持
- 音声ハンドラーの保持
- 状態変更の通知（オブザーバーパターン）
"""

from dataclasses import dataclass, field
from typing import Callable, List, Optional
from core.history import TranslationHistory
from core.text_to_speech import TextToSpeechHandler

@dataclass
class AppState:
    """アプリケーション状態を一元管理"""

    # 初期化済みフラグ
    initialized: bool = False

    # コアオブジェクト（遅延初期化）
    history: Optional[TranslationHistory] = None
    speech_handler: Optional[TextToSpeechHandler] = None
    dictionary_size: int = 0

    # 状態変更リスナー
    _listeners: List[Callable] = field(default_factory=list)

    def initialize(self, app_root):
        """状態を初期化"""
        self._init_dictionary()
        self._init_history(app_root)
        self._init_speech_handler()
        self.initialized = True

    def add_listener(self, callback: Callable):
        """状態変更リスナーを追加"""
        self._listeners.append(callback)

    def notify(self, event: str, data=None):
        """リスナーに通知"""
        for listener in self._listeners:
            listener(event, data)
```

**行数目標**: 80-100行

---

### 3.3 components/text_display.py

**責務**: テキスト表示エリアのウィジェット管理

```python
# text_display.py - 概要設計
"""
TextDisplay クラス
- テキストエリアの作成・設定
- タグ設定（色分け）
- ログメッセージ表示
- フォントサイズ変更
- 右クリックメニュー
"""

class TextDisplay(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
        self._setup_tags()
        self._setup_bindings()

    def log_message(self, message: str, tag: str = None):
        """メッセージを表示"""
        pass

    def log_tutor_message(self, message: str, is_user: bool):
        """家庭教師メッセージを表示"""
        pass

    def clear(self):
        """テキストをクリア"""
        pass

    def change_font_size(self, delta: int):
        """フォントサイズを変更"""
        pass
```

**行数目標**: 120-150行

---

### 3.4 components/chat_panel.py

**責務**: チャットパネルのウィジェット管理

```python
# chat_panel.py - 概要設計
"""
ChatPanel クラス
- トグルボタン
- 入力エリア
- 送信ボタン
- ヒントラベル
- 表示/非表示切り替え
"""

class ChatPanel(tk.Frame):
    def __init__(self, parent, on_send: Callable[[str], None], **kwargs):
        super().__init__(parent, **kwargs)
        self.on_send = on_send
        self._visible = False
        self._create_widgets()

    def toggle(self):
        """表示/非表示を切り替え"""
        pass

    def get_message(self) -> str:
        """入力メッセージを取得"""
        pass

    def clear_input(self):
        """入力をクリア"""
        pass

    def focus_input(self):
        """入力欄にフォーカス"""
        pass
```

**行数目標**: 100-150行

---

### 3.5 components/status_bar.py

**責務**: ステータスバーの管理

```python
# status_bar.py - 概要設計
"""
StatusBar クラス
- ステータスメッセージ表示
- 自動リセット機能
"""

class StatusBar(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self._create_widgets()
        self._reset_job = None

    def update(self, message: str, duration: int = 3000):
        """ステータスを更新（duration ms後にリセット）"""
        pass

    def set_permanent(self, message: str):
        """永続的なステータスを設定"""
        pass
```

**行数目標**: 40-50行

---

### 3.6 controllers/translation_controller.py

**責務**: 翻訳処理のビジネスロジック

```python
# translation_controller.py - 概要設計
"""
TranslationController クラス
- 翻訳処理の実行
- キャッシュ確認
- 言語検出
- 翻訳API呼び出し
- 履歴保存
"""

from typing import Callable, Optional
from dataclasses import dataclass

@dataclass
class TranslationResult:
    """翻訳結果"""
    success: bool
    original_text: str
    translated_text: Optional[str] = None
    source_lang: Optional[str] = None
    target_lang: Optional[str] = None
    from_cache: bool = False
    error_message: Optional[str] = None

class TranslationController:
    def __init__(self, state: AppState, clipboard: ClipboardService):
        self.state = state
        self.clipboard = clipboard

    def translate(
        self,
        on_success: Callable[[TranslationResult], None],
        on_error: Callable[[str], None],
        on_status: Callable[[str], None]
    ):
        """翻訳を実行（非同期）"""
        pass

    def _perform_translation(self, text: str) -> TranslationResult:
        """翻訳処理の実体"""
        pass

    def _check_cache(self, text: str, source_lang: str) -> Optional[str]:
        """キャッシュを確認"""
        pass
```

**行数目標**: 150-200行

---

### 3.7 controllers/dictionary_controller.py

**責務**: 辞書検索処理

```python
# dictionary_controller.py - 概要設計
"""
DictionaryController クラス
- 辞書検索処理
- ローカル辞書検索
- Claude API検索
- 結果の統合
"""

class DictionaryController:
    def __init__(self, state: AppState, clipboard: ClipboardService):
        self.state = state
        self.clipboard = clipboard

    def lookup(
        self,
        on_success: Callable,
        on_error: Callable,
        on_status: Callable
    ):
        """辞書検索を実行（非同期）"""
        pass
```

**行数目標**: 80-100行

---

### 3.8 controllers/speech_controller.py

**責務**: 音声出力処理

```python
# speech_controller.py - 概要設計
"""
SpeechController クラス
- 音声出力処理
- 音量制御
"""

class SpeechController:
    def __init__(self, state: AppState):
        self.state = state

    def speak(
        self,
        text: str,
        on_success: Callable,
        on_error: Callable,
        on_status: Callable
    ):
        """音声出力を実行"""
        pass
```

**行数目標**: 60-80行

---

### 3.9 controllers/tutor_controller.py

**責務**: 家庭教師モードの処理（TutorChatHandlerのラッパー）

```python
# tutor_controller.py - 概要設計
"""
TutorController クラス
- TutorChatHandlerへの委譲
- UI向けコールバック管理
"""

class TutorController:
    def __init__(self, state: AppState):
        self.state = state
        self.handler = TutorChatHandler(history_manager=state.history)

    def process_message(
        self,
        message: str,
        on_success: Callable,
        on_error: Callable,
        on_search_info: Callable
    ):
        """メッセージを処理"""
        self.handler.process_message(
            message,
            on_success=on_success,
            on_error=on_error,
            on_search_info=on_search_info
        )
```

**行数目標**: 60-100行

---

### 3.10 services/hotkey_service.py

**責務**: グローバルホットキーの管理

```python
# hotkey_service.py - 概要設計
"""
HotkeyService クラス
- ホットキーの登録・解除
- 設定からの読み込み
- リスナーの開始・停止
- 再起動機能
"""

from enum import Enum
from typing import Callable, Dict
from pynput import keyboard

class HotkeyAction(Enum):
    TRANSLATE = "translate"
    DICTIONARY = "dictionary"
    SPEECH = "speech"

class HotkeyService:
    def __init__(self, on_triggered: Callable[[HotkeyAction], None]):
        self.on_triggered = on_triggered
        self._listener = None
        self._hotkeys: Dict[str, HotkeyAction] = {}

    def start(self):
        """ホットキー監視を開始"""
        self._load_hotkeys_from_config()
        self._start_listener()

    def stop(self):
        """ホットキー監視を停止"""
        pass

    def restart(self):
        """ホットキー監視を再起動"""
        self.stop()
        self.start()

    def _load_hotkeys_from_config(self):
        """設定からホットキーを読み込み"""
        pass

    def _build_hotkey_string(self, key: str, ctrl: bool, alt: bool, shift: bool) -> str:
        """pynput用のホットキー文字列を構築"""
        pass
```

**行数目標**: 80-100行

---

### 3.11 services/clipboard_service.py

**責務**: クリップボード操作のラッパー

```python
# clipboard_service.py - 概要設計
"""
ClipboardService クラス
- クリップボード読み取り
- クリップボード書き込み
- スレッドセーフなロック管理
"""

import threading
import pyperclip

class ClipboardService:
    def __init__(self):
        self._lock = threading.Lock()

    def get_text(self) -> str:
        """クリップボードからテキストを取得"""
        with self._lock:
            return pyperclip.paste()

    def set_text(self, text: str):
        """クリップボードにテキストを設定"""
        with self._lock:
            pyperclip.copy(text)
```

**行数目標**: 30-50行

---

### 3.12 services/window_service.py

**責務**: ウィンドウ位置の保存・復元

```python
# window_service.py - 概要設計
"""
WindowService クラス
- ウィンドウ位置の保存
- ウィンドウ位置の復元
- 画面外チェック
"""

class WindowService:
    def __init__(self, window: tk.Tk):
        self.window = window

    def save_position(self):
        """ウィンドウ位置を保存"""
        pass

    def load_position(self) -> bool:
        """ウィンドウ位置を復元"""
        pass

    def _ensure_on_screen(self, x: int, y: int, width: int, height: int):
        """画面内に収まるよう調整"""
        pass
```

**行数目標**: 60-80行

---

## 4. 依存関係図

```
                    ┌─────────────────────────────────────────┐
                    │              main_window.py              │
                    │           (TranslationApp)               │
                    └────────────────────┬────────────────────┘
                                         │
         ┌───────────────┬───────────────┼───────────────┬───────────────┐
         │               │               │               │               │
         ▼               ▼               ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  AppState   │ │ TextDisplay │ │  ChatPanel  │ │  StatusBar  │ │   Services  │
│             │ │             │ │             │ │             │ │             │
│ - history   │ │ - log_msg() │ │ - toggle()  │ │ - update()  │ │ - Hotkey    │
│ - speech    │ │ - clear()   │ │ - on_send   │ │             │ │ - Clipboard │
│ - dict_size │ │             │ │             │ │             │ │ - Window    │
└──────┬──────┘ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘
       │
       │ 参照
       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Controllers                                     │
│  ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐             │
│  │TranslationCtrl   │ │ DictionaryCtrl   │ │  SpeechCtrl      │             │
│  │                  │ │                  │ │                  │             │
│  │- translate()     │ │- lookup()        │ │- speak()         │             │
│  └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘             │
│           │                    │                    │                       │
│           └────────────────────┴────────────────────┘                       │
│                                │                                             │
│                                ▼                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                         Core Layer                                    │   │
│  │   translation.py  │  history.py  │  dictionary.py  │  tutor/         │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. 通信パターン

### 5.1 コールバックベースの非同期処理

```python
# 例: 翻訳処理のフロー

# main_window.py
def _on_translate_hotkey(self):
    self.status_bar.update("翻訳中...")
    self.translation_ctrl.translate(
        on_success=self._on_translation_success,
        on_error=self._on_translation_error,
        on_status=self.status_bar.update
    )

def _on_translation_success(self, result: TranslationResult):
    self.text_display.log_message(f"【入力】{result.original_text}")
    self.text_display.log_message(f"【翻訳結果】{result.translated_text}")
    self.status_bar.update("翻訳完了")

def _on_translation_error(self, error_msg: str):
    self.text_display.log_message(error_msg, tag='error')
    self.status_bar.update("エラーが発生しました")
```

### 5.2 状態変更の通知（オブザーバーパターン）

```python
# app_state.py
class AppState:
    def notify(self, event: str, data=None):
        for listener in self._listeners:
            listener(event, data)

# main_window.py
def __init__(self):
    self.state.add_listener(self._on_state_change)

def _on_state_change(self, event: str, data):
    if event == 'history_updated':
        # 必要に応じてUIを更新
        pass
```

---

## 6. 移行計画（フォールバックなし）

### 移行の鉄則

```
各Phaseの作業手順:
1. 新モジュールを作成
2. main_window.py の該当コードを【削除】（コメントアウトではない）
3. 新モジュールをimportして使用
4. 動作確認（失敗したらその場で修正、git revert も可）
5. コミット
6. 次のPhaseへ
```

**絶対にやらないこと**:
- `# OLD: ` コメントで旧コードを残す
- `if USE_NEW_MODULE:` のような分岐
- `except: fallback_to_old()` のようなフォールバック

---

### Phase 1: 準備
**目的**: ディレクトリ構造の準備

```bash
# 作成するディレクトリ
ui/components/
ui/controllers/
ui/services/
```

**作業内容**:
1. ディレクトリ作成
2. 各ディレクトリに `__init__.py` 作成
3. コミット: `refactor: create directory structure for ui modules`

**確認**: アプリが正常起動すること

---

### Phase 2: Services層の抽出
**目的**: 外部サービスとの連携を分離

#### Phase 2-1: ClipboardService
**作成**: `ui/services/clipboard_service.py`

**移行元** (main_window.py):
- L26-27: `clipboard_lock` 定義
- L600-601, L626-627, L636-637, L650-651, L668-669, L711-712, L762-763: `with clipboard_lock:` ブロック

**作業**:
1. `clipboard_service.py` を作成
2. main_window.py から `clipboard_lock` 定義を【削除】
3. main_window.py から `pyperclip` の直接使用を【削除】
4. `ClipboardService` をインスタンス化して使用
5. 動作確認: 翻訳ホットキーでクリップボード読み書きできること
6. コミット: `refactor: extract ClipboardService`

#### Phase 2-2: WindowService
**作成**: `ui/services/window_service.py`

**移行元** (main_window.py):
- L857-879: `save_window_position()`
- L880-916: `load_window_position()`

**作業**:
1. `window_service.py` を作成
2. main_window.py から上記メソッドを【削除】
3. `WindowService` をインスタンス化して使用
4. 動作確認: 終了時に位置保存、起動時に位置復元
5. コミット: `refactor: extract WindowService`

#### Phase 2-3: HotkeyService
**作成**: `ui/services/hotkey_service.py`

**移行元** (main_window.py):
- L523-534: `_build_hotkey_string()`
- L536-571: `hotkey_listener()`
- L573-594: 各 `*_hotkey_callback()`, `restart_hotkey_listener()`

**作業**:
1. `hotkey_service.py` を作成
2. main_window.py から上記メソッドを【削除】
3. `HotkeyService` をインスタンス化、コールバックを接続
4. 動作確認: 全ホットキー（翻訳・辞書・音声）が動作すること
5. コミット: `refactor: extract HotkeyService`

---

### Phase 3: Components層の抽出
**目的**: UIウィジェットを独立コンポーネントに

#### Phase 3-1: StatusBar
**作成**: `ui/components/status_bar.py`

**移行元** (main_window.py):
- L65-66: `status_label` 作成
- L428-437: `update_status()`

**作業**:
1. `status_bar.py` を作成
2. main_window.py から `status_label` 関連を【削除】
3. `StatusBar` コンポーネントをインスタンス化
4. 動作確認: ステータスメッセージが表示されること
5. コミット: `refactor: extract StatusBar component`

#### Phase 3-2: TextDisplay
**作成**: `ui/components/text_display.py`

**移行元** (main_window.py):
- L74-104: `text_area` 作成、タグ設定
- L388-397: コンテキストメニュー関連
- L399-426: `copy_selected_text()`, `select_all_text()`, `clear_text()`
- L448-482: `change_font_size()`
- L484-521: `log_message()`

**作業**:
1. `text_display.py` を作成
2. main_window.py から上記を【削除】
3. `TextDisplay` コンポーネントをインスタンス化
4. 動作確認: テキスト表示、コピー、フォントサイズ変更
5. コミット: `refactor: extract TextDisplay component`

#### Phase 3-3: ChatPanel
**作成**: `ui/components/chat_panel.py`

**移行元** (main_window.py):
- L226-312: `create_chat_panel()`, `toggle_chat_panel()`
- L314-321: `on_chat_enter()`, `on_chat_newline()`
- L323-337: `send_chat_message()`
- L339-351: `log_tutor_message()`

**作業**:
1. `chat_panel.py` を作成
2. main_window.py から上記を【削除】
3. `ChatPanel` コンポーネントをインスタンス化
4. 動作確認: チャットパネル開閉、メッセージ送信
5. コミット: `refactor: extract ChatPanel component`

---

### Phase 4: AppState の導入
**目的**: 状態管理を一元化

**作成**: `ui/app_state.py`

**移行元** (main_window.py):
- L42-44: `dictionary_size` 等の状態変数
- L118-135: `init_dictionary()`
- L137-140: `init_history()`
- L142-152: `init_speech_handler()`

**作業**:
1. `app_state.py` を作成
2. main_window.py から上記を【削除】
3. `AppState` をインスタンス化、`self.state` として保持
4. 各コンポーネント/コントローラーは `state` 経由でアクセス
5. 動作確認: 全機能が動作すること
6. コミット: `refactor: introduce AppState for centralized state management`

---

### Phase 5: Controllers層の抽出
**目的**: ビジネスロジックをUIから分離

#### Phase 5-1: TranslationController
**作成**: `ui/controllers/translation_controller.py`

**移行元** (main_window.py):
- L596-662: `perform_translation()`

**作業**:
1. `translation_controller.py` を作成
2. main_window.py から `perform_translation()` を【削除】
3. `TranslationController` をインスタンス化
4. ホットキーコールバックから `translation_ctrl.translate()` を呼び出し
5. 動作確認: Ctrl+Alt+D で翻訳が動作
6. コミット: `refactor: extract TranslationController`

#### Phase 5-2: DictionaryController
**作成**: `ui/controllers/dictionary_controller.py`

**移行元** (main_window.py):
- L664-747: `perform_dictionary_translation()`

**作業**:
1. `dictionary_controller.py` を作成
2. main_window.py から `perform_dictionary_translation()` を【削除】
3. `DictionaryController` をインスタンス化
4. 動作確認: Ctrl+Alt+J で辞書検索が動作
5. コミット: `refactor: extract DictionaryController`

#### Phase 5-3: SpeechController
**作成**: `ui/controllers/speech_controller.py`

**移行元** (main_window.py):
- L749-790: `perform_speech()`
- L439-446: `update_speech_status()`, `handle_speech_error()`

**作業**:
1. `speech_controller.py` を作成
2. main_window.py から上記を【削除】
3. `SpeechController` をインスタンス化
4. 動作確認: Ctrl+Alt+T で音声出力が動作
5. コミット: `refactor: extract SpeechController`

#### Phase 5-4: TutorController
**作成**: `ui/controllers/tutor_controller.py`

**移行元** (main_window.py):
- L353-386: `process_tutor_message()`
- L106-107: `TutorChatHandler` 初期化

**作業**:
1. `tutor_controller.py` を作成
2. main_window.py から上記を【削除】
3. `TutorController` をインスタンス化
4. 動作確認: チャットパネルから質問が動作
5. コミット: `refactor: extract TutorController`

---

### Phase 6: 最終調整
**目的**: クリーンアップと検証

**作業**:
1. main_window.py の不要な import を削除
2. main_window.py が300行以下であることを確認
3. 全機能の動作確認チェックリスト実行
4. README.md / ARCHITECTURE.md 更新
5. コミット: `refactor: complete main_window.py refactoring`

---

### 動作確認チェックリスト

各Phaseの完了時に実施:

```
[ ] アプリが正常起動する
[ ] Ctrl+Alt+D: 翻訳が動作する
[ ] Ctrl+Alt+J: 辞書検索が動作する
[ ] Ctrl+Alt+T: 音声出力が動作する
[ ] チャットパネル: 開閉が動作する
[ ] チャットパネル: メッセージ送信が動作する
[ ] 設定画面: 開閉が動作する
[ ] 設定保存: ホットキー変更が反映される
[ ] 終了時: ウィンドウ位置が保存される
[ ] 起動時: ウィンドウ位置が復元される
[ ] Ctrl+ホイール: フォントサイズ変更が動作する
[ ] 右クリック: コンテキストメニューが動作する
```

---

## 7. リスクと対策

| リスク | 対策 |
|--------|------|
| 移行中の機能破損 | 各Phaseで動作確認、壊れたら即 git revert |
| 循環参照の発生 | 依存関係図を厳守、インターフェース経由でやり取り |
| パフォーマンス低下 | コールバックの過剰なネストを避ける |
| グローバル config への依存 | AppState 経由でアクセスするよう統一 |
| フォールバック誘惑 | 【禁止】旧コードは即削除、残さない |

### フォールバック禁止の具体例

```python
# ❌ これは絶対にやらない
class TranslationApp:
    def perform_translation(self):
        try:
            self.translation_ctrl.translate(...)
        except:
            # フォールバック: 旧ロジック
            self._old_perform_translation()  # ← 禁止

    def _old_perform_translation(self):
        # 旧コード（念のため残しておく）  # ← 禁止
        pass

# ❌ これも禁止
USE_NEW_CLIPBOARD_SERVICE = True  # フラグで切り替え

if USE_NEW_CLIPBOARD_SERVICE:
    text = self.clipboard.get_text()
else:
    text = pyperclip.paste()  # ← 旧ロジックが残っている

# ✅ 正しい実装
class TranslationApp:
    def __init__(self):
        self.clipboard = ClipboardService()  # 新モジュールのみ
        # pyperclip の import すら削除

    def _on_translate(self):
        text = self.clipboard.get_text()  # これしかない
        self.translation_ctrl.translate(text, ...)  # これしかない
```

---

## 8. テスト方針

### 8.1 ユニットテスト対象
- `ClipboardService`: モック使用でテスト
- `HotkeyService`: 設定読み込みロジックをテスト
- `TranslationController`: API モック使用でテスト
- `BM25Ranker` (既存): 現状維持

### 8.2 統合テスト
- 翻訳フロー全体（ホットキー → 翻訳 → 表示）
- 辞書検索フロー全体
- 家庭教師モードフロー全体

### 8.3 手動テスト
- UIの表示確認
- ホットキーの動作確認
- 設定変更の即時反映確認

---

## 9. 行数サマリー（目標）

| ファイル | 目標行数 | 責務 |
|----------|----------|------|
| main_window.py | 250-300 | UIレイアウト・統合 |
| app_state.py | 80-100 | 状態管理 |
| text_display.py | 120-150 | テキスト表示 |
| chat_panel.py | 100-150 | チャットパネル |
| status_bar.py | 40-50 | ステータスバー |
| translation_controller.py | 150-200 | 翻訳処理 |
| dictionary_controller.py | 80-100 | 辞書検索 |
| speech_controller.py | 60-80 | 音声出力 |
| tutor_controller.py | 60-100 | 家庭教師 |
| hotkey_service.py | 80-100 | ホットキー |
| clipboard_service.py | 30-50 | クリップボード |
| window_service.py | 60-80 | ウィンドウ位置 |
| **合計** | **1,110-1,460** | （現状908行から機能追加分含む） |

---

## 10. 変更履歴

| 日付 | バージョン | 変更内容 |
|------|------------|----------|
| 2025-12-29 | 1.0 | 初版作成 |
