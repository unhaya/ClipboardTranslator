# ClipboardTranslator v1.10 - Controllers
"""
コントローラーモジュール
- TranslationController: 翻訳処理 (Phase 5-1)
- DictionaryController: 辞書検索処理 (Phase 5-2)
- SpeechController: 音声出力処理 (Phase 5-3)
- TutorController: 家庭教師処理 (Phase 5-4)
"""
from .translation_controller import TranslationController
from .dictionary_controller import DictionaryController
from .speech_controller import SpeechController
from .tutor_controller import TutorController

__all__ = ['TranslationController', 'DictionaryController', 'SpeechController', 'TutorController']
