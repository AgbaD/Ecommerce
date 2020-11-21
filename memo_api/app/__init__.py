#!/usr/bin/python3
# Author:   @AgbaD | @agba_dr3

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .utils.keygen import gen_key
import os

db = SQLAlchemy()
cors = CORS()

secret_key = gen_key(33)
basedir = os.path.abspath(os.path.dirname(__file__))


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secret_key
    app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///' + os.path.join(basedir, 'data.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    cors.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app

