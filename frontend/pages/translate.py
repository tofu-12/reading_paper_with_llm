import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import streamlit as st

from app.ai_agent.translate import translate_pdf
from app.ai_agent.schemas import TranslateSchema


def show_result(translate_result: TranslateSchema):
    try:
        st.subheader("論文情報")
        st.text('English Title:')
        st.code(translate_result.English_Title, language='text')
        st.text('タイトル:')
        st.code(translate_result.Japanese_Title, language='text')
        st.text("発表年度:")
        st.code(str(translate_result.Publication_Year), language='text')
        st.text("ジャーナル/カンファレンス:")
        st.code(translate_result.Journal_or_Conference, language='text')
        st.text("キーワード:")
        st.code(', '.join(translate_result.Keywords), language='text')

        st.subheader("概要")
        st.code(translate_result.Abstract, language='text')

        st.subheader("イントロダクション")
        st.code(translate_result.Introduction, language='text')

        st.subheader("関連研究")
        st.code(translate_result.Related_Research, language='text')

        st.subheader("提案手法")
        st.code(translate_result.Method, language='text')

        st.subheader("まとめ")
        st.code(translate_result.Conclusion, language='text')
    except Exception as e:
        raise e


st.title('Translate Paper with LLM')

pdf = st.file_uploader('論文のPDFファイルを選択してください', type="pdf")

if pdf is not None:
    if st.button('翻訳を実行'):
        try:
            with st.spinner('PDFファイルを翻訳中です...'):
                encoded_pdf = pdf.getvalue()
                translate_result = translate_pdf(encoded_pdf)
            
            show_result(translate_result)
            
        except Exception as e:
            st.error(str(e))
