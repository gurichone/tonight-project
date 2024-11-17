FROM python:3.10

RUN python -m pip install --upgrade pip

RUN pip install --no-cache-dir Flask

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

ENV FLASK_APP=app:create_app

ENV FLASK_ENV=development

RUN apt update

RUN apt install lsof
