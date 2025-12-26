# ClipboardTranslator v1.00 - Text to Speech Module
import tempfile
import os
import time
import socket
import threading

try:
    import pygame
    from gtts import gTTS
    import langid
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("音声出力モジュール(gtts, pygame)がインストールされていません")


class TextToSpeechHandler:
    """テキストを音声に変換して再生するためのハンドラークラス"""

    def __init__(self, status_callback=None, error_callback=None):
        """
        TextToSpeechHandlerの初期化

        Parameters:
        status_callback (callable): 状態更新時に呼び出されるコールバック関数
        error_callback (callable): エラー発生時に呼び出されるコールバック関数
        """
        self.status_callback = status_callback
        self.error_callback = error_callback
        self.is_playing = False
        self.temp_file = None

        if TTS_AVAILABLE:
            pygame.mixer.init()

    def update_status(self, message):
        """状態更新コールバックを呼び出す"""
        if self.status_callback:
            self.status_callback(message)

    def report_error(self, message):
        """エラーコールバックを呼び出す"""
        if self.error_callback:
            self.error_callback(message)

    def is_connected(self):
        """インターネット接続を確認する"""
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def detect_language(self, text):
        """
        テキストの言語を検出する

        Returns:
        str: 言語コード ('ja', 'en', etc.)
        """
        if not text:
            return 'en'

        if len(text.strip()) <= 5:
            if any(ord(c) > 127 for c in text):
                return 'ja'
            if all(ord(c) < 128 for c in text):
                return 'en'

        try:
            detected_lang, confidence = langid.classify(text)
            return detected_lang
        except Exception as e:
            print(f"言語検出に失敗しました: {e}")
            if any(ord(c) > 127 for c in text):
                return 'ja'
            return 'en'

    def speak(self, text, volume=1.0):
        """
        テキストを音声に変換して再生する

        Parameters:
        text (str): 音声に変換するテキスト
        volume (float): 音量 (0.0 ~ 1.0)

        Returns:
        bool: 成功した場合はTrue、失敗した場合はFalse
        """
        if not TTS_AVAILABLE:
            self.report_error("音声出力モジュールがインストールされていません")
            return False

        if not text:
            self.report_error("テキストが空です")
            return False

        if self.is_playing:
            self.report_error("すでに音声を再生中です")
            return False

        if not self.is_connected():
            self.report_error("インターネット接続がありません")
            return False

        threading.Thread(target=self._speak_thread, args=(text, volume), daemon=True).start()
        return True

    def _speak_thread(self, text, volume):
        """音声出力処理を行うスレッド"""
        self.is_playing = True
        self.update_status("言語を検出中...")

        try:
            lang = self.detect_language(text)
            self.update_status(f"音声を生成中... ({lang})")

            fd, self.temp_file = tempfile.mkstemp(suffix='.mp3')
            os.close(fd)

            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(self.temp_file)

            self.update_status("音声を再生中...")

            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.load(self.temp_file)
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            self.update_status("音声再生完了")

        except Exception as e:
            self.report_error(f"音声出力エラー: {e}")
        finally:
            if self.temp_file and os.path.exists(self.temp_file):
                try:
                    os.remove(self.temp_file)
                    self.temp_file = None
                except Exception as e:
                    print(f"一時ファイル削除エラー: {e}")

            self.is_playing = False

    def stop(self):
        """音声再生を停止する"""
        if self.is_playing and TTS_AVAILABLE:
            try:
                pygame.mixer.music.stop()
                self.update_status("音声再生を停止しました")
            except Exception as e:
                print(f"音声停止エラー: {e}")

            self.is_playing = False

    def cleanup(self):
        """リソースを解放する"""
        self.stop()

        if self.temp_file and os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
                self.temp_file = None
            except Exception as e:
                print(f"一時ファイル削除エラー: {e}")

        if TTS_AVAILABLE:
            try:
                pygame.mixer.quit()
            except:
                pass
