#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, make_response, request

import uuid
import json

from . import api


@api.route('/api/v1/login', methods=['POST'])
def login():
    data = request.get_json()

    password = data['password']
    email = data['email']

    return ''


@api.route('/api/v1/register', methods=['POST'])
def register():
    data = request.get_json()

    return jsonify({})

