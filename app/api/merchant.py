#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3


import jwt
from . import api
from datetime import datetime, timedelta
from .utils.auth import merchant_required
from flask import jsonify, request, current_app
from ..backend.merchant import get_all_feedback, delete_merchant, deactivate_merchant
from ..backend.merchant import create_merchant, create_store, add_merchant_id, login_merchant
from ..backend.merchant import activate_merchant, create_product, update_product, delete_product


# Merchant


@api.route("/merchant/register", methods=['POST'])
def merchant_register():
    try:
        data = request.get_json()

        f_name = data['firstname']
        l_name = data['lastname']
        email = data['email'].lower()
        phone = data['phone']
        password = data['password']
        repeat_password = data['repeat_password']
        store_name = data['store_name']
        store_description = data['store_description']
        store_tags = data['store_tags']

        info_merchant = {
            'firstname': f_name,
            'lastname': l_name,
            'email': email,
            'phone': phone,
            'password': password,
            'repeat_password': repeat_password
        }

        info_store = {
            'name': store_name,
            'description': store_description,
            'tags': store_tags
        }

        store = create_store(info_store)
        if store['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': store['msg']
            }), 400

        store = store['data']['store']
        store_id = store.id
        info_merchant['store_id'] = store_id
        store_pid = store.public_id

        resp = create_merchant(info_merchant)
        if resp['status'] != 'success':
            print(resp['msg'])
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400

        merchant = resp['data']['merchant']
        merchant_id = merchant.id

        resp = add_merchant_id(store_pid, merchant_id)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400

        return jsonify({
            'status': 'success',
            'msg': 'Store and merchant accounts created successfully!'
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route("/merchant/deactivate", methods=['PUT'])
@merchant_required
def merchant_deactivate(merchant):
    try:
        merchant_pid = merchant.public_id
        resp = deactivate_merchant(merchant_pid)
        if resp['status'] != "success":
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


@api.route("/merchant/activate", methods=['POST'])
def merchant_activate():
    try:
        data = request.get_json()
        email = data['email'].lower()
        password = data['password']

        info = {
            'email': email,
            'password': password
        }
        resp = activate_merchant(info)

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


@api.route('/merchant/delete', methods=['DELETE'])
@merchant_required
def merchant_delete(merchant):
    try:
        merchant_id = merchant.id
        resp = delete_merchant(merchant_id)
        if resp['status'] != 'success':
            return jsonify({
                'status': "error",
                'msg': resp['msg']
            }), 400
        return jsonify({
            "status": 'success',
            'msg': "Merchant deleted successfully"
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route("/merchant/login", methods=['POST'])
def merchant_login():
    try:
        data = request.get_json()

        email = data['email'].lower()
        password = data['password']

        info = {
            'email': email,
            'password': password
        }

        resp = login_merchant(info)

        if resp['status'] != 'success':
            return jsonify({
                'status': "error",
                'msg': resp['msg']
            }), 400

        pid = resp['data']['public_id']
        token = jwt.encode({
            'public_id': pid,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, current_app.config['SECRET_KEY'], "HS256")

        return jsonify({
            'status': 'success',
            'msg': 'Merchant login successfully',
            'data': {
                'token': token
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route("/merchant/product/create", methods=['POST'])
@merchant_required
def add_product(merchant):
    try:
        data = request.get_json()

        name = data['name']
        description = data['description']
        price = data['price']
        denomination = data['denomination']
        category = data['category']
        tags = data['tags']

        merchant_id = merchant.id

        prod = {
            'name': name,
            'description': description,
            'price': price,
            'denomination': denomination,
            'category': category,
            'tags': tags
        }

        resp = create_product(merchant_id, prod)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400

        return jsonify({
            "status": 'success',
            'msg': 'Product successfully created'
        }), 201
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/merchant/product/<product_pid>/update', methods=['POST'])
@merchant_required
def edit_product(merchant, product_pid):
    try:
        data = request.get_json()
        info = {}

        merchant_id = merchant.id
        
        if data['name']:
            info['name'] = data['name']
        if data['description']:
            info['description'] = data['description']
        if data['price']:
            info['price'] = data['price']
        if data['denomination']:
            info['denomination'] = data['denomination']
        if data['category']:
            info['category'] = data['category']
        if data['tags']:
            info['tags'] = data['tags']

        resp = update_product(merchant_id, product_pid, info)
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


@api.route('/merchant/product/<product_pid>/delete', methods=['DELETE'])
@merchant_required
def product_delete(merchant, product_pid):
    try:
        merchant_id = merchant.id
        resp = delete_product(product_pid, merchant_id)
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


@api.route('/merchant/feedback', methods=['GET'])
@merchant_required
def merchant_feedback(merchant):
    try:
        merchant_id = merchant.id
        resp = get_all_feedback(merchant_id)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'data': resp['data']['feedback']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500
