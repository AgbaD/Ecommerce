#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

import jwt
from . import api
from ..backend.misc import get_product
from datetime import datetime, timedelta
from flask import jsonify, request, current_app
from .utils.auth import token_required, admin_required, merchant_required


@api.route("/index", methods=['GET'])
def index():
    return jsonify({
        'msg': 'You are connected!'
    }), 200


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
