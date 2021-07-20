#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3


from flask import jsonify, request, current_app

from . import api
from .utils import token_required
from .. import mysql

from datetime import datetime


@api.route('/api/v1/home', methods=['GET'])
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
        now = datetime.utcnow()

        latest = {}
        for prod in data:
            if len(latest) < 7:
                pid = prod.id
                name = prod.name
                description = prod.des
                arrival_time = prod.datetime
                img = None  # prod img
                product = [name, description, img, arrival_time]
                latest[pid] = product
            else:
                arrival_time = prod.datetime


        return jsonify({
            'status': 'success', 'message': '',
            'data': {
                'categories': categories,
                'latest': ''
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'error', 'message': f'Internal server error ({e})'
        }), 500
