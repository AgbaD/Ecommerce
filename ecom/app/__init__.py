#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_msearch import Search

from ..config import config

db = SQLAlchemy()
search = Search(db=db)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    search.init_app(app)
    CORS(app)

    return app

