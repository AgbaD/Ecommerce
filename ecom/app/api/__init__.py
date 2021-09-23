#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from flask import Blueprint

api = Blueprint('api', __name__)

from . import main, merchant, product, user
