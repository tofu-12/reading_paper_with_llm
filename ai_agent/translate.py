import json
import os
import sys
sys.path.append(os.pardir)

from ai_agent.gemini_api import GeminiModel, GeminiError
from ai_agent.schemas import TranslateSchema
from ai_agent.prompt import translate_prompt


class TranslateClient:
    def __init__(self):
        """
        pdfを翻訳するクライエントの初期化
        """
        pass

    def process(self, encoded_pdf, max_trial: int=5):
        """
        Geminiによるpdfの翻訳

        Args:
            encoded_pdf: base64エンコードされたpdf
            max_trial: 失敗した際に何回繰り返すか
        
        Returns:
            dict
                English_Title: 英語のタイトル
                Japanese_Title: 日本語のタイトル
                Publication_Year: 発表年度
                Journal_or_Conference: ジャーナルまたはカンファレンス
                Keywords: 論文のキーワード
                Abstract: abstract
                Introduction: introduction
                Related_Research: related research
                Method: method
                Conclusion: conclusion
        
        Raise:
            GeminiError: Gemini関連のエラー
            Exception: その他のエラー
        """
        for i in range(max_trial):
            try:
                client = GeminiModel()
                prompt = self._create_prompt()
                response = client.run_with_pdf(prompt, encoded_pdf, json_schema=TranslateSchema)

                result_dict = json.loads(response)
                return result_dict
            
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


def translate_pdf(encoded_pdf, max_trial: int=5):
    """
    Geminiによるpdfの翻訳

    Args:
        encoded_pdf: base64エンコードされたpdf
        max_trial: 失敗した際に何回繰り返すか
    
    Returns:
        dict
            English_Title: 英語のタイトル
            Japanese_Title: 日本語のタイトル
            Publication_Year: 発表年度
            Journal_or_Conference: ジャーナルまたはカンファレンス
            Keywords: 論文のキーワード
            Abstract: abstract
            Introduction: introduction
            Related_Research: related research
            Method: method
            Conclusion: conclusion
    
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
