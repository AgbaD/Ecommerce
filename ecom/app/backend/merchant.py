#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from werkzeug.security import generate_password_hash, check_password_hash
from ..models import Merchant, Store, Product, Feedback
from .. import db

import uuid
from .utils.schema import validate_product
from .utils.schema import validate_merchant, validate_store


def create_merchant(data):
    try:
        f_name = data['firstname']
        l_name = data['lastname']
        email = data['email']
        phone = data['phone']
        password = data['password']
        repeat_password = data['repeat_password']
        store_id = data['store_id']
    except Exception as e:
        return {
            "status": 'error',
            'msg': e
        }

    mern = {
        'f_name': f_name,
        'l_name': l_name,
        'email': email,
        'phone': phone,
        'password': password,
        'store_id': store_id
    }

    if password != repeat_password:
        return {
            "status": 'error',
            'msg': "Passwords do not match"
        }

    schema = validate_merchant(mern)
    if schema['msg'] != 'success':
        return {
            "status": 'error',
            'msg': schema['error']
        }

    merchant = Merchant.query.filter_by(email=email).first()
    if merchant:
        return {
            "status": 'error',
            'msg': "Email has already been used"
        }

    password_hash = generate_password_hash(password)
    public_id = str(uuid.uuid4())

    merchant = Merchant(
        first_name=f_name,
        last_name=l_name,
        public_id=public_id,
        store_id=store_id,
        email=email,
        phone=phone,
        password_hash=password_hash
    )
    db.session.add(merchant)
    db.session.commit()
    return {
        'status': "success",
        'data': {
            'merchant': merchant
        }
    }


def create_store(data):
    try:
        name = data['name']
        description = data['description']
        tags = data['tags']
    except Exception as e:
        return {
            "status": 'error',
            'msg': e
        }

    store = {
        'name': name,
        'description': description
    }

    schema = validate_store(store)
    if schema['msg'] != 'success':
        return {
            "status": 'error',
            'msg': schema['error']
        }

    store = Store.query.filter_by(name=name).first()
    if store:
        return {
            "status": 'error',
            'msg': "Store name has already been used"
        }

    public_id = str(uuid.uuid4())
    store = Store(
        name=name,
        public_id=public_id,
        description=description,
        tags=tags
    )
    db.session.add(store)
    db.session.commit()
    return {
        'status': "success",
        'data': {
            'store': store
        }
    }


def add_merchant_id(store_pid, merchant_id):
    store = Store.query.filter_by(public_id=store_pid).first()
    if not store:
        return {
            "status": 'error',
            'msg': "Store not found"
        }
    if store.merchant_id:   # should never happen
        return {
            "status": 'error',
            'msg': "Store already has a merchant id"
        }
    store.merchant_id = merchant_id
    db.session.add(store)
    db.session.commit()
    return {
        "status": 'success',
        'msg': "Merchant id added successfully"
    }


def login_merchant(data):
    email = data['email']
    password = data['password']

    # check email using regex

    merchant = Merchant.query.filter_by(email=email).first()
    if not merchant:
        return {
            'status': 'error',
            'msg': "Merchant not found"
        }

    if check_password_hash(merchant.password_hash, password):
        return {
            'status': 'success',
            'data': {
                'public_id': merchant.public_id
            }
        }

    return {
        'status': 'error',
        'msg': 'Password is incorrect'
    }


def deactivate_merchant(merchant_pid):
    merchant = Merchant.query.filter_by(public_id=merchant_pid).first()
    if not merchant:
        return {
            "status": 'error',
            'msg': "Merchant not found"
        }
    merchant.active = False
    db.session.add(merchant)
    db.session.commit()
    return {
        "status": 'success',
        'msg': "Merchant deactivated successfully"
    }


def deactivate_store(store_pid):
    store = Store.query.filter_by(public_id=store_pid).first()
    if not store:
        return {
            "status": 'error',
            'msg': "Store not found"
        }
    store.active = False
    db.session.add(store)
    db.session.commit()
    return {
        "status": 'success',
        'msg': "Store deactivated successfully"
    }


def create_product(data):
    if not data:
        return {
            'status': 'error',
            'msg': "data not found"
        }
    try:
        merchant_id = data['merchant_id']
        name = data['name']
        description = data['description']
        price = data['price']
        denomination = data['denomination']
        category = data['category']
        tags = data['tags']
    except Exception as e:
        return {
            'status': 'error',
            'msg': e
        }

    prod = {
        'merchant_id': merchant_id,
        'name': name,
        'description': description,
        'price': price,
        'denomination': denomination,
        'category': category,
        'tags': tags
    }

    schema = validate_product(prod)
    if schema['msg'] != 'success':
        return {
            'status': 'error',
            'msg': schema['error']
        }

    prod = Product.query.filter_by(name=name).first()
    if prod and prod.merchant_id == merchant_id:
        return {
            'status': 'error',
            'msg': "Product with same name already created"
        }

    public_id = str(uuid.uuid4())
    product = Product(
        public_id=public_id,
        merchant_id=merchant_id,
        name=name,
        description=description,
        price=price,
        denomination=denomination,
        category=category,
        tags=tags
    )

    db.session.add(product)
    db.session.commit()
    return {
        "status": 'success',
        'msg': 'Product successfully created',
        'data': {
            'product': product
        }
    }


def get_product(product_pid):
    pass


def update_product(product_pid, data):
    product = Product.query.filter_by(public_id=product_pid).first()
    if not product:
        return {
            'status': 'error',
            'msg': 'Product not found'
        }
    try:
        name = data['name']
        product.name = name
    except Exception:
        pass

    try:
        description = data['description']
        product.description = description
    except Exception:
        pass

    try:
        price = data['price']
        product.price = price
    except Exception:
        pass

    try:
        denomination = data['denomination']
        product.denomination = denomination
    except Exception:
        pass

    try:
        category = data['category']
        product.category = category
    except Exception:
        pass

    try:
        tags = data['tags']
        product.tags = tags
    except Exception:
        pass

    db.session.add(product)
    db.session.commit()
    return {
        'status': 'success',
        'msg': 'Product updated successfully'
    }


def get_all_products(merchant_id):
    products = Product.query.filter_by(merchant_id=merchant_id).all()
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


def get_all_feedback(merchant_id):
    feedback = Feedback.query.filter_by(merchant_id=merchant_id).all()
    if not feedback:
        return {
            'status': 'error',
            'msg': "Feedbacks not found"
        }
    return {
        'status': 'success',
        'data': {
            'feedback': feedback
        }
    }


def get_product_reviews(product_id):
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

