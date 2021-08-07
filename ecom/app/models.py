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


class Store(db.Model):
    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    merchant_id = db.Column(db.Integer, defald=None)
    name = db.Column(db.String(128))
    description = db.Column(db.String(256))
    tags = db.Column(db.PickleType)
    active = db.Column(db.Boolean, default=False)


class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(256))
    store_id = db.Column(db.Integer)
    name = db.Column(db.String(128))
    description = db.Column(db.String(512))
    price = db.Column(db.Integer)
    denomination = db.Column(db.String(8))
    category = db.Column(db.String(128))
    tags = db.Column(db.PickleType)


