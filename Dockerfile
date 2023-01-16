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
RUN apt-get update && apt-get install libgl1 -y
# install dependencies
RUN python3 -m pip install --upgrade pip setuptools
RUN pip install -r requirements.txt

# django를 단독으로 실행할 때 사용 명령어
# nginx를 이용해서 django를 실행할때는 주석처리!!
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]

# Expose application port
EXPOSE 8000
