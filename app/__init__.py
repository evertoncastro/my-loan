from os import getenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from celery import Celery


def setup_app() -> object:
    _app = Flask(__name__)
    _app.config.from_object(
        f"config.{getenv('FLASK_ENV', 'development')}"
    )
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