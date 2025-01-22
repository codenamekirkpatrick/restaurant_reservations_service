FROM python:3.12-slim-buster

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

