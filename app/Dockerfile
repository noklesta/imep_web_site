# pull official base image
FROM python:3.7-alpine as base

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
RUN apk update \
    && apk add --virtual build-deps gcc python3-dev musl-dev \
    && apk add postgresql-dev \
    && pip install psycopg2 \
    #&& pip install psycopg2-binary \
    && apk del build-deps

# install dependencies
RUN pip install --upgrade pip
RUN pip install pipenv==2018.10.9
COPY ./Pipfile /usr/src/app/Pipfile
RUN pipenv install --skip-lock --system


# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh

# copy project
COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
CMD ["gunicorn", "cdhlab.wsgi:application", "--bind", "0.0.0.0:8000"]
