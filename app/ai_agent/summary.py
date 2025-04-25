import json
import os

from .gemini_api import GeminiModel, GeminiError
from .prompt import summary_prompt
from .schemas import SummarySchema


class SummaryClient:
    def __init__(self):
        """
        pdfを要約するクライエントの初期化
        """
        pass

    def process(self, encoded_pdf, max_trial: int=5) -> SummarySchema:
        """
        Geminiによるpdfの要約

        Args:
            encoded_pdf: base64エンコードされたpdf
            max_trial: 失敗した際に何回繰り返すか
        
        Returns:
            SummarySchema
        
        Raise:
            GeminiError: Gemini関連のエラー
            Exception: その他のエラー
        """
        for i in range(max_trial):
            try:
                client = GeminiModel()
                prompt = self._create_prompt()
                response = client.run_with_pdf(prompt, encoded_pdf, json_schema=SummarySchema)

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
            prompt = summary_prompt()
            return prompt
        
        except Exception as e:
            raise Exception(f'プロンプトの作成の際にエラーが発生しました: {str(e)}')
    
    def _parse_response(self, response) -> SummarySchema:
        """
        JSON文字列からSummarySchema型に変換

        Args:
            JSON文字列
        
        Returns:
            SummarySchema
        """
        try:
            response_dict = json.loads(response)
            result = SummarySchema(**response_dict)

            return result
        
        except Exception as e:
            raise e


def summary_pdf(encoded_pdf, max_trial: int=5) -> SummarySchema:
    """
    Geminiによるpdfの要約

    Args:
        encoded_pdf: base64エンコードされたpdf
        max_trial: 失敗した際に何回繰り返すか
    
    Returns:
        SummarySchema
    
    Raise:
        GeminiError: Gemini関連のエラー
        Exception: その他のエラー
    """
    try:
        client = SummaryClient()
        result = client.process(encoded_pdf, max_trial)

        return result
    
    except Exception as e:
        raise e


if __name__ == '__main__':
    with open(os.path.join(os.pardir, 'test_data', 'test.pdf'), 'rb') as f:
        encoded_pdf = f.read()
    
    result = summary_pdf(encoded_pdf)
    print(result)
