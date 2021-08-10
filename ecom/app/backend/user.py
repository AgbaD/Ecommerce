#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from ..models import User, Product, Feedback
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db


def create_user(data):
    email = data['email']
    fullname = data['fullname']
    password = data['password']
    repeat_password = data['repeat_password']
    phone = data['phone']
    address = data['address']

    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'status': 'error',
            'msg': 'Email has already been used'
        }

    data = {

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
