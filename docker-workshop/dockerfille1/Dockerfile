FROM ubuntu:18.04

RUN apt-get update
RUN apt-get --assume-yes install python3.6
RUN apt-get --assume-yes update && apt-get --assume-yes upgrade
RUN apt-get  --assume-yes install python3-pip


ENV APP=/app
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR $APP

COPY . $APP

COPY requirements.txt $APP/


RUN  pip3 install -r $APP/requirements.txt

ENV PORT 5000
ARG PROJECT


CMD gunicorn -b :$PORT main:app --timeout 600
