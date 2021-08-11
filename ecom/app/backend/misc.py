#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from ..models import Product


def get_product(data):
    product_pid = data["product_pid"]

    product = Product.query.filter_by(public_id=product_pid)
    if not product:
        return {
            "status": 'error',
            'msg': "Product not found"
        }

    return {
        'status': 'success',
        'data': product
    }
