#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, make_response, redirect

import uuid
import json

from . import api
from .. import mysql


@api.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()

    password = data['password']
    email = data['email']

    return ''


@api.route('/api/v1/register', methods=['POST'])
def register():
    if request.method == ['POST']:
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
                    'status': 'error', 'status_code': 400, 'message': 'Passwords do not match'
                })

            password_hash = generate_password_hash(password)
            public_id = str(uuid.uuid4())

            cur = mysql.connection.cursor()
            cur.execute(
                "INSERT INTO users (public_id, firstname, lastname, email, password_hash, phone, address) VALUES (%s, "
                "%s, %s, %s, %s, %s, %s)", (public_id, first_name, last_name, email, password_hash, phone, address)
            )
            mysql.connection.commit()

            return jsonify({
                'status': 'success', 'status_code': 200, 'message': 'User created successfully'
            })
        except Exception as e:
            return jsonify({
                'status': 'error', 'status_code': 500, 'message': e
            })

    else:
        return jsonify({
            'status': 'error', 'status_code': 400, 'message': "Endpoint doesn't support GET requests"
        })

