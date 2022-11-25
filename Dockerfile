
# syntax=docker/dockerfile:1
FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev build-base linux-headers

WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "djangoApi.wsgi.application"]
CMD gunicorn djangoApi.wsgi:application --bind 0.0.0.0:$PORT


# # pull official base image
# FROM python:3.8.12-alpine3.14

# # set work directory
# WORKDIR ./asset-management-tool

# # set environment variables
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # install psycopg2 dependencies
# RUN apk update \
#     && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libffi-dev cairo-dev pango-dev gdk-pixbuf-dev build-base linux-headers

# # install dependencies
# RUN pip install --upgrade setuptools
# RUN pip install --upgrade pip
# COPY ./requirements.txt .
# RUN pip install -r requirements.txt

# # copy project
# . /code/
# CMD gunicorn djangoApi.wsgi:application --bind 0.0.0.0:$PORT
