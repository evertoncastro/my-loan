FROM python:3.8

ENV FLASK_ENV=staging
ENV PYTHONPATH=$PYTHONPATH:$(pwd)/app
ENV FLASK_APP=app/main.py
ENV FLASK_DEBUG=0

EXPOSE 8080

COPY app/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt && apt-get update && apt-get install -y mariadb-client

COPY . /app

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]