import os
import sys
sys.path.append(os.pardir)
sys.path.append(os.path.join(os.pardir, os.pardir))

import streamlit as st

from ai_agent.translate import translate_pdf
from ai_agent.schemas import TranslateSchema


def show_result(translate_result: TranslateSchema):
    try:
        st.subheader("論文情報")
        st.text(f'English Title:\n{translate_result.English_Title}')
        st.text(f'タイトル:\n{translate_result.Japanese_Title}')
        st.text(f"発表年度:\n{str(translate_result.Publication_Year)}")
        st.text(f"ジャーナル/カンファレンス:\n{translate_result.Journal_or_Conference}")
        st.text(f"キーワード:\n{', '.join(translate_result.Keywords)}")

        st.subheader("概要")
        st.text(translate_result.Abstract)

        st.subheader("イントロダクション")
        st.text(translate_result.Introduction)

        st.subheader("関連研究")
        st.text(translate_result.Related_Research)

        st.subheader("提案手法")
        st.text(translate_result.Method)

        st.subheader("まとめ")
        st.text(translate_result.Conclusion)
    
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
