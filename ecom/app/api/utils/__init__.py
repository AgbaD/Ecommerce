#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from functools import wraps
from flask import jsonify, request, current_app

from ... import mysql


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({
                'status': 'error', 'message': 'Token is missing!'
            }), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            cur = mysql.connection.cursor()
            cur.execute(
                'SELECT * FROM users WHERE public_id={}'.format(data['public_id'])
            )

            current_user = cur.fetchone()
            cur.close()
        except Exception as e:
            return jsonify({
                'status': 'error', 'message': 'Token is invalid!'
            }), 401

        return f(current_user, *args, **kwargs)
    return decorated
