# base image
FROM python:3.12.5-alpine3.20

WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt requirements.txt

# install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy whole project to your docker home directory.
COPY . .

# Migrate the database and start the server.
CMD python ./src/manage.py migrate ; \
    python ./src/manage.py runserver 0.0.0.0:8000
