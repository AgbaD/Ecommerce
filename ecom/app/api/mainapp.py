#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from flask import jsonify, request, current_app

from . import api
from .utils import token_required
from .. import mysql, cache

from datetime import datetime


@api.route('/api/home', methods=['GET'])
@cache.cached(timeout=300)
def home():
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                'SELECT DISTINCT category FROM products'
            )
            data = cur.fetchall()
            if not data:
                return jsonify({
                    'status': 'error',
                    'message': 'Internal server error'
                }), 500

            categories = [i for i in data]

            cur.execute(
                'SELECT * FROM products'
            )
            data = cur.fetchall()
            cur.close()
            if not data:
                return jsonify({
                    'status': 'error',
                    'message': 'Internal server error'
                }), 500
            now = datetime.utcnow()

            latest = {}
            for prod in data:
                if len(latest) < 7:
                    img = None  # prod img
                    product = [prod['name'], prod['description'], img, prod['datetime'],
                               prod['price'], prod['category']]
                    latest[prod['id']] = product
                else:
                    arrival_time = prod['datetime']
                    time_diff = now - arrival_time

                    for k, v in latest.items():
                        if (now - v[3]) > time_diff:
                            latest.pop(k)

                            img = None  # prod img
                            product = [prod['name'], prod['description'], img, prod['datetime'],
                                       prod['price'], prod['category']]
                            latest[prod['id']] = product
                            break

            return jsonify({
                'status': 'success',
                'data': {
                    'categories': categories,
                    'latest': latest
                }
            }), 200

        except Exception as e:
            return jsonify({
                'status': 'error',
                'message': f'Internal server error ({e})'
            }), 500
    else:
        return jsonify({
            'status': 'error',
            'message': f"Endpoint doesn't support {request.method} requests"
        }), 400


@api.route('/api/get_all_products', methods=['GET'])
@cache.cached(timeout=900)
def get_all_products():
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                'SELECT * FROM products'
            )
            data = cur.fetchall()
            cur.close()
            if not data:
                return jsonify({
                    'status': 'error',
                    'message': 'Internal server error'
                }), 500

            products = {}
            for prod in data:
                img = None  # prod img
                product = [prod['name'], prod['description'], img, prod['datetime'],
                           prod['price'], prod['category']]
                products[prod['id']]: product

            return jsonify({
                'status': 'success',
                'data': {
                    'products': products
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


@api.route('/api/get_category/<str:category_name>', methods=['GET'])
@cache.cached(timeout=300)
def get_category(category_name):
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                f'SELECT * FROM products WHERE category={category_name}'
            )
            data = cur.fetchall()
            cur.close()
            if not data:
                return jsonify({
                    'status': 'error',
                    'message': 'Category not found'
                }), 404

            products = {}
            for prod in data:
                img = None  # prod img
                product = [prod['name'], prod['description'], img, prod['datetime'],
                           prod['price'], prod['category']]
                products[prod['id']]: product

            return jsonify({
                'status': 'success',
                'data': {
                    'products': products
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


@api.route('/api/get_product/<str:product_name>', methods=['GET'])
@cache.cached(timeout=900)
def get_product(product_name):
    if request.method == 'GET':
        try:
            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM products WHERE name=%s", product_name
            )
            prod = cur.fetchone()
            cur.close()

            if not prod:
                return jsonify({
                    'status': 'error',
                    'message': 'Product not found'
                }), 404

            prod_category = prod['category']
            img = None
            product = [prod['name'], prod['description'], img, prod['datetime'],
                       prod['price'], prod['category']]

            cur = mysql.connection.cursor()
            cur.execute(
                "SELECT * FROM products WHERE category=%s", prod_category
            )
            products = cur.fetchall()
            cur.close()

            sim_products = {}
            for prod in products:
                pd = [prod['name'], prod['description'], img, prod['datetime'],
                      prod['price'], prod['category']]
                sim_products[prod['id']] = pd

            return jsonify({
                'status': 'success',
                'data': {
                    'product': product,
                    'similar_product': sim_products
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

