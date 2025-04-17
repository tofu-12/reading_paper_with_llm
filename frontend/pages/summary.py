import os
import sys
sys.path.append(os.pardir)
sys.path.append(os.path.join(os.pardir, os.pardir))

import streamlit as st

from ai_agent.summary import summary_pdf


def show_result(summary_result):
    try:
        st.subheader("論文情報")
        st.text(f'English Title:\n{summary_result['English_Title']}')
        st.text(f'タイトル:\n{summary_result['Japanese_Title']}')
        st.text(f"発表年度:\n{str(summary_result['Publication_Year'])}")
        st.text(f"ジャーナル/カンファレンス:\n{summary_result['Journal_or_Conference']}")
        st.text(f"キーワード:\n{', '.join(summary_result['Keywords'])}")

        st.subheader("概要")
        st.text(summary_result['Japanese_Abstract'])

        st.subheader("提案手法")
        st.text(summary_result['Summary_of_Proposed_Method'])

        st.subheader("新規性")
        st.text(summary_result['Summary_of_Novelty_of_Proposed_Method'])

        st.subheader("実験と結果")
        st.text(summary_result['Summary_of_Experiments_and_Results'])

        st.subheader("今後の展望")
        st.text(summary_result['Summary_of_Future_Work'])

        st.subheader("全体のまとめ")
        st.text(summary_result['Overall_Summary'])

        st.subheader("重要な参考文献")
        for ref in summary_result['Important_Reference']:
            st.markdown(f"- {ref}")
    
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
