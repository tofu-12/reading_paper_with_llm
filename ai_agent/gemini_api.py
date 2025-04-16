import os

from dotenv import load_dotenv

from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch, Part


class GeminiError(Exception):
    pass


class GeminiModel:
    def __init__(self, model_id: str='gemini-2.0-flash'):
        self.model_id = model_id
        self.client = self._get_gemini_client()
    
    def run(self, prompt: str, using_search: bool=False, json_schema=None):
        """
        Geminiモデルにプロンプトを送信し、応答を生成

        Args:
            prompt: Geminiモデルに送信するプロンプト
            using_search: Google検索を使用するか
            json_schema: 構造化出力をする際のJSON schema

        Returns:
            Geminiモデルからの応答テキスト
        
        Raises:
            GeminiError: Geminiによる生成に失敗した場合
        """
        try:
            tools = []
            if using_search:
                tools.append(Tool(google_search=GoogleSearch()))

            config = GenerateContentConfig(
                tools=tools,
            )

            if json_schema is None:
                config.response_modalities = ['TEXT']
            else:
                config.response_mime_type = 'application/json'
                config.response_schema = json_schema

            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=config
            )
                
            response_text = response.text
            return response_text
        
        except Exception as e:
            raise GeminiError(f"AIモデルによる生成に失敗しました: {str(e)}")
    
    def run_with_pdf(self, prompt: str, encoded_pdf, using_search: bool=False, json_schema=None):
        """
        Geminiモデルにプロンプトとpdfを送信し、応答を生成

        Args:
            prompt: Geminiモデルに送信するプロンプト
            encoded_pdf: base64エンコードされたpdf
            using_search: Google検索を使用するか
            json_schema: 構造化出力をする際のJSON schema

        Returns:
            Geminiモデルからの応答テキスト
        
        Raises:
            GeminiError: Geminiによる生成に失敗した場合
        """
        try:
            tools = []
            if using_search:
                tools.append(Tool(google_search=GoogleSearch()))

            config = GenerateContentConfig(
                tools=tools,
            )

            if json_schema is None:
                config.response_modalities = ['TEXT']
            else:
                config.response_mime_type = 'application/json'
                config.response_schema = json_schema

            response = self.client.models.generate_content(
                model=self.model_id,
                contents=[
                    Part.from_bytes(
                        data=encoded_pdf,
                        mime_type='application/pdf',
                    ),
                    prompt
                ],
                config=config
            )
                
            response_text = response.text
            return response_text
        
        except Exception as e:
            raise GeminiError(f"AIモデルによる生成に失敗しました: {str(e)}")
            
    def _get_gemini_client(self):
        """
        Gemini clientの取得

        Returns:
            Gemini client
        
        Raises:
            GeminiError: Geminiのクライアントを取得できない場合
        """
        try:
            # 環境変数の読み込み
            load_dotenv()

            # API keyの取得
            GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

            # clientの取得
            client = genai.Client(api_key=GEMINI_API_KEY)

            return client

        except Exception as e:
            raise GeminiError(f'Geminiのクライエントの初期化に失敗しました: {str(e)}')
    

if __name__ == '__main__':
    client = GeminiModel()
    response = client.run('こんにちわ')
    print(response)

    with open(os.path.join(os.pardir, 'test_data', 'test.pdf'), 'rb') as f:
        encoded_pdf = f.read()
    
    response = client.run_with_pdf('このpdfの内容を日本語で要約してください', encoded_pdf)
    print(response)
