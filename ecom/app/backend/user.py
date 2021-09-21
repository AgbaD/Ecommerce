#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from werkzeug.security import generate_password_hash, check_password_hash

import uuid
from .. import db
from .utils.schema import validate_user
from ..models import User, Product, Feedback


def create_user(data):
    email = data['email']
    fullname = data['fullname']
    password = data['password']
    repeat_password = data['repeat_password']
    phone = data['phone']
    address = data['address']

    info = {
        'email': email,
        'password': password,
        'fullname': fullname,
        'phone': phone,
        'address': address
    }

    if password != repeat_password:
        return {
            'status': 'error',
            'msg': 'Passwords do not match!'
        }

    schema = validate_user(info)
    if schema['msg'] != 'success':
        return {
            'status': 'error',
            'msg': schema['error']
        }

    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'status': 'error',
            'msg': 'Email has already been used'
        }

    password_hash = generate_password_hash(password)
    public_id = str(uuid.uuid4())
    user = User(
        public_id=public_id,
        email=email,
        fullname=fullname,
        phone=phone,
        address=address,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()
    return {
        'status': 'success',
        'msg': "User has been created successfully!"
    }


def login_user(data):
    email = data['email']
    password = data['password']

    # check email using regex

    user = User.query.filter_by(email=email).first()
    if not user:
        return {
            'status': 'error',
            'msg': "User not found"
        }

    if check_password_hash(user.password_hash, password):
        return {
            'status': 'success',
            'data': {
                'public_id': user.public_id
            }
        }
    return {
        'status': 'error',
        'msg': 'Password is incorrect'
    }
