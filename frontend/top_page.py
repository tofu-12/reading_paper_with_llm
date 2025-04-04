import streamlit as st

from pages.reading_paper import ReadingPaperClient
from pages.searching_paper import SearchingPaperClient


class TopPageClient:
    def __init__(self):
        st.set_page_config(page_title="top page", page_icon="")
    
    def run(self):
        st.title('Top Page')
        st.button('Reading Paper with LLM', on_click=self._change_to_reading_paper)
        st.button('Searching Paper', on_click=self._change_to_searching_paper)
    
    def _change_to_reading_paper(self):
        client = ReadingPaperClient()
        client.run()
    
    def _change_to_searching_paper(self):
        client = SearchingPaperClient()
        client.run()


if __name__ == 'main':
    client = TopPageClient()
    client.run()
