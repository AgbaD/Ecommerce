#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

import jwt
from functools import wraps
from ...models import User, Admin, Merchant
from flask import request, jsonify, current_app


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({
                'status': 'error',
                'msg': 'Access token is missing!'
            }), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except Exception:
            return jsonify({
                'status': 'error',
                'msg': 'Token is invalid'
            }), 401

        return f(current_user, *args, **kwargs)
    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({
                'status': 'error',
                'msg': 'Access token is missing'
            }), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
            admin = Admin.query.filter_by(public_id=data['public_id']).first()
        except Exception:
            return jsonify({
                'status': 'error',
                'msg': 'Token is invalid'
            }), 401

        return f(admin, *args, **kwargs)
    return decorated


def merchant_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({
                'status': 'error',
                'msg': 'Access token is missing'
            }), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
            admin = Merchant.query.filter_by(public_id=data['public_id']).first()
        except Exception:
            return jsonify({
                'status': 'error',
                'msg': 'Token is invalid'
            }), 401

        return f(admin, *args, **kwargs)
    return decorated

