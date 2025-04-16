import json
import os
import sys
sys.path.append(os.pardir)

from ai_agent.gemini_api import GeminiModel, GeminiError
from ai_agent.prompt import summary_prompt
from ai_agent.schemas import SummarySchema


class SummaryClient:
    def __init__(self):
        """
        pdfを要約するクライエントの初期化
        """
        pass

    def process(self, encoded_pdf, max_trial: int=5):
        """
        Geminiによるpdfの要約

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
                Japanese_Abstract: Abstractの日本語訳
                Summary_of_Proposed_Method: 提案手法の要約
                Summary_of_Novelty_of_Proposed_Method: 提案手法の新規性についての要約
                Summary_of_Experiments_and_Results: 実験内容とその結果の要約
                Summary_of_Future_Work: 今後についての要約
                Overall_Summary: 全体の要約
                Important_Reference: 重要な参考文献
        
        Raise:
            GeminiError: Gemini関連のエラー
            Exception: その他のエラー
        """
        for i in range(max_trial):
            try:
                client = GeminiModel()
                prompt = self._create_prompt()
                response = client.run_with_pdf(prompt, encoded_pdf, json_schema=SummarySchema)

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
            prompt = summary_prompt()
            return prompt
        
        except Exception as e:
            raise Exception(f'プロンプトの作成の際にエラーが発生しました: {str(e)}')


def summary_pdf(encoded_pdf, max_trial: int=5):
    """
    Geminiによるpdfの要約

    Args:
        encoded_pdf: base64エンコードされたpdf
        max_trial: 失敗した際に何回繰り返すか
    
    Returns:
        dict (SummarySchema)
            English_Title: 英語のタイトル
            Japanese_Title: 日本語のタイトル
            Publication_Year: 発表年度
            Journal_or_Conference: ジャーナルまたはカンファレンス
            Keywords: 論文のキーワード
            Japanese_Abstract: Abstractの日本語訳
            Summary_of_Proposed_Method: 提案手法の要約
            Summary_of_Novelty_of_Proposed_Method: 提案手法の新規性についての要約
            Summary_of_Experiments_and_Results: 実験内容とその結果の要約
            Summary_of_Future_Work: 今後についての要約
            Overall_Summary: 全体の要約
            Important_Reference: 重要な参考文献
    
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
