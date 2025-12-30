# ClipboardTranslator v1.20 - Translation Module
import requests
import json
import sys
import os

# 親ディレクトリをパスに追加
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.constants import DEEPL_URL, CLAUDE_API_URL, TRANSLATION_LANGUAGES
from config.settings import config


# DeepL API言語コードマッピング（v1.20: 多言語対応）
# DeepL APIは一部の言語で特殊なコードを使用する
DEEPL_LANG_CODE_MAP = {
    'ZH': 'ZH-HANS',  # 中国語簡体字
    'PT-BR': 'PT-BR',  # ブラジルポルトガル語
}


def translate_with_deepl(text, target_lang):
    """
    DeepL APIを使用してテキストを翻訳

    Parameters:
        text (str): 翻訳するテキスト
        target_lang (str): 翻訳先言語コード（JA, EN, ZH, KO, FR, DE, ES, PT-BR, IT, NL, PL, RU）

    Returns:
        str: 翻訳されたテキスト、エラー時はNone
    """
    try:
        api_key = config.get('Settings', 'deepl_api_key', fallback='')
        if not api_key:
            print("DeepL APIキーが設定されていません。設定画面から設定してください。")
            return None

        # 言語コードをDeepL API形式に変換
        target_lang_code = DEEPL_LANG_CODE_MAP.get(target_lang, target_lang)

        headers = {
            'Authorization': f'DeepL-Auth-Key {api_key}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'text': text,
            'target_lang': target_lang_code
        }

        response = requests.post(DEEPL_URL, headers=headers, data=data, timeout=10)

        if response.status_code == 200:
            response_data = response.json()
            translated_text = response_data['translations'][0]['text']
            return translated_text
        else:
            print(f"DeepL API エラー: ステータスコード {response.status_code}")
            print(f"レスポンス: {response.text}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"DeepL API リクエストエラー: {e}")
        return None
    except Exception as e:
        print(f"DeepL翻訳中に予期しないエラーが発生しました: {e}")
        return None


def translate_with_google(text, target_lang_code):
    """
    Googleの非公式API(googletrans)を用いてテキストを翻訳する関数。
    日本語(JA)・英語(EN)以外の入力を翻訳する際などに使用する。
    """
    try:
        from googletrans import Translator
        translator = Translator()

        lang_map = {
            'EN': 'en',
            'JA': 'ja'
        }
        if target_lang_code in lang_map:
            target_lang_code = lang_map[target_lang_code]

        result = translator.translate(text, dest=target_lang_code)
        return result.text
    except Exception as e:
        print(f"Google翻訳中にエラーが発生しました: {e}")
        return None


# Claude API モデル定義（2025年12月時点の最新）
CLAUDE_MODELS = {
    'sonnet': 'claude-sonnet-4-5-20250929',   # 推奨: バランス型、コーディング・エージェント向け
    'haiku': 'claude-haiku-4-5-20251001',     # 高速・低コスト
    'opus': 'claude-opus-4-5-20251101',       # 最高性能・高コスト
}

# デフォルトモデル
DEFAULT_CLAUDE_MODEL = 'sonnet'


def query_claude_api(word, prompt_template, api_key, model_type=None):
    """
    Claude APIを使用して単語の意味や使い方を取得する（ストリーミングモード）

    Parameters:
    word (str): 調べたい単語
    prompt_template (str): プロンプトテンプレート。{word}は実際の単語に置換される
    api_key (str): Claude API キー
    model_type (str): モデルタイプ ('sonnet', 'haiku', 'opus')。Noneの場合はデフォルト

    Returns:
    str: Claude APIからの応答テキスト、エラーの場合はNone
    """
    try:
        prompt = prompt_template.format(word=word)

        # モデル選択
        if model_type and model_type in CLAUDE_MODELS:
            model = CLAUDE_MODELS[model_type]
        else:
            model = CLAUDE_MODELS[DEFAULT_CLAUDE_MODEL]

        headers = {
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json"
        }

        data = {
            "model": model,
            "max_tokens": 1000,
            "stream": True,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }

        result_text = ""
        with requests.post(CLAUDE_API_URL, headers=headers, json=data, stream=True, timeout=15) as response:
            if response.status_code != 200:
                print(f"Claude API エラー: ステータスコード {response.status_code}")
                print(f"レスポンス: {response.text}")
                return None

            for line in response.iter_lines():
                if line:
                    line_text = line.decode('utf-8')

                    if line_text.startswith('data: '):
                        json_str = line_text[6:]

                        if json_str == "[DONE]":
                            continue

                        try:
                            data = json.loads(json_str)

                            if data.get('type') == 'content_block_delta' and 'delta' in data and 'text' in data['delta']:
                                result_text += data['delta']['text']
                        except json.JSONDecodeError:
                            print(f"JSONパースエラー: {json_str}")

            return result_text

    except requests.exceptions.RequestException as e:
        print(f"Claude API リクエストエラー: {e}")
        return None
    except Exception as e:
        print(f"Claude API 呼び出し中に予期しないエラーが発生しました: {e}")
        return None
