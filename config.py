#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

import os
from dotenv import load_dotenv

load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY') or "863g4r98fhydg97623vruy08r7wvdo309826gvo827"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # Search Feature
    WHOOSH_BASE = os.path.join(basedir, "search.db")

    MSEARCH_INDEX_NAME = "msearch"
    MSEARCH_BACKEND = "whoosh"
    MSEARCH_PRIMARY_KEY = "id"
    MSEARCH_ENABLE = True

    # username = os.getenv('DB_USERNAME')
    # password = os.getenv('DB_PASSWORD')
    # dbname = os.getenv("DB_NAME")
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or \
    #                           f"postgresql://{username}:{password}@localhost:5432/{dbname}"
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir}/ecom.db"

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True


class Production(Config):

    @classmethod
    def init_app(cls, app):
        Config.init_app(app)

        # log to stderr
        import logging
        from logging import StreamHandler
        file_handler = StreamHandler()
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)


config = {
    'development': Development,
    'production': Production,
    'default': Development
}
