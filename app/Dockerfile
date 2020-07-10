FROM python:3.7

ENV FLASK_ENV=development
ENV PYTHONPATH=$PYTHONPATH:$(pwd)/app
ENV FLASK_APP=app/main.py
ENV FLASK_DEBUG=0

# Refers to gunicorn WSGI port (Gunicorn will map each request in this port to Flask on 5000, See file src/main.py)
EXPOSE 8080

COPY app/requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT ["/bin/sh", "entrypoint.sh"]