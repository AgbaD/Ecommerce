#!/usr/bin/python3
# Author:   @AgbaD | @agba_dr3

from . import db


class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(80))
    email = db.Column(db.String(50))
    admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"User(name:{name}, email:{email}, public_id:{public_id})"


class Memo(db.Model):
    __tablename__ = "memo"
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    text = db.Column(db.String)
    title = db.Column(db.String)
    user_id = db.Column(db.Integer)

