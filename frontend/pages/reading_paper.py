import streamlit as st


class ReadingPaperClient:
    def __init__(self):
        st.set_page_config(page_title="Reading Paper with LLM", page_icon="📃")

    def run(self):
        """
        streamlitを実行
        """
        st.title('Reading Paper with LLM')

        st.subheader('How to use')
        how_to_use = """
1. 要約する論文のPDFファイルをアップロードしてください
2. 論文の使用言語を入力してください
"""
        st.markdown(how_to_use)

        st.subheader('Upload Data')
        file = st.file_uploader('PDFファイルをアップロードしてください', type=['pdf'])
        language = st.text_input('使用言語を入力してください')
        is_runnig = st.button('Run')

        if is_runnig:
            if file is None or language == '':
                st.error('PDFファイルまたは使用言語が入力されていません')
            else:
                pdf_data = self._deal_pdf(file)
                st.success('Success message')
        
        st.subheader('Result')

    def _deal_pdf(self, file):
        """
        fileを受け取り、fileを解析

        Args:
            file: 解析するpdfファイル
        """
        pdf_data = file.getvalue()
        return pdf_data



if __name__ == '__main__':
    client = ReadingPaperClient()
    client.run()