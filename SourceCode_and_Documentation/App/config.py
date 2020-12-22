import os

class Config:

    dir = os.path.abspath(os.path.dirname(__file__))
    SECRET_KEY = '83?-14!*d8fa'
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(dir, 'database.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
