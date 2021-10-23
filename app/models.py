#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

import ast
from . import db
from datetime import datetime


class Merchant(db.Model):
    __tablename__ = "merchants"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    store_id = db.Column(db.Integer)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.String)
    password_hash = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=True)
    admin_active_remark = db.Column(db.Boolean, default=True)


class Store(db.Model):
    __tablename__ = "stores"
    __searchable__ = ['name', 'tags']
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    merchant_id = db.Column(db.Integer, default=None)
    name = db.Column(db.String(128))
    description = db.Column(db.String(256))
    tags = db.Column(db.String(128))
    date_created = db.Column(db.DateTime, default=datetime.utcnow())
    active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)


class Product(db.Model):
    __tablename__ = "products"
    __searchable__ = ['name', 'tags', 'category']
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    merchant_id = db.Column(db.Integer)
    store_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    description = db.Column(db.String(512))
    price = db.Column(db.String)
    denomination = db.Column(db.String(8))
    category = db.Column(db.String(128))
    tags = db.Column(db.String(128))
    review = db.Column(db.String(8192), default="{}")

    def add_review(self, username, review):
        rev = ast.literal_eval(self.review)
        rev[username] = review
        self.review = str(rev)

    def get_reviews(self):
        return ast.literal_eval(self.review)


class Category(db.Model):
    __tablename__ = "category"
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(128))
    merchant_id = db.Column(db.Integer)
    content = db.Column(db.String(4096))
    datetime = db.Column(db.DateTime, default=datetime.utcnow())


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    email = db.Column(db.String(128))
    fullname = db.Column(db.String(128))
    phone = db.Column(db.String)
    address = db.Column(db.String(256))
    password_hash = db.Column(db.String(256))
    cart = db.Column(db.String(1024), default="[]")
    active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)

    def add_to_cart(self, product_pid):
        if self.cart == "[]":
            self.cart = str([product_pid])
        else:
            ca = ast.literal_eval(self.cart)
            ca.append(product_pid)
            self.cart = str(ca)

    def remove_from_cart(self, product_pid):
        if self.cart == "[]":
            pass
        else:
            ca = ast.literal_eval(self.cart)
            ca.remove(product_pid)
            self.cart = str(ca)

    def get_cart(self):
        return ast.literal_eval(self.cart)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

