#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3


import jwt
from . import api
from datetime import datetime, timedelta
from flask import jsonify, request, current_app
from .utils.auth import token_required, admin_required, merchant_required
from ..backend.product import get_all_stores, get_all_products_from_store, get_product_reviews
from ..backend.product import get_all_products, get_product, get_all_categories, get_category_products


@api.route('/get_all_products', methods=['GET'])
def fetch_all_products():
    try:
        resp = get_all_products()
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'data': resp['data']['products']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/get_product/<product_pid>', methods=['GET'])
def fetch_product(product_pid):
    try:
        resp = get_product(product_pid)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'data': resp['data']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/get_all_categories', methods=['GET'])
def fetch_all_categories():
    try:
        resp = get_all_categories()
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'data': resp['data']['categories']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/get_category_products/<category_name>', methods=['GET'])
def fetch_category_products(category_name):
    try:
        resp = get_category_products(category_name)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'data': resp['data']['products']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/get_all_stores', methods=[GET])
def fetch_all_stores():
    try:
        resp = get_all_stores()
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'data': resp['data']['stores']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/get_all_products_from_store/<store_pid>', methods=['GET'])
def fetch_all_products_from_store(store_pid):
    try:
        resp = get_all_products_from_store(store_pid)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'data': resp['data']['products']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500


@api.route('/get_product_reviews/<product_pid>', methods=['GET'])
def fetch_product_reviews(product_pid):
    try:
        resp = get_product_reviews(product_pid)
        if resp['status'] != 'success':
            return jsonify({
                'status': 'error',
                'msg': resp['msg']
            }), 400
        return jsonify({
            'status': 'success',
            'data': resp['data']['reviews']
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error',
            'msg': e
        }), 500

