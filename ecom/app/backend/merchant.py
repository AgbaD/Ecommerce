#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3
import uuid

from ..models import Merchant, Store, Product, Feedback
from werkzeug.security import generate_password_hash
from .. import db

import uuid
from ..utilities.schema import validate_merchant, validate_store
from ..utilities.schema import validate_product


def create_merchant(data=None):
    if not data:
        return None, ""
    try:
        f_name = data['firstname']
        l_name = data['lastname']
        email = data['email']
        phone = data['phone']
        password = data['password']
        store_id = data['store_id']
    except Exception as e:
        return None, e

    mern = {
        'f_name': f_name,
        'l_name': l_name,
        'email': email,
        'phone': phone,
        'password': password,
        'store_id': store_id
    }

    schema = validate_merchant(mern)
    if schema['msg'] != 'success':
        return None, schema['error']

    merchant = Merchant.query.filter_by(email=email).first()
    if merchant:
        return None, "Email has already been used"

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
    return 1, "Merchant Created!"


def create_store(data=None):
    if not data:
        return None, ""
    try:
        name = data['name']
        description = data['description']
        tags = data['tags']
    except Exception as e:
        return None, e

    store = {
        'name': name,
        'description': description
    }

    schema = validate_store(store)
    if schema['msg'] != 'success':
        return None, schema['error']

    store = Store.query.filter_by(name=name).first()
    if store:
        return None, "Store name has already been used"

    public_id = str(uuid.uuid4())
    store = Store(
        name=name,
        public_id=public_id,
        description=description,
        tags=tags
    )
    db.session.add(store)
    db.session.commit()
    return 1, "Store Created!"


def add_merchant_id(store_pid, merchant_id):
    store = Store.query.filter_by(public_id=store_pid).first()
    if not store:
        return None, ""
    if store.merchant_id:
        return None, ""
    store.merchant_id = merchant_id
    db.session.add(store)
    db.session.commit()
    return 1, ""


def deactivate_merchant(merchant_pid):
    merchant = Merchant.query.filter_by(public_id=merchant_pid).first()
    if not merchant:
        return None, ""
    merchant.active = False
    db.session.add(merchant)
    db.session.commit()
    return 1, ""


def deactivate_store(store_pid):
    store = Store.query.filter_by(public_id=store_pid).first()
    if not store:
        return None, "Store not found"
    store.active = False
    db.session.add(store)
    db.session.commit()
    return 1, ""


def create_product(data):
    if not data:
        return None, ""
    try:
        store_id = data['store_id']
        name = data['name']
        description = data['description']
        price = data['price']
        denomination = data['denomination']
        category = data['category']
        tags = data['tags']
    except Exception as e:
        return None, e

    prod = {
        'store_id': store_id,
        'name': name,
        'description': description,
        'price': price,
        'denomination': denomination,
        'category': category,
        'tags': tags
    }

    schema = validate_product(prod)
    if schema['msg'] != 'success':
        return None, schema['error']

    prod = Product.query.filter_by(name=name).first()
    if prod and prod.store_id == store_id:
        return None, ""

    public_id = str(uuid.uuid4())
    product = Product(
        public_id=public_id,
        store_id=store_id,
        name=name,
        description=description,
        price=price,
        denomination=denomination,
        category=category,
        tags=tags
    )

    db.session.add(product)
    db.session.commit()
    return 1, ""


def update_products(product_pid, data):
    product = Product.query.filter_by(public_id=product_pid).first()
    if not product:
        return None, ""
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
    return 1, ""


def get_all_products(merchant_id):
    products = Product.query.filter_by(merchant_id=merchant_id).all()
    if not products:
        return None, ""
    return 1, products


def get_all_feedback(merchant_id):
    feedback = Feedback.query.filter_by(merchant_id=merchant_id).all()
    if not feedback:
        return None, ""
    return 1, feedback


def get_product_reviews(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    if not product:
        return None, ""
    reviews = product.reviews
    return 1, reviews

