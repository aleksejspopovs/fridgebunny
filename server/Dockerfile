FROM python:3.9.1-buster

RUN mkdir /code
WORKDIR /code

RUN pip install gunicorn

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY app /code/app

ENV PORT 8000
EXPOSE $PORT
CMD gunicorn --workers 1 --threads 8 --bind :$PORT app.app:app

