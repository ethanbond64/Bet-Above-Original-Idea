import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'heressometext'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass

class Dev1(Config):
    Debug = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'dev-data1.sqlite')

config = {
    'Dev1': Dev1,
    'testing': None,
    'production': None,

    'default': Dev1
}
