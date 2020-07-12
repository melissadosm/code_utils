FROM python:3.7.3-alpine

ENV APP=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR $APP

COPY . $APP

COPY requirements.txt $APP/

RUN apk update && apk upgrade && pip install -U pip
RUN apk add build-base linux-headers
RUN  pip install -r $APP/requirements.txt

ENV PORT 5000
ARG PROJECT


ENV GOOGLE_APPLICATION_CREDENTIALS "/secrets/sa/key.json"

CMD gunicorn -b :$PORT main:app --timeout 600