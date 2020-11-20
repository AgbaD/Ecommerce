#!/usr/bin/python3
# Author:   @AgbaD | @agba_dr3

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request
import uuid
from . import main
from .. import db
from ..models import User, Memo


@main.route("/api/get_user/<public_id>", methods=["GET"])
def get_user(public_id):
    pass


@main.route("/api/get_all_users", methods=["GET"])
def get_all_users():
    pass


@main.route("/api/create_acc", methods=["POST"])
def create_acc():
    data = request.get_json()

    name = data['name']
    hash_password = generate_password_hash(data['password'])
    email = data['email']
    public_id = str(uuid.uuid4())

    user = User(public_id=public_id, name=name, email=email,
                password=hash_password)
    db.session.add(user)
    db.session.commit()


@main.route("api/edit_user/<public_id>", methods=["PUT"])
def edit_user(public_id):
    pass


@main.route("api/login", methods=["POST"])
def login():
    pass
