#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, current_app
import jwt

import uuid
from functools import wraps
from datetime import datetime, timedelta

from . import api
from .. import mysql


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
        except Exception as e:
            return jsonify({
                'status': 'error', 'message': 'Token is invalid!'
            }), 401

        return f(current_user, *args, **kwargs)
    return decorated


@api.route('/api/v1/login', methods=['POST'])
def login():
    if request.method == "POST":
        try:
            data = request.get_json()

            password = data['password']
            email = data['email']

            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM users WHERE email={}".format(email)
            )

            user = cur.fetchone()
            if not user:
                return jsonify({
                    'status': 'error', 'message': 'User not found'
                }), 401
            cur.close()

            if not check_password_hash(user.password_hash, password):
                return jsonify({
                    'status': 'error', 'message': 'Password is incorrect'
                }), 401

            token = jwt.encode({
                'public_id': user.public_id, 'exp': datetime.utcnow() + timedelta(minutes=90)
            }, current_app.config['SECRET_KEY'])

            return jsonify({
                'status': 'success', 'message': 'Login successful',
                'data': {
                    'token': token.decode('UTF-8')
                }
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error', 'message': e
            }), 500
    else:
        return jsonify({
            'status': 'error', 'message': "Endpoint doesn't support GET requests"
        }), 400


@api.route('/api/v1/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()

            first_name = data['first_name']
            last_name = data['last_name']
            email = data['email']
            password = data['password']
            re_password = data['re_password']
            phone = str(data['phone'])
            address = data["address"]

            if password != re_password:
                return jsonify({
                    'status': 'error', 'message': 'Passwords do not match'
                }), 400

            cur = mysql.connection.cursor()
            user = None
            try:
                cur.execute(
                    "SELECT * FROM users WHERE email={}".format(email)
                )
                user = cur.fetchone()
            except Exception as e:
                print(e)

            cur.close()
            if user:
                return jsonify({
                    'status': 'error', 'message': 'Email has ben used!'
                }), 400

            password_hash = generate_password_hash(password)
            public_id = str(uuid.uuid4())

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (public_id, firstname, lastname, email, password_hash, phone, address) VALUES (%s, "
                "%s, %s, %s, %s, %s, %s)", (public_id, first_name, last_name, email, password_hash, phone, address)
            )
            mysql.connection.commit()

            return jsonify({
                'status': 'success', 'message': 'User created successfully'
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error', 'message': e
            }), 500

    else:
        return jsonify({
            'status': 'error', 'message': "Endpoint doesn't support GET requests"
        }), 400

