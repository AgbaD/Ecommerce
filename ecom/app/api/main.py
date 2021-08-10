#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from flask import jsonify, request, current_app
from . import api
import jwt
from ..backend.user import login_user
from .utils.auth import token_required
from datetime import datetime, timedelta


@api.route("/index", methods=['GET'])
def index():
    return jsonify({
        'msg': 'You are connected!'
    }), 200


@api.route('/user/login', methods=['POST'])
def user_login():
    if request.method == 'POST':
        data = request.get_json()

        email = data['email'].lower()
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
        token = jwt.encode({
            'public_id': pid,
            'exp': datetime.utcnow() + timedelta(minutes=90)
        }, current_app.config['SECRET_KEY'], "HS256")

        return jsonify({
            'status': 'success',
            'msg': 'User login successful',
            'data': {
                'token': token
            }
        }), 200

    return jsonify({
        'status': 'error',
        'msg': f"Endpoint doesnt support {request.method} requests"
    }), 400


@api.route('/user/register', methods=['POST'])
def user_register():
    data = request.get_json()
