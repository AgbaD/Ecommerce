#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from ..models import Product, Category, Store
# from .. import db


def get_all_products():
    products = Product.query.all()
    if not products:
        return {
            'status': 'error',
            'msg': "Products not found"
        }
    all_products = {}
    i = 0
    for prod in products:
        all_products[i] = {
            'id': prod.id,
            'public_id': prod.public_id,
            'store_id': prod.store_id,
            'name': prod.name,
            'description': prod.description,
            'price': prod.price,
            'denomination': prod.denomination,
            'category': prod.category,
            'reviews': prod.review
        }
        i += 1
    return {
        'status': 'success',
        'data': {
            'products': all_products
        }
    }


def get_product(product_pid):
    prod = Product.query.filter_by(public_id=product_pid).first()
    if not prod:
        return {
            "status": 'error',
            'msg': "Product not found"
        }
    product = {
        0: {
            'id': prod.id,
            'public_id': prod.public_id,
            'store_id': prod.store_id,
            'name': prod.name,
            'description': prod.description,
            'price': prod.price,
            'denomination': prod.denomination,
            'category': prod.category,
            'reviews': prod.review
        }
    }
    return {
        'status': 'success',
        'data': product
    }


def get_all_categories():
    categories = Category.query.all()
    if not categories:
        return {
            'status': 'error',
            'msg': 'Categories not found'
        }

    all_categories = [i.name for i in categories]
    return {
        'status': 'success',
        'data': {
            'categories': all_categories
        }
    }


def get_category_products(category):
    products = Product.query.filter_by(category=category).all()
    if not products:
        return {
            'status': 'error',
            'msg': "Products not found"
        }

    all_products = {}
    i = 0
    for prod in products:
        all_products[i] = {
            'id': prod.id,
            'public_id': prod.public_id,
            'store_id': prod.store_id,
            'name': prod.name,
            'description': prod.description,
            'price': prod.price,
            'denomination': prod.denomination,
            'category': prod.category,
            'reviews': prod.review
        }
        i += 1
    return {
        'status': 'success',
        'data': {
            'products': all_products
        }
    }


def get_all_stores():
    stores = Store.query.all()
    if not stores:
        return {
            'status': 'error',
            'msg': "Stores not found"
        }

    all_stores = {}
    i = 0
    for store in stores:
        all_stores[i] = {
            'id': store.id,
            'public_id': store.public_id,
            'name': store.name,
            'description': store.description,
            'active': store.active,
            'tags': store.tags
        }
        i += 1
    return {
        'status': 'success',
        'data': {
            'stores': all_stores
        }
    }


def get_all_products_from_store(store_pid):
    products = Product.query.filter_by(store_id=store_id).all()
    if not products:
        return {
            'status': 'error',
            'msg': "Store does not contain any product"
        }

    all_products = {}
    i = 0
    for prod in products:
        all_products[i] = {
            'id': prod.id,
            'public_id': prod.public_id,
            'store_id': prod.store_id,
            'name': prod.name,
            'description': prod.description,
            'price': prod.price,
            'denomination': prod.denomination,
            'category': prod.category,
            'reviews': prod.review
        }
        i += 1
    return {
        'status': 'success',
        'data': {
            'products': all_products
        }
    }


def get_product_reviews(product_pid):
    product = Product.query.filter_by(public_id=product_id).first()
    if not product:
        return {
            'status': 'error',
            'msg': "Product not found"
        }
    reviews = product.reviews
    if not reviews:
        return {
            'status': 'error',
            'msg': "Product does not have reviews"
        }
    all_reviews = {}
    i = 0
    for rev in reviews:
        all_reviews[i] = rev
        i += 1
    return {
            'status': 'success',
            'data': {
                'reviews': all_reviews
            }
        }
