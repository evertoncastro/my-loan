import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    Debug = True
    RESTPLUS_MASK_HEADER = False


class DevelopmentConfig(Config):
    ...


class TestingConfig(Config):
    ...


development = DevelopmentConfig()
testing = TestingConfig()