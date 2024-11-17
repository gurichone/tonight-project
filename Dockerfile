FROM python:3.10

RUN python -m pip install --upgrade pip

WORKDIR /app

# requirements.txtを先にコピーして、依存関係をインストール
COPY requirements.txt /app/

# requirements.txtから依存関係をインストール
RUN pip install -r requirements.txt

# 残りのファイルをコピー
COPY . /app/

# lsofのインストール
RUN apt update && apt install -y lsof

ENV FLASK_APP=app:create_app
ENV FLASK_ENV=development

CMD ["flask", "run", "--host=0.0.0.0", "--port=5001"]
