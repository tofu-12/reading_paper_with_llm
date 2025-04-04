import streamlit as st


class SearchingPaperClient:
    def __init__(self):
        st.set_page_config(page_title="Searching Paper", page_icon="🔍")
    
    def run(self):
        st.title('Searching Paper')


if __name__ == '__main__':
    client = SearchingPaperClient()
    client.run()
