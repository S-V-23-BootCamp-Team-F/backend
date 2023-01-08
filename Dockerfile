# backend/Dockerfile
# set base image
FROM python:3.8

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# set work directory
WORKDIR /backend

# Copy project
COPY . ./

# install dependencies
RUN python3 -m pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# Expose application port
EXPOSE 8000
