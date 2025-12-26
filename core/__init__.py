# ClipboardTranslator v1.00 - Core Module
from .translation import translate_with_deepl, translate_with_google, query_claude_api
from .dictionary import check_dictionary, load_ngsl_dictionary, save_dictionary_cache, load_dictionary_cache
from .language_detection import detect_language, is_single_word
from .text_to_speech import TextToSpeechHandler
from .history import TranslationHistory
from .network import is_connected
