#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3
import uuid

from werkzeug.security import generate_password_hash
from ..models import Merchant, Store, Product
from .. import db

import uuid
from ..utilities.schema import validate_merchant, validate_store


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
    name = data['name']
    description = data['description']
    tags = data['tags']

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


def add_merchant_id(merchant_pid, store_id):
    merchant = Merchant.query.filter_by(public_id=merchant_pid).first()
    if not merchant:
        return None, "Merchant not found!"
    if merchant.store_id:
        return None, "Merchant already has a store associated to it"
    merchant.store_id = store_id
    db.session.add(merchant)
    db.session.commit()


def deactivate_merchant(merchant_pid):
    merchant = Merchant.query.filter_by(public_id=merchant_pid).first()
    if not merchant:
        return None, "Merchant not found"
    merchant.active = False
    db.session.add(merchant)
    db.session.commit()
    return 1, "Merchant has been deactivated"


def deactivate_store(store_pid):
    store = Store.query.filter_by(public_id=store_pid).first()
    if not store:
        return None, "Store not found"
    store.active = False
    db.session.add(store)
    db.session.commit()
    return 1, "Store has been deactivated"
