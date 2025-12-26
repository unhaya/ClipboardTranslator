# ClipboardTranslator v1.00 - Settings Manager
import os
import sys
import configparser
from .constants import DEFAULT_SETTINGS

# Global config object
config = configparser.ConfigParser()

def get_config_file_path():
    """設定ファイルのパスを取得する関数"""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config_path = os.path.join(script_dir, 'data', 'translation_app.ini')
    return config_path

def get_data_dir():
    """データディレクトリのパスを取得"""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(script_dir, 'data')

class ConfigManager:
    """設定管理クラス"""

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config_file = get_config_file_path()
        self.load_config()

    def load_config(self):
        """設定を読み込み、必要なデフォルト値を設定"""
        # データディレクトリがなければ作成
        data_dir = os.path.dirname(self.config_file)
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # 設定ファイルの存在確認
        if os.path.exists(self.config_file):
            try:
                self.config.read(self.config_file, encoding='utf-8')
                print(f"設定ファイル読み込み成功: {self.config_file}")
            except Exception as e:
                print(f"設定ファイル読み込みエラー: {e}")

        # 'Settings'セクションがない場合は作成
        if not self.config.has_section('Settings'):
            print("Settingsセクションを新規作成します")
            self.config.add_section('Settings')
            for key, value in DEFAULT_SETTINGS.items():
                self.config['Settings'][key] = value
            self.save_config()
        else:
            # 必要なキーが存在しない場合は追加
            needs_update = False
            for key, default_value in DEFAULT_SETTINGS.items():
                if key not in self.config['Settings']:
                    self.config['Settings'][key] = default_value
                    needs_update = True
                    print(f"不足している設定キーを追加: {key}")

            if needs_update:
                self.save_config()

    def save_config(self):
        """設定をファイルに保存"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                self.config.write(f)
            print(f"設定ファイルを保存しました: {self.config_file}")
        except Exception as e:
            print(f"設定ファイル保存エラー: {e}")

    def get(self, section, key, fallback=''):
        """設定値を取得"""
        return self.config.get(section, key, fallback=fallback)

    def get_bool(self, section, key, fallback=False):
        """設定値をboolとして取得"""
        try:
            value = self.config.get(section, key, fallback=str(fallback))
            return value.lower() in ('true', 'yes', '1', 'on')
        except:
            return fallback

    def get_int(self, section, key, fallback=0):
        """設定値をintとして取得"""
        try:
            return int(self.config.get(section, key, fallback=str(fallback)))
        except:
            return fallback

    def get_float(self, section, key, fallback=0.0):
        """設定値をfloatとして取得"""
        try:
            return float(self.config.get(section, key, fallback=str(fallback)))
        except:
            return fallback

    def set(self, section, key, value):
        """設定値を設定"""
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config[section][key] = str(value)

    def save(self):
        """設定を保存（エイリアス）"""
        self.save_config()


def load_config():
    """設定を読み込み（後方互換性のため）"""
    global config
    config_file = get_config_file_path()

    # データディレクトリがなければ作成
    data_dir = os.path.dirname(config_file)
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)

    if os.path.exists(config_file):
        try:
            config.read(config_file, encoding='utf-8')
            print(f"設定ファイル読み込み成功: {config_file}")
        except Exception as e:
            print(f"設定ファイル読み込みエラー: {e}")

    if not config.has_section('Settings'):
        config.add_section('Settings')
        for key, value in DEFAULT_SETTINGS.items():
            config['Settings'][key] = value

        try:
            with open(config_file, 'w', encoding='utf-8') as f:
                config.write(f)
            print(f"新しい設定ファイルを作成しました: {config_file}")
        except Exception as e:
            print(f"設定ファイル作成エラー: {e}")
    else:
        needs_update = False
        for key, default_value in DEFAULT_SETTINGS.items():
            if key not in config['Settings']:
                config['Settings'][key] = default_value
                needs_update = True

        if needs_update:
            try:
                with open(config_file, 'w', encoding='utf-8') as f:
                    config.write(f)
            except Exception as e:
                print(f"設定ファイル更新エラー: {e}")
