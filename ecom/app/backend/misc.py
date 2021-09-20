#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from ..models import Product


def get_product(product_pid):
    product = Product.query.filter_by(public_id=product_pid).first()
    if not product:
        return {
            "status": 'error',
            'msg': "Product not found"
        }

    return {
        'status': 'success',
        'data': product
    }


def get_all_products():
    products = Product.query.all()
    if not products:
        return {
            'status': 'error',
            'msg': "Products not found"
        }
    return {
        'status': 'success',
        'data': {
            'products': products
        }
    }


def get_all_store_products(store_id):
    products = Product.query.filter_by(store_id=merchant_id).all()
    if not products:
        return {
            'status': 'error',
            'msg': "Products not found"
        }
    return {
        'status': 'success',
        'data': {
            'products': products
        }
    }


def get_product_reviews(product_pid):
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return {
            'status': 'error',
            'msg': "Product not found"
        }
    reviews = product.reviews
    if not reviews:
        return {
            'status': 'error',
            'msg': "Product review not found"
        }
    return {
            'status': 'success',
            'data': {
                'reviews': reviews
            }
        }