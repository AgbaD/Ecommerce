#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, current_app
import jwt

import uuid
from datetime import datetime, timedelta

from . import api
from .. import mysql
from .utils import token_required
from .utils.schema import validate_login, validate_reg


@api.route('/api/login', methods=['POST'])
def login():
    if request.method == "POST":
        try:
            data = request.get_json()

            password = data['password']
            email = data['email']

            data = {
                'email': email,
                'password': password
            }

            schema = validate_login(data)
            if schema['msg'] != "success":
                return jsonify({
                    'status': 'error',
                    'message': schema['error']
                }), 400

            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM users WHERE email={}".format(email)
            )

            user = cur.fetchone()
            cur.close()
            if not user:
                return jsonify({
                    'status': 'error',
                    'message': 'User not found'
                }), 401

            if not check_password_hash(user['password_hash'], password):
                return jsonify({
                    'status': 'error',
                    'message': 'Password is incorrect'
                }), 401

            token = jwt.encode({
                'public_id': user['public_id'], 'exp': datetime.utcnow() + timedelta(minutes=30)
            }, current_app.config['SECRET_KEY'])

            return jsonify({
                'status': 'success',
                'message': 'Login successful',
                'data': {
                    'token': token.decode('UTF-8')
                }
            }), 200
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': e
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': f"Endpoint doesn't support {request.method} requests"
        }), 400


@api.route('/api/register', methods=['POST'])
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
                    'status': 'error',
                    'message': 'Passwords do not match'
                }), 400

            data = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'password': password,
                'phone': phone,
                'address': address
            }

            schema = validate_reg(data)
            if schema['msg'] != 'success':
                return jsonify({
                    'status': 'error',
                    'message': schema['error']
                }), 400

            cur = mysql.connection.cursor()
            user = None
            try:
                cur.execute(
                    f"SELECT * FROM users WHERE email={email}"
                )
                user = cur.fetchone()
            except Exception as e:
                print(e)

            cur.close()
            if user:
                return jsonify({
                    'status': 'error',
                    'message': 'Email has ben used!'
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
                'status': 'success',
                'message': 'User created successfully'
            }), 201
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': e
            }), 500

    else:
        return jsonify({
            'status': 'error',
            'message': f"Endpoint doesn't support {request.method} requests"
        }), 400


@api.route("/api/get_profile", methods=['GET'])
@token_required
def get_profile(current_user):
    if request.method == 'GET':
        try:
            data = {
                'email': current_user['email'],
                'first_name': current_user['first_name'],
                'last_name': current_user['last_name'],
                'phone': current_user['phone'],
                'address': current_user['address'],
                'public_id': current_user['public_id']
            }
            return jsonify({
                'status': 'success',
                'data': {
                    'user': data
                }
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': e
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': f"Endpoint doesn't support {request.method} requests"
        }), 400


@api.route("/api/update_password", methods=['PUT', 'POST'])
@token_required
def update_password(current_user):
    if request.method == 'PUT' or request.method == 'POST':
        try:
            data = request.get_json()

            password = data['password']
            repeat_password = data['repeat_password']

            if password != repeat_password:
                return jsonify({
                    'status': 'error',
                    'message': 'Passwords do not match!'
                }), 400

            password_hash = generate_password_hash(password)

            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE users SET password_hash=%s WHERE email=%s",
                (password_hash, current_user['email'])
            )
            mysql.connection.commit()

            return jsonify({
                'status': 'success',
                'message': 'User updated successfully'
            }), 201
        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': e
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': f"Endpoint doesn't support {request.method} requests"
        }), 400


@api.route("/api/update_profile", methods=['PUT', 'POST'])
@token_required
def update_profile(current_user):
    if request.method == 'PUT' or request.method == 'POST':
        pass
    else:
        return jsonify({
            'status': 'error',
            'message': f"Endpoint doesn't support {request.method} requests"
        }), 400


@api.route("/api/delete_user", methods=['DELETE'])
@token_required
def delete_user(current_user):
    if request.method == 'DELETE':
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "UPDATE users SET is_active={} WHERE email=%s",
                (False, current_user['email'])
            )
            mysql.connection.commit()
            return jsonify({
                'status': 'success',
                'message': 'User deleted successfully'
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': e
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': f"Endpoint doesn't support {request.method} requests"
        }), 400


@api.route("/api/forgot_password", methods=['POST'])
@token_required
def forgot_password(current_user):
    if request.method == 'POST':
        pass
    else:
        return jsonify({
            'status': 'error',
            'message': f"Endpoint doesn't support {request.method} requests"
        }), 400
