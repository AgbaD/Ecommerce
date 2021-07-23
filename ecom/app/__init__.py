#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from flask import Flask
from flask_cors import CORS
from flask_caching import Cache
from config import config
from flask_msearch import Search
from flask_mysqldb import MySQL
from flask_sslify import SSLify

cache = Cache()
search = Search()
mysql = MySQL()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    if not app.debug or not app.testing and not app.config["SSL_DISABLE"]:
        sslify = SSLify(app)

    cache.init_app(app)
    search.init_app(app)
    mysql.init_app(app)
    CORS(app)

    from .api import api
    app.register_blueprint(api)

    return app
