import os
from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery

basedir = os.path.abspath(os.path.dirname(__file__))

def setup_app() -> object:
    _app = Flask(__name__)
    _app.config['DEBUG'] = True
    _app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://{username}:{password}@{host}:{port}/{db_name}'.format(
            host='loan-db',
            username='root',
            password='admin',
            port=3306,
            db_name='loan'
        )
    _app.config['RESTPLUS_MASK_HEADER'] = False
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    _app.config['CELERY_BROKER_URL'] = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
    _app.config['CELERY_RESULT_BACKEND'] = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
    _app.config['CELERY_SEND_EVENTS'] = True
    _app.config['LOAN_API_URL'] = 'https://challenge.noverde.name'
    _app.config['LOAN_API_TOKEN'] = 'SnAB7jQEFs1Ai8XtZdssa14gORT3jWPI7TWdXN97'
    if getenv('FLASK_ENV') in ['testing']:
        _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
    elif getenv('FLASK_ENV') in ['development']:
        _app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
        _app.config['CELERY_BROKER_URL'] = 'amqp://rabbitmq:rabbitmq@0.0.0.0:5672/'
        _app.config['CELERY_RESULT_BACKEND'] = 'amqp://rabbitmq:rabbitmq@0.0.0.0:5672/'

    return _app


def setup_database(_app: object) -> SQLAlchemy:
    _db = SQLAlchemy()
    _db.init_app(_app)
    return _db


def setup_database_migration(_app: object, _db: SQLAlchemy) -> Migrate:
    return Migrate(_app, _db)


def make_celery(app):
    celery = Celery(
        'myloan',
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['services.process_loan']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


app = setup_app()
db = setup_database(app)
migrate = setup_database_migration(app, db)
celery = make_celery(app)


@celery.task()
def add_together(a, b):
    print('Everton Teste')
    return a + b