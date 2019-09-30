import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS= True
    SQLALCHEMY_ECHO = False

class DevelopmentConfig(Config):
    Debug = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')


config = {
    'development' : DevelopmentConfig
}
