# ClipboardTranslator v1.00 - Tutor State Management
# 状態管理モジュール

from enum import Enum, auto


class ApplicationState(Enum):
    """アプリケーションの状態"""
    NORMAL = auto()        # 通常翻訳・辞書・読み上げモード
    TUTOR_ACTIVE = auto()  # RAG家庭教師会話モード


class TutorState:
    """家庭教師モードの状態を管理するクラス"""

    def __init__(self):
        self._state = ApplicationState.NORMAL
        self._listeners = []

    @property
    def state(self) -> ApplicationState:
        """現在の状態を取得"""
        return self._state

    @property
    def is_tutor_active(self) -> bool:
        """家庭教師モードがアクティブかどうか"""
        return self._state == ApplicationState.TUTOR_ACTIVE

    def activate_tutor(self):
        """家庭教師モードを起動"""
        if self._state != ApplicationState.TUTOR_ACTIVE:
            self._state = ApplicationState.TUTOR_ACTIVE
            self._notify_listeners('activated')
            print("家庭教師モードを起動しました")

    def deactivate_tutor(self):
        """家庭教師モードを終了"""
        if self._state != ApplicationState.NORMAL:
            self._state = ApplicationState.NORMAL
            self._notify_listeners('deactivated')
            print("家庭教師モードを終了しました")

    def add_listener(self, callback):
        """状態変更リスナーを追加"""
        self._listeners.append(callback)

    def remove_listener(self, callback):
        """状態変更リスナーを削除"""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def _notify_listeners(self, event):
        """リスナーに通知"""
        for listener in self._listeners:
            try:
                listener(event, self._state)
            except Exception as e:
                print(f"リスナー通知エラー: {e}")
