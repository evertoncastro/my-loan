import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    Debug = True
    RESTPLUS_MASK_HEADER = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')


class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')


development = DevelopmentConfig()
testing = TestingConfig()
