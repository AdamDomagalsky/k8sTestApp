FROM python:3.8-slim as demo-api

RUN mkdir -p /usr/src/app/.metrics

WORKDIR /usr/src/app

ADD main.py requirements.txt /usr/src/app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD python main.py
