FROM python:3.8-alpine3.13
LABEL maintainer="viniderp@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
  /py/bin/pip install --upgrade pip && \
  apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
      build-base postgresql-dev musl-dev && \
  /py/bin/pip install -r /tmp/requirements.txt && \
  /py/bin/pip install -r /tmp/requirements.dev.txt && \
  apk del .tmp-build-deps && \
  rm -rf /tmp

ENV PATH="/py/bin:$PATH"
