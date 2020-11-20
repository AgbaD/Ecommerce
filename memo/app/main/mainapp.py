#!/usr/bin/python3
# Author:   @AgbaD | @agba_dr3

from flask import jsonify, request
from . import main
from ..models import User, Memo


@main.route("/api/get_user/<public_id>", methods=["GET"])
def get_user(public_id):
    pass


@main.route("/api/get_all_users", methods=["GET"])
def get_all_users():
    pass


@main.route("/api/create_acc", methods=["POST"])
def create_acc():
    pass


@main.route("api/edit_user/<public_id>", methods=["PUT"])
def edit_user(public_id):
    pass


@main.route("api/login", methods=["POST"])
def login():
    pass
