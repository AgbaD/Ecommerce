#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from . import api
from flask import jsonify


@api.route("/index", methods=['GET'])
def index():
    return jsonify({
        'status': 'success',
        'msg': 'You are connected!'
    }), 200

