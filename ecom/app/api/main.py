#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from flask import jsonify, request
from . import api
import jwt
from ..backend.user import login_user


@api.route("/index", methods=['GET'])
def index():
    return jsonify({
        'msg': 'You are connected!'
    }), 200


@api.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()

        email = data['email']
        password = data['password']

        info = {
            'email': email,
            'password': password
        }

        resp = login_user(info)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400

        pid = resp['data']['public_id']

    return jsonify({
        'status': 'error',
        'msg': f"Endpoint doesnt support {request.method} requests"
    }), 400
