# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

# WORKDIR /dicomframework
ENV TERM=xterm

RUN pip install pipenv 
RUN apt-get update && apt-get install

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY Pipfile .
COPY Pipfile.lock .

RUN pipenv install --deploy

CMD [ "pipenv", "run", "python", "dicomframework"]

COPY . .