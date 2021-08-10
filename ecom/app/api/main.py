#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from flask import jsonify, request, current_app
from . import api
import jwt
from datetime import datetime, timedelta
from ..backend.user import login_user, create_user
from .utils.auth import token_required, admin_required, merchant_required


@api.route("/index", methods=['GET'])
def index():
    return jsonify({
        'msg': 'You are connected!'
    }), 200


@api.route('/user/login', methods=['POST'])
def user_login():
    try:
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

    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 400


@api.route('/user/register', methods=['POST'])
def user_register():
    data = request.get_json()

    email = data['email']
    fullname = data['fullname']
    password = data['password']
    repeat_password = data['repeat_password']
    phone = data['phone']
    address = data['address']

    info = {
        'email': email,
        'password': password,
        'repeat_password': repeat_password,
        'fullname': fullname,
        'phone': phone,
        'address': address
    }

    resp = create_user(info)
    if resp['status'] != 'success':
        return jsonify({
            'status': 'error',
            'msg': resp['msg']
        }), 400

    return jsonify({
        'status': 'success',
        'msg': "user has been created successfully!"
    })
