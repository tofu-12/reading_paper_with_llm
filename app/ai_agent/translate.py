import json
import os

from .gemini_api import GeminiModel, GeminiError
from .schemas import TranslateSchema
from .prompt import translate_prompt


class TranslateClient:
    def __init__(self):
        """
        pdfを翻訳するクライエントの初期化
        """
        pass

    def process(self, encoded_pdf, max_trial: int=5) -> TranslateSchema:
        """
        Geminiによるpdfの翻訳

        Args:
            encoded_pdf: base64エンコードされたpdf
            max_trial: 失敗した際に何回繰り返すか
        
        Returns:
            TranslateSchema
        
        Raise:
            GeminiError: Gemini関連のエラー
            Exception: その他のエラー
        """
        for i in range(max_trial):
            try:
                client = GeminiModel()
                prompt = self._create_prompt()
                response = client.run_with_pdf(prompt, encoded_pdf, json_schema=TranslateSchema)

                result = self._parse_response(response)
                return result
            
            except GeminiError as e:
                raise GeminiError(f'Geminiによる要約に失敗しました: {str(e)}')
            
            except Exception as e:
                if i == max_trial - 1:
                    raise Exception(f'Geminiによる要約に失敗しました: {str(e)}')
                else:
                    continue

    def _create_prompt(self):
        """
        Geminiに渡すプロンプトの作成

        Returns:
            Geminiに渡すプロンプト
        
        Raise:
            Exception: エラー
        """
        try:
            prompt = translate_prompt()
            return prompt
        
        except Exception as e:
            raise Exception(f'プロンプトの作成の際にエラーが発生しました: {str(e)}')
    
    def _parse_response(self, response) -> TranslateSchema:
        """
        JSON文字列からSummarySchema型に変換

        Args:
            JSON文字列
        
        Returns:
            SummarySchema
        """
        try:
            response_dict = json.loads(response)
            result = TranslateSchema(**response_dict)

            return result
        
        except Exception as e:
            raise e


def translate_pdf(encoded_pdf, max_trial: int=5) -> TranslateSchema:
    """
    Geminiによるpdfの翻訳

    Args:
        encoded_pdf: base64エンコードされたpdf
        max_trial: 失敗した際に何回繰り返すか
    
    Returns:
        TranslateSchema
    
    Raise:
        GeminiError: Gemini関連のエラー
        Exception: その他のエラー
    """
    try:
        client = TranslateClient()
        result = client.process(encoded_pdf, max_trial)

        return result
    
    except Exception as e:
        raise e


if __name__ == '__main__':
    with open(os.path.join(os.pardir, 'test_data', 'test.pdf'), 'rb') as f:
        encoded_pdf = f.read()
    
    result = translate_pdf(encoded_pdf)
    print(result)
