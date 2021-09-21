#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

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
    phone = db.Column(db.PickleType)
    password_hash = db.Column(db.String(256))
    active = db.Column(db.Boolean, default=True)
    admin_active_remark = db.Column(db.Boolean, default=True)


class Store(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    merchant_id = db.Column(db.Integer, defald=None)
    name = db.Column(db.String(128))
    description = db.Column(db.String(256))
    tags = db.Column(db.String(128))
    date_created = db.Column(db.Datetime)
    active = db.Column(db.Boolean, default=False)
    is_verified = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(Store, self).__init__(**kwargs)
        Store.date_created = datetime.utcnow()


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    merchant_id = db.Column(db.Integer)
    store_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    description = db.Column(db.String(512))
    price = db.Column(db.Integer)
    denomination = db.Column(db.String(8))
    category = db.Column(db.String(128))
    tags = db.Column(db.String(128))
    reviews = db.Column(db.PickleType)


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    merchant_id = db.Column(db.Integer)
    content = db.Column(db.String(2048))
    datetime = db.Column(db.DateTime, default=datetime.utcnow())


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    email = db.Column(db.String(128))
    fullname = db.Column(db.String(128))
    phone = db.Column(db.Integer)
    address = db.Column(db.String(256))
    password_hash = db.Column(db.string(256))
    active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)


class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    email = db.Column(db.String(128))
    password_hash = db.Column(db.String(128))

