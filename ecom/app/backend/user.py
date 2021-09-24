#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3


import uuid
from .. import db
from .utils.schema import validate_user
from ..models import User, Product, Feedback, Merchant, Store
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(data):
    email = data['email']
    fullname = data['fullname']
    password = data['password']
    repeat_password = data['repeat_password']
    phone = data['phone']
    address = data['address']

    info = {
        'email': email,
        'password': password,
        'fullname': fullname,
        'phone': phone,
        'address': address
    }

    if password != repeat_password:
        return {
            'status': 'error',
            'msg': 'Passwords do not match!'
        }

    schema = validate_user(info)
    if schema['msg'] != 'success':
        return {
            'status': 'error',
            'msg': schema['error']
        }

    user = User.query.filter_by(email=email).first()
    if user:
        return {
            'status': 'error',
            'msg': 'Email has already been used'
        }

    password_hash = generate_password_hash(password)
    public_id = str(uuid.uuid4())
    user = User(
        public_id=public_id,
        email=email,
        fullname=fullname,
        phone=phone,
        address=address,
        password_hash=password_hash
    )

    db.session.add(user)
    db.session.commit()
    return {
        'status': 'success',
        'msg': "User has been created successfully!"
    }


def deactivate_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return {
            'status': 'error',
            'msg': 'User not found!'
        }
    if not user.active:
        return {
            'status': 'success',
            'msg': 'User already deactivated!'
        }
    user.active = False
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'success',
        'msg': 'User has been deactivated successfully'
    }


def activate_user(info):
    email = info['email']
    password = info['password']

    user = User.query.filter_by(email=email).first()
    if not user:
        return {
            'status': 'error',
            'msg': 'User not found!'
        }

    if not check_password_hash(user.password_hash, password):
        return {
            'status': 'error',
            'msg': 'Password is incorrect!'
        }

    if user.active:
        return {
            'status': 'success',
            'msg': 'User already active'
        }

    user.active = True
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'success',
        'msg': 'User has been activated successfully'
    }


def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return {
            'status': 'error',
            'msg': 'User not found!'
        }
    db.session.delete(user)
    db.session.commit()
    return {
        'status': 'success',
        'msg': 'User deleted successfully'
    }


def login_user(data):
    email = data['email']
    password = data['password']

    # check email using regex

    user = User.query.filter_by(email=email).first()
    if not user:
        return {
            'status': 'error',
            'msg': "User not found"
        }

    if check_password_hash(user.password_hash, password):
        return {
            'status': 'success',
            'data': {
                'public_id': user.public_id
            }
        }
    return {
        'status': 'error',
        'msg': 'Password is incorrect'
    }


def add_to_cart(user_pid, product_pid):
    user = User.query.filter_by(public_id=user_pid).first()
    if not user:
        return {
            'status': 'error',
            'msg': 'User not found'
        }

    product = Product.query.filter_by(public_id=product_pid).first()
    if not product:
        return {
            'status': 'error',
            'msg': 'Product not found'
        }

    user.cart.append(product)
    db.session.add(user)
    db.session.commit()
    return {
        'status': 'success',
        'msg': 'Product added to cart'
    }


def remove_from_cart(user_pid, product_pid):
    user = User.query.filter_by(public_id=user_pid).first()
    if not user:
        return {
            'status': 'error',
            'msg': 'User not found'
        }

    product = Product.query.filter_by(public_id=product_pid).first()
    if not product:
        return {
            'status': 'error',
            'msg': 'Product not found'
        }

    if product in user.cart:
        user.cart.remove(product)
        db.session.add(user)
        db.session.commit()
        return {
            'status': 'success',
            'msg': 'Product removed from cart'
        }
    return {
        'status': 'error',
        'msg': 'Product not present in cart'
    }


def get_cart(user_pid):
    user = User.query.filter_by(public_id=user_pid).first()
    if not user:
        return {
            'status': 'error',
            'msg': 'User not found'
        }

    f_cart = user.cart
    if not f_cart:
        return {
            'status': 'success',
            'msg': 'User cart is empty'
        }

    cart = {}
    i = 0
    for prod in f_cart:
        cart[i] = {
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
            'cart': cart
        }
    }


def product_review(user_pid, product_pid, review):
    user = User.query.filter_by(public_id=user_pid).first()
    if not user:
        return {
            'status': 'error',
            'msg': 'User not found'
        }

    product = Product.query.filter_by(public_id=product_pid).first()
    if not product:
        return {
            'status': 'error',
            'msg': 'Product not found'
        }

    username = user.fullname
    rev = {username: review}
    product.review.append(rev)
    db.session.add(product)
    db.session.commit()
    return {
        'status': 'success',
        'msg': 'Product review added successfully!'
    }


def store_feedback(user_pid, store_pid, feedback):
    user = User.query.filter_by(public_id=user_pid).first()
    if not user:
        return {
            'status': 'error',
            'msg': 'User not found'
        }

    store = Store.query.filter_by(public_id=store_pid).first()
    if not store:
        return {
            'status': 'error',
            'msg': 'Store not found'
        }

    merchant_id = store.merchant_id
    feedback = Feedback(
        user=user.fullname,
        merchant_id=merchant_id,
        content=feedback
    )
    db.session.add(feedback)
    db.session.commit()
    return {
        'status': 'success',
        'msg': 'Feedback sent successfully!'
    }

