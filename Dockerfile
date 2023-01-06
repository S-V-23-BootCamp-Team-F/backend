FROM python:3.8

ENV PYTHONUNBUFFERED 1

RUN apt-get -y update

RUN mkdir /backend    

COPY . /backend/

WORKDIR /backend

RUN pip install --upgrade pip
RUN pip install -r requirements.txt