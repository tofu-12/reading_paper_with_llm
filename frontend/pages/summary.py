import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st

from app.ai_agent.summary import summary_pdf
from app.ai_agent.schemas import SummarySchema
from app.notion.notion_api import NotionClient


def show_result(summary_result: SummarySchema):
    try:
        st.subheader("論文情報")
        st.text('English Title:')
        st.code(summary_result.English_Title, language='text')
        st.text('タイトル:')
        st.code(summary_result.Japanese_Title, language='text')
        st.text("発表年度:")
        st.code(str(summary_result.Publication_Year), language='text')
        st.text("ジャーナル/カンファレンス:")
        st.code(summary_result.Journal_or_Conference, language='text')
        st.text("キーワード:")
        st.code(', '.join(summary_result.Keywords), language='text')

        st.subheader("概要")
        st.text(summary_result.Japanese_Abstract)

        st.subheader("提案手法")
        st.text(summary_result.Summary_of_Proposed_Method)

        st.subheader("新規性")
        st.text(summary_result.Summary_of_Novelty_of_Proposed_Method)

        st.subheader("実験と結果")
        st.text(summary_result.Summary_of_Experiments_and_Results)

        st.subheader("今後の展望")
        st.text(summary_result.Summary_of_Future_Work)

        st.subheader("全体のまとめ")
        st.text(summary_result.Overall_Summary)

        st.subheader("重要な参考文献")
        reference_str = ''
        for ref in summary_result.Important_Reference:
            reference_str += f"- {ref}\n"
        st.write(reference_str)
    
    except Exception as e:
        raise e


st.title('Summary Paper with LLM')

pdf = st.file_uploader('論文のPDFファイルを選択してください', type="pdf")

if pdf is not None:
    if st.button('要約を実行'):
        try:
            with st.spinner('PDFファイルを要約中です...'):
                encoded_pdf = pdf.getvalue()
                summary_result = summary_pdf(encoded_pdf)
            
            show_result(summary_result)

            notion_client = NotionClient()
            notion_client.save_data(summary_result)

            st.success("Notionへの保存に成功しました")
            
        except Exception as e:
            st.error(e)
