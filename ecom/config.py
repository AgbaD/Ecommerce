#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or ""
    EMAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
    EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    CACHE_TYPE = "simplecache"
    PAYSTACK_KEY = ""
    PAYPAL_CLIENT_SECRET = ""
    PAYPAL_CLIENT_ID = ""

    @staticmethod
    def init_app(app):
        pass


class Development(Config):
    DEBUG = True


class Production(Config):
    pass


config = {
    "dev": Development,
    "prod": Production,
    "default": Development
}


