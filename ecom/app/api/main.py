#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from flask import jsonify
from . import api


@api.route("/index", methods=['GET'])
def index():
    return jsonify()
