# reading_paper_with_llm

## 概要
このアプリケーションは論文のPDFを要約し、Notionのデータベースに保存する機能を提供します。
論文のPDFの要約では、Gemini 2.0 flashを使用します。

## 環境構築
1. **リポジトリをクローン**
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **依存パッケージのインストール**
    ```bash
    uv sync
    ```

3. **環境変数の設定**

    以下のコマンドで```.env.sample```をコピーして、```.env```に必要な環境変数を設定する。
    ```bash
    cp .env.example .env
    ```

## アプリケーションの実行

プロジェクトルートで以下のコマンドを実行する。
```bash
bash ./start_app.sh
```