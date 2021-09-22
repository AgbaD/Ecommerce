#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

import jwt
from . import api
from datetime import datetime, timedelta
from flask import jsonify, request, current_app
from .utils.auth import token_required, admin_required, merchant_required


@api.route("/index", methods=['GET'])
def index():
    return jsonify({
        'msg': 'You are connected!'
    }), 200



