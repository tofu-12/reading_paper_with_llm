def summary_prompt():
    """
    pdfの内容をまとめるプロンプト

    Returns:
        Geminiに渡すプロンプト
    """
    prompt = """
# 指示
あなたはPDFの内容を読み取り、論文の要約をする専門家です。
与えられた論文のPDFの内容を読み取り、出力の指示の通りにまとめてください。
なお、出力の際には誤りがないことを確認してください。

# 出力の指示
以下の12つの情報を含むJSON形式で出力してください。
なお、1番の英語のタイトルと12番の重要な参考文献以外は日本語で答えてください。
1. 英語のタイトル
2. 日本語のタイトル
3. 発表年度
4. ジャーナルまたはカンファレンス
5. 論文のキーワード
6. Abstractの日本語訳
7. 提案手法の要約
8. 提案手法の新規性についての要約
9. 実験内容とその結果の要約
10. 今後についての要約
11. 全体の要約
12. 重要な参考文献

また、以下のJSON schemaを利用してください。
result = {
    "English_Title": str,
    "Japanese_Title": str,
    "Publication_Year": int,
    "Journal_or_Conference": str,
    "Keywords": list[str],
    "Japanese_Abstract": str,
    "Summary_of_Proposed_Method": str,
    "Summary_of_Novelty_of_Proposed_Method": str,
    "Summary_of_Experiments_and_Results": str,
    "Summary_of_Future_Work": str,
    "Overall_Summary": str,
    "Important_Reference": list[str]
}
Return: result
"""

    return prompt


def translate_prompt():
    """
    pdfの内容を翻訳するプロンプト

    Returns:
        Geminiに渡すプロンプト
    """
    prompt = """
# 指示
あなたはPDFの内容を読み取り、英語を日本語に訳す専門家です。
与えられたPDFの論文の内容をそのまま日本語に翻訳してください。
翻訳の際には内容に過不足なく行ない、論文全体の構造を保ってください。

# 出力の指示
以下の10つの情報を含むJSON形式で出力してください。
1. 英語のタイトル
2. 日本語のタイトル
3. 発表年度
4. ジャーナルまたはカンファレンス
5. 論文のキーワード
6. Abstractの日本語訳
7. Introductionの日本語訳
8. Related_Researchの日本語訳
9. Methodの日本語訳
10. Conclusionの日本語訳

また、以下のJSON schemaを利用してください。
result = {
    "English_Title": str,
    "Japanese_Title": str,
    "Publication_Year": int,
    "Journal_or_Conference": str,
    "Keywords": list[str],
    "Abstract": str,
    "Introduction": str,
    "Related_Research": str,
    "Method": str,
    "Conclusion": str
}
Return: result
"""

    return prompt
