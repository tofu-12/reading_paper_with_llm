import os
import sys
sys.path.append(os.pardir)
sys.path.append(os.path.join(os.pardir, os.pardir))

import streamlit as st

from ai_agent.summary import summary_pdf
from ai_agent.schemas import SummarySchema


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
        st.code(summary_result.Japanese_Abstract, language='text')

        st.subheader("提案手法")
        st.code(summary_result.Summary_of_Proposed_Method, language='text')

        st.subheader("新規性")
        st.code(summary_result.Summary_of_Novelty_of_Proposed_Method, language='text')

        st.subheader("実験と結果")
        st.code(summary_result.Summary_of_Experiments_and_Results, language='text')

        st.subheader("今後の展望")
        st.code(summary_result.Summary_of_Future_Work, language='text')

        st.subheader("全体のまとめ")
        st.code(summary_result.Overall_Summary, language='text')

        st.subheader("重要な参考文献")
        reference_str = '[ \n'
        for ref in summary_result.Important_Reference:
            reference_str += f"    \"{ref}\",\n"
        reference_str += "]"
        st.code(reference_str, language='text')
    
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
            
        except Exception as e:
            st.error(str(e))
