# Dockerでの環境構築
1. Dockerfile から独自のイメージをビルドする
```
docker build -t weather-app .
```
2. イメージからコンテナを起動
```
docker run -p 8501:8501 weather-app
```
3. streamlitがインストールされていないエラーが出るため、コンテナをシェルモードで起動する
```
docker run -it -p 8501:8501 --entrypoint /bin/bash weather-app
```
4. コンテナ内でstreamlitをインストールする
```
pip install streamlit
```
5. streamlitを使ってアプリケーションを実行
```
streamlit run main.py
```