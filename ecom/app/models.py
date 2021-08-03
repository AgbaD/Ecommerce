#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from . import db
from datetime import datetime


class Merchant:
    __tablename__ = "merchants"
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(128))
    last_name = db.Column(db.String(128))
    public_id = db.Column(db.String(128))
    store_id = db.Column(db.String(128))
    email = db.Column(db.String(128))
    phone = db.Column(db.PickleType)
    password_hash = db.Column(db.String(128))


