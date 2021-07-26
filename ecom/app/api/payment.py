#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from flask import jsonify, request, current_app

import uuid
from datetime import datetime, timedelta

from . import api
from .. import mysql
from .utils import token_required


@api.route('/api/purchase/<str:product_name>', methods=[])
@token_required
def purchase(current_user, product_name):
    pass
