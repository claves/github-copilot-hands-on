# ベースイメージを指定
FROM python:3.9-slim

# 作業ディレクトリを設定
WORKDIR /app

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# 必要なパッケージをインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY main.py /app/main.py

# Streamlitの設定を行う
RUN mkdir -p ~/.streamlit
RUN bash -c 'echo -e "\
[server]\n\
headless = true\n\
port = 8501\n\
enableCORS = false\n\
" > ~/.streamlit/config.toml'

# ポートを公開
EXPOSE 8501

# コンテナ起動時に実行するコマンドを指定
ENTRYPOINT ["streamlit", "run"]
CMD ["main.py"]