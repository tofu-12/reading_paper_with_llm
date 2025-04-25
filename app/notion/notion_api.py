import os
from typing import List, Dict, Any

from dotenv import load_dotenv
import requests

from ..ai_agent.schemas import SummarySchema


class NotionClient:
    def __init__(self):
        """
        Notionと接続するクライエントの初期化
        """
        # 環境変数の読み込み
        load_dotenv()

        # 環境変数の取得
        self.NOTION_API_KEY = os.getenv("NOTION_API_KEY")
        self.DATABASE_ID = os.getenv("DATABASE_ID")

    def save_data(self, summary_result: SummarySchema) -> None:
        """
        notionにデータを記録

        Args:
            summary_result: Geminiのまとめた結果
        """
        try:
            url = 'https://api.notion.com/v1/pages'

            headers =  {
                'Notion-Version': '2022-06-28',
                'Authorization': 'Bearer ' + self.NOTION_API_KEY,
                'Content-Type': 'application/json',
            }

            properties = self._get_propaties(summary_result)
            children = self._get_children(summary_result)

            json_data = {
                'parent': { 'database_id': self.DATABASE_ID },
                'properties': properties,
                'children': children
            }

            response = requests.post(url, headers=headers, json=json_data)

            if response.status_code != 200:
                print(f"ステータスコード: {str(response.status_code)}, エラーメッセージ: {response.text}")
                raise Exception(f"ステータスコード: {str(response.status_code)}, エラーメッセージ: {response.text}")
            else:
                print("Notionへの保存に成功しました")
        
        except Exception as e:
            print(f"結果のnotionへの保存に失敗しました: {str(e)}")
            raise Exception(f"結果のnotionへの保存に失敗しました: {str(e)}")
    
    def _get_propaties(self, summary_result: SummarySchema) -> dict:
        """
        保存するページのプロパティを作成

        Args:
            summary_result: Geminiのまとめた結果
        
        Returns:
            dict: プロパティをまとめた辞書型
        """
        properties = {
            'English Title': {
                'title': [
                    {
                        'text': {
                            'content': summary_result.English_Title
                        }
                    }
                ]
            },
            'Japanese Title': {
                'rich_text': [
                    {
                        'text': {
                            'content': summary_result.Japanese_Title
                        }
                    }
                ]
            },
            'Publication Year': {
                'number': summary_result.Publication_Year
            },
            'Journal/Conference': {
                'rich_text': [
                    {
                        'text': {
                            'content': summary_result.Journal_or_Conference
                        }
                    }
                ]
            },
            'Keywords': {
                'multi_select': [{'name': keyword} for keyword in summary_result.Keywords]
            }
        }

        return properties

    def _get_children(self, summary_result: SummarySchema) -> List[Dict[str, Any]]:
        """
        保存するページの内容を生成

        Args:
            summary_result: Geminiのまとめた結果
        
        Returns:
            List[Dict[str, Any]]: ページを構成するブロックをまとめたlist
        """
        children: List[Dict[str, Any]] = []

        # ページ本文にセクションを追加するヘルパー関数
        def add_section(title: str, content: str):
            if content: # 内容がある場合のみ追加
                children.append({
                    'object': 'block',
                    'type': 'heading_3',
                    'heading_3': {
                        'rich_text': [{'type': 'text', 'text': {'content': title}}]
                    }
                })
                # 長いテキストの場合、一つのパラグラフブロックに入れる
                children.append({
                    'object': 'block',
                    'type': 'paragraph',
                    'paragraph': {
                        'rich_text': [{'type': 'text', 'text': {'content': content}}]
                    }
                })
        
        # 各要約項目をページ本文に追加
        add_section("Japanese Abstract", summary_result.Japanese_Abstract)
        add_section("Summary of Proposed Method", summary_result.Summary_of_Proposed_Method)
        add_section("Summary of Novelty of Proposed Method", summary_result.Summary_of_Novelty_of_Proposed_Method)
        add_section("Summary of Experiments and Results", summary_result.Summary_of_Experiments_and_Results)
        add_section("Summary of Future Work", summary_result.Summary_of_Future_Work)
        add_section("Overall Summary", summary_result.Overall_Summary)

        # 重要な参考文献をリストとして追加
        if summary_result.Important_Reference:
            children.append({
                'object': 'block',
                'type': 'heading_2',
                'heading_2': {
                    'rich_text': [{'type': 'text', 'text': {'content': "Important References"}}]
                }
            })
            for reference in summary_result.Important_Reference:
                children.append({
                    'object': 'block',
                    'type': 'bulleted_list_item',
                    'bulleted_list_item': {
                        'rich_text': [{'type': 'text', 'text': {'content': reference}}]
                    }
                })
        
        return children
