FROM python:3.7
MAINTAINER Carlos Ávila


# Start Installing the Basic Dependencies
RUN pip install --upgrade pip
RUN pip install gunicorn


RUN mkdir -p /sanic/config
RUN mkdir -p /sanic/opi_dragon_api

COPY config/* /sanic/config/
COPY opi_dragon_api/ /sanic/opi_dragon_api/
COPY requirements.txt /sanic
RUN pip install -r sanic/requirements.txt
COPY run.py /sanic/run.py
COPY .env /sanic/.env

WORKDIR /sanic
RUN find . -type f

ENV SANIC_SERVER_PORT 8000
ENV SANIC_SERVER_HOST 0.0.0.0

EXPOSE 8000


ENTRYPOINT ["gunicorn", "run:app", "--config", "/sanic/config/gunicorn.conf", "--log-config", "/sanic/config/logging.conf", "-b", "0.0.0.0:8000", "--worker-class",  "sanic.worker.GunicornWorker"]

