import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db', 'psqi.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = '76a2f5884803b6ada4fa2be67cbbdfe6'