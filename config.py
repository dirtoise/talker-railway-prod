from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = config("SQLALCHEMY_TRACK_MODIFICATIONS", cast=bool)

class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/talker_prod"
    DEBUG = True
    SQLALCHEMY_ECHO = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/talker_prod"
    DEBUG = False
    SQLALCHEMY_ECHO = False

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:password@localhost/testtalker_prod"
    SQLALCHEMY_ECHO = False
    TESTING = True