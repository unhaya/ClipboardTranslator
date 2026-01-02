# ClipboardTranslator v1.20 - Prompt Manager
# 外部INIファイルからプロンプトを管理するモジュール

import configparser
import os
from pathlib import Path

# ハードコードのデフォルトプロンプト（フォールバック用）
from config.constants import DEFAULT_CLAUDE_PROMPTS, DEFAULT_TUTOR_PROMPTS


class PromptManager:
    """外部INIファイルからプロンプトを管理するクラス"""

    def __init__(self):
        self.config = configparser.ConfigParser()
        # 複数行の値を正しく読み込むための設定
        self.config.optionxform = str  # キーの大文字小文字を保持
        self._prompts_file = None
        self._loaded = False

    def _get_prompts_file_path(self) -> str:
        """prompts.iniのパスを取得"""
        if self._prompts_file:
            return self._prompts_file

        # 実行ファイルまたはスクリプトのディレクトリを基準にする
        if getattr(sys, 'frozen', False):
            # PyInstallerでビルドされた場合
            base_dir = Path(sys.executable).parent
        else:
            # 開発環境
            base_dir = Path(__file__).parent.parent

        self._prompts_file = str(base_dir / 'data' / 'prompts.ini')
        return self._prompts_file

    def load(self):
        """INIファイルを読み込み、なければデフォルトから生成"""
        prompts_file = self._get_prompts_file_path()

        if os.path.exists(prompts_file):
            try:
                self.config.read(prompts_file, encoding='utf-8')
                self._loaded = True
            except Exception as e:
                print(f"Warning: Failed to load prompts.ini: {e}")
                self._loaded = False
        else:
            # ファイルが存在しない場合、デフォルトから生成
            self._create_default_file()

    def _create_default_file(self):
        """constants.pyのデフォルトからINIファイルを生成"""
        # 辞書プロンプト
        for lang, prompt in DEFAULT_CLAUDE_PROMPTS.items():
            section = f'Dictionary_{lang}'
            self.config[section] = {'prompt': prompt.strip()}

        # 家庭教師プロンプト
        for lang, prompt in DEFAULT_TUTOR_PROMPTS.items():
            section = f'Tutor_{lang}'
            self.config[section] = {'prompt': prompt.strip()}

        self.save()
        self._loaded = True

    def get_dictionary_prompt(self, lang: str) -> str:
        """辞書プロンプト取得（フォールバック付き）"""
        if not self._loaded:
            self.load()

        section = f'Dictionary_{lang}'
        if section in self.config:
            prompt = self.config[section].get('prompt', '')
            if prompt:
                return prompt

        # フォールバック: ENセクション
        en_section = 'Dictionary_EN'
        if en_section in self.config:
            prompt = self.config[en_section].get('prompt', '')
            if prompt:
                return prompt

        # 最終フォールバック: ハードコードデフォルト
        return DEFAULT_CLAUDE_PROMPTS.get(lang, DEFAULT_CLAUDE_PROMPTS['EN'])

    def get_tutor_prompt(self, lang: str) -> str:
        """家庭教師プロンプト取得（フォールバック付き）"""
        if not self._loaded:
            self.load()

        section = f'Tutor_{lang}'
        if section in self.config:
            prompt = self.config[section].get('prompt', '')
            if prompt:
                return prompt

        # フォールバック: ENセクション
        en_section = 'Tutor_EN'
        if en_section in self.config:
            prompt = self.config[en_section].get('prompt', '')
            if prompt:
                return prompt

        # 最終フォールバック: ハードコードデフォルト
        return DEFAULT_TUTOR_PROMPTS.get(lang, DEFAULT_TUTOR_PROMPTS['EN'])

    def set_dictionary_prompt(self, lang: str, prompt: str):
        """辞書プロンプトを設定"""
        section = f'Dictionary_{lang}'
        if section not in self.config:
            self.config[section] = {}
        self.config[section]['prompt'] = prompt.strip()

    def set_tutor_prompt(self, lang: str, prompt: str):
        """家庭教師プロンプトを設定"""
        section = f'Tutor_{lang}'
        if section not in self.config:
            self.config[section] = {}
        self.config[section]['prompt'] = prompt.strip()

    def save(self):
        """INIファイルに保存"""
        prompts_file = self._get_prompts_file_path()

        # ディレクトリが存在しない場合は作成
        os.makedirs(os.path.dirname(prompts_file), exist_ok=True)

        try:
            with open(prompts_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
        except Exception as e:
            print(f"Warning: Failed to save prompts.ini: {e}")

    def reload(self):
        """INIファイルを再読み込み"""
        self._loaded = False
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.load()


# sysモジュールのインポート（frozen属性のため）
import sys

# グローバルインスタンス（遅延初期化）
_prompt_manager = None


def get_prompt_manager() -> PromptManager:
    """PromptManagerのシングルトンインスタンスを取得"""
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = PromptManager()
    return _prompt_manager
