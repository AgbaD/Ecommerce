#!/usr/bin/python3
# Author: @AgbaD | @agba_dr3

from flask import Blueprint

main = Blueprint('main', __name__)

from . import mainapp

