# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

RUN pip install pipenv 
RUN apt-get update && apt-get install

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

WORKDIR /app

RUN pipenv install --system --ignore-pipfile

COPY . /app

CMD [ "python", "wsgi.py" ]
