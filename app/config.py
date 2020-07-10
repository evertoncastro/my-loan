import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    Debug = True
    RESTPLUS_MASK_HEADER = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@0.0.0.0:5672/'
    CELERY_RESULT_BACKEND = 'amqp://rabbitmq:rabbitmq@0.0.0.0:5672/'


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')


development = DevelopmentConfig()
testing = TestingConfig()
