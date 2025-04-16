from pydantic import BaseModel


class SummarySchema(BaseModel):
    """
    Geminiに指示する要約のJSON schema

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
    """
    English_Title: str
    Japanese_Title: str
    Publication_Year: int
    Journal_or_Conference: str
    Keywords: list[str]
    Japanese_Abstract: str
    Summary_of_Proposed_Method: str
    Summary_of_Novelty_of_Proposed_Method: str
    Summary_of_Experiments_and_Results: str
    Summary_of_Future_Work: str
    Overall_Summar: str
    Important_Reference: list[str]
