FROM python:3.12

WORKDIR /app

COPY ./requirements.txt /app/

RUN pip install -r requirements.txt --no-cache-dir

COPY . /app/

