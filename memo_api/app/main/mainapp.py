#!/usr/bin/python3
# Author:   @AgbaD | @agba_dr3

from werkzeug.security import generate_password_hash, check_password_hash
from flask import jsonify, request, make_response, current_app
from functools import wraps
import jwt
import uuid
import datetime
from . import main
from .. import db
from ..models import User, Memo


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({"status": "error", "msg": "Token is missing"}), 401

        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({"status": "error", "msg": "Token is invalid"}), 401

        return f(current_user, *args, **kwargs)
    return decorated


@main.route("/api/get_user/<public_id>", methods=["GET"])
@token_required
def get_user(current_user, public_id):
    pass


@main.route("/api/get_me", methods=["GET"])
@token_required
def get_me(current_user):
    data = {'email': current_user.email, 'name': current_user.name,
            'admin': current_user.admin}

    return jsonify(data)


@main.route("/api/get_all_users", methods=["GET"])
@token_required
def get_all_users(current_user):
    if not current_user.admin:
        return jsonify({"status": "error", "msg": "Can not perform action"}), 403

    all_users = User.query.all()
    memos = Memo.query.all()

    output = []
    for user in all_users:
        data = {'email': user.email, 'public_id': user.public_id,
                'name': user.name, 'active': user.active,
                'memos': {}}
        if memos:
            for mem in memos:
                if mem.user_id == user.id:
                    data['memos'][mem.date] = mem.text

        output.append(data)

    return jsonify({'users': output})


@main.route("/api/create_acc", methods=["POST"])
def create_acc():
    try:
        data = request.get_json()

        email = data['email']

        tmp_usr = None
        try:
            tmp_usr = User.query.filter_by(email=email).first()
        except:
            pass
        if tmp_usr:
            return jsonify({"status": "error", "msg": "Email already taken"}), 409
        # if data['password'] != data['password_again']:
            # return jsonify({"status": "error", "msg": "Passwords do not coincide"}), 409

        name = data['name']
        hash_password = generate_password_hash(data['password'])
        public_id = str(uuid.uuid4())

        user = User(public_id=public_id, name=name, email=email,
                    password=hash_password)
        db.session.add(user)
        db.session.commit()

        return jsonify({"status": "success", "msg": "User Created!"}), 201
    except:
        return jsonify({"status": "error", "msg": "Internal Server Error"}), 500


@main.route("/api/edit_user", methods=["PUT"])
def edit_user():
    pass


@main.route("/api/login", methods=["POST"])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response("Could not verify", 401, {
            'WWW-Authenticate': 'Basic realm="Login required"'
        })

    user = User.query.filter_by(email=auth.username).first()

    if not user:
        return make_response("Could not verify", 401, {
            'WWW-Authenticate': 'Basic realm="Login required"'
        })

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id': user.public_id,
                            'exp': datetime.datetime.utcnow() +
                                   datetime.timedelta(minutes=30)},
                           current_app.config['SECRET_KEY'])
        return jsonify({"status": "success", "token": token.decode('UTF-8')})
    return make_response("Could not verify", 401, {
        'WWW-Authenticate': 'Basic realm="Login required"'
    })



