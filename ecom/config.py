#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Search Feature
    WHOOSH_BASE = os.path.join(basedir, "search.db")

    MSEARCH_INDEX_NAME = "msearch"
    MSEARCH_BACKEND = "whoosh"
    MSEARCH_PRIMARY_KEY = "id"
    MSEARCH_ENABLE = True

    username = os.getenv('DB_USERNAME')
    password = os.getenv('DB_PASSWORD')
    dbname = os.getenv("DB_NAME")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
                              f"mysql+mysqlconnector://{username}:{password}@localhost/{dbname}"

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True


class Production(Config):
    pass


config = {
    'development': Development,
    'production': Production,
    'default': Development
}
