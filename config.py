from decouple import config
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

class Config:
    SECRET_KEY = config(os.getenv("SECRET_KEY"))
    SQLALCHEMY_TRACK_MODIFICATIONS = config(os.getenv("SQLALCHEMY_TRACK_MODIFICATIONS"), cast=bool)

class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_PUBLIC_URL")
    DEBUG = os.getenv("DEBUG")
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO")
