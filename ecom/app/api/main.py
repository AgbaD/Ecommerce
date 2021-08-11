#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from flask import jsonify, request, current_app
from . import api
import jwt
from ..backend.misc import get_product
from datetime import datetime, timedelta
from ..backend.user import login_user, create_user
from .utils.auth import token_required, admin_required, merchant_required
from ..backend.merchant import create_merchant, create_store, add_merchant_id
from ..backend.merchant import login_merchant, create_product


@api.route("/index", methods=['GET'])
def index():
    return jsonify({
        'msg': 'You are connected!'
    }), 200


# User


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
            'exp': datetime.utcnow() + timedelta(minutes=90)
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
        }), 400


@api.route('/user/register', methods=['POST'])
def user_register():
    try:
        data = request.get_json()

        email = data['email']
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
            'msg': "user has been created successfully!"
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 400


# Merchant


@api.route("/merchant/register", methods=['POST'])
def merchant_register():
    data = request.get_json()

    f_name = data['firstname']
    l_name = data['lastname']
    email = data['email']
    phone = data['phone']
    password = data['password']
    repeat_password = data['repeat_password']
    store_name = data['store_name']
    store_description = data['store_description']
    store_tags = data['store_tags']

    info_merchant = {
        'f_name': f_name,
        'l_name': l_name,
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


@api.route("/merchant/login", methods=['POST'])
def merchant_login():
    try:
        data = request.get_json()

        email = data['email']
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
            'exp': datetime.utcnow() + timedelta(minutes=90)
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
        }), 400


@api.route("/merchant/create_product", methods=['POST'])
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
            'merchant_id': merchant_id,
            'name': name,
            'description': description,
            'price': price,
            'denomination': denomination,
            'category': category,
            'tags': tags
        }

        resp = create_product(prod)
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
        }), 400


@api.route('/merchant/update_product/<product_pid>', methods=['POST'])
def edit_product(product_pid):
    data = request.get_json()

    name = data['name']
    description = data['description']
    price = data['price']
    denomination = data['denomination']
    category = data['category']
    tags = data['tags']

    k_keys = [name, description, price, denomination, category, tags]
    keys = [i for i in k_keys if i]
    i = 0
    product = {}
    while i < len(keys):
        product[i] = {}


@api.route('/get/product/<product_pid>', methods=['GET'])
def fetch_product(product_pid):
    try:
        product = get_product({'product_pid': product_pid})

        if product['status'] == 'success':
            return jsonify({
                'status': 'success',
                'data': {
                    'product': product['data']
                }
            }), 200
        return jsonify({
            'status': 'error',
            'msg': product['msg']
        }), 400
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 400
