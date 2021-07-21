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
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT DISTINCT category FROM products'
        )
        data = cur.fetchall()
        categories = [i for i in data]

        cur.execute(
            'SELECT * FROM products'
        )
        data = cur.fetchall()
        cur.close()
        now = datetime.utcnow()

        latest = {}
        for prod in data:
            if len(latest) < 7:
                img = None  # prod img
                product = [prod.name, prod.description, img, prod.datetime]
                latest[prod.id] = product
            else:
                arrival_time = prod.datetime
                time_diff = now - arrival_time

                for k, v in latest.items():
                    if (now - v[3]) > time_diff:
                        latest.pop(k)

                        img = None  # prod img
                        product = [prod.name, prod.description, img, prod.datetime]
                        latest[prod.id] = product
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
            'status': 'error', 'message': f'Internal server error ({e})'
        }), 500


@api.route('/api/get_all_products', methods=['GET'])
@cache.cached(timeout=900)
def get_all_products():
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            'SELECT * FROM products'
        )
        data = cur.fetchall()
        cur.close()

        products = [i for i in data]
        return jsonify({
            'status': 'success',
            'data': {
                'products': products
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error', 'message': e
        }), 500


@api.route('/api/get_category/<str:_name>', methods=['GET'])
@cache.cached(timeout=300)
def get_category(_name):
    try:
        cur = mysql.connection.cursor()
        cur.execute(
            f'SELECT * FROM products WHERE category={_name}'
        )
        data = cur.fetchall()
        cur.close()
        if not data:
            return jsonify({
                'status': 'error', 'message': 'Category not found'
            }), 404

        products = [i for i in data]
        return jsonify({
            'status': 'success',
            'data': {
                'products': products
            }
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error', 'message': e
        }), 500

