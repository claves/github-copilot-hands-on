# Dockerのインストール
## Windowsの場合
1. [Docker Desktop for Windows](https://docs.docker.com/desktop/install/windows-install/)をダウンロードしてインストール
2. インストール後、Docker Desktopを起動

## Macの場合
1. [Docker Desktop for Mac](https://docs.docker.com/desktop/install/mac-install/)をダウンロードしてインストール
2. インストール後、Docker Desktopを起動

## Linuxの場合
1. [Docker Desktop for Linux](https://docs.docker.com/desktop/setup/install/linux/)をダウンロード
2. インストール後、Docker Desktopを起動


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
docker run -it -p 8501:8501 -v $(pwd):/app --entrypoint /bin/bash weather-app
```
4. コンテナ内でstreamlitをインストールする
```
pip install streamlit
```
5. streamlitを使ってアプリケーションを実行
```
streamlit run main.py
```