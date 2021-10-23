#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3


from . import api
from flask import jsonify
from ..backend.product import search_product, search_store, search_category
from ..backend.product import get_all_stores, get_all_products_from_store, get_product_reviews
from ..backend.product import get_all_products, get_product, get_all_categories, get_category_products


@api.route('/product/all', methods=['GET'])
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


@api.route('/product/<product_pid>', methods=['GET'])
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


@api.route('/category/all', methods=['GET'])
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


@api.route('/category/<category_name>/products', methods=['GET'])
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


@api.route('/store/all', methods=['GET'])
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


@api.route('/store/<store_id>/products', methods=['GET'])
def fetch_all_products_from_store(store_id):
    try:
        resp = get_all_products_from_store(store_id)
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


@api.route('/product/<product_pid>/reviews', methods=['GET'])
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
        

@api.route('/product/search/<query>', methods=['GET'])
def product_search(query):
    try:
        resp = search_product(query)
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
        

@api.route('/store/search/<query>', methods=['GET'])
def store_search(query):
    try:
        resp = search_store(query)
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
        

@api.route('/category/search/<query>', methods=['GET'])
def category_search(query):
    try:
        resp = search_category(query)
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

