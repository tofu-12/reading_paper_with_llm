# スクリプトがあるディレクトリまで移動
BASE_DIR=$(dirname "$0")
cd "$BASE_DIR" || exit 1

# streamlitの起動
uv run streamlit run frontend/home.py
