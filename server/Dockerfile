FROM python:3.9.1-buster

RUN mkdir /code
WORKDIR /code

RUN pip install gunicorn

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY app /code/app

WORKDIR /code/app
EXPOSE 8000
CMD gunicorn -w 4 -b 0.0.0.0:8000 app:app

