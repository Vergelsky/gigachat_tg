FROM python:3.12-slim

WORKDIR /code

COPY . .

RUN pip install -r requirements.txt

RUN python main.py