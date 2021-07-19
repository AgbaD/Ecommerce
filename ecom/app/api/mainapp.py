#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3


from flask import jsonify, make_response, request

import uuid

from . import api



@api.route('/api/v1/home', methods=['GET'])
def home():
    # get top products and categories from db
 
    return jsonify({})
