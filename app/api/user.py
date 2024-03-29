#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3


import jwt
from . import api
from .utils.auth import token_required
from datetime import datetime, timedelta
from flask import jsonify, request, current_app
from ..backend.user import add_to_cart, product_review, store_feedback, remove_from_cart
from ..backend.user import login_user, create_user, activate_user, deactivate_user, delete_user, get_cart


# User


@api.route('/user/register', methods=['POST'])
def user_register():
    try:
        data = request.get_json()

        email = data['email'].lower()
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
            'msg': "User has been created successfully!"
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/user/deactivate', methods=['PUT'])
@token_required
def user_deactivate(current_user):
    try:
        user_id = current_user.id
        resp = deactivate_user(user_id)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'msg': resp['msg']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/user/activate', methods=['POST'])
def user_activate():
    try:
        data = request.get_json()

        email = data['email'].lower()
        password = data['password']

        info = {
            'email': email,
            'password': password
        }

        resp = activate_user(info)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'msg': resp['msg']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/user/delete', methods=['DELETE'])
@token_required
def user_delete(current_user):
    try:
        user_id = current_user.id
        resp = delete_user(user_id)

        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'msg': resp['msg']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


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
            'exp': datetime.utcnow() + timedelta(minutes=30)
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
        }), 500


@api.route('/user/cart/add/<product_pid>', methods=['PUT'])
@token_required
def add_product_to_cart(current_user, product_pid):
    try:
        user_pid = current_user.public_id
        resp = add_to_cart(user_pid, product_pid)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'msg': resp['msg']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/user/cart/remove/<product_pid>', methods=['PUT'])
@token_required
def remove_product_from_cart(current_user, product_pid):
    try:
        user_pid = current_user.public_id
        resp = remove_from_cart(user_pid, product_pid)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'msg': resp["msg"]
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/user/cart', methods=['GET'])
@token_required
def fetch_cart(current_user):
    try:
        user_pid = current_user.public_id
        resp = get_cart(user_pid)
        if resp['status'] != 'success':
            return jsonify({
                'status': resp['status'],
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': resp['status'],
            'data': resp['data']['cart']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/user/product/<product_pid>/review', methods=['POST'])
@token_required
def review_product(current_user, product_pid):
    try:
        data = request.get_json()
        review = data['review']

        user_pid = current_user.public_id
        resp = product_review(user_pid, product_pid, review)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'msg': resp["msg"]
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/user/feedback/<store_pid>', methods=['POST'])
@token_required
def feedback_store(current_user, store_pid):
    try:
        data = request.get_json()
        feedback = data['feedback']

        user_pid = current_user.public_id
        resp = store_feedback(user_pid, store_pid, feedback)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'msg': resp['msg']
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500
