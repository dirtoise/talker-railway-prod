from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config(os.getenv('SECRET_KEY'))
    SQLALCHEMY_TRACK_MODIFICATIONS = config(os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS'), cast=bool)

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = config(os.getenv(''))
    DEBUG = config(os.getenv('DEBUG'))
    SQLALCHEMY_ECHO = config(os.getenv('SQLALCHEMY_ECHO'))

