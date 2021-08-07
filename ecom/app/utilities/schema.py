#!usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

merchantDb = {
    'type': 'object',
    'properties': {
        "f_name": {
            'type': 'string'
        },
        "l_name": {
            'type': 'string'
        },
        'email': {
            'type': 'string',
            'format': 'email'
        },
        'phone': {
            'type': 'integer'
        },
        'password': {
            'type': 'string'
        },
        'store_id': {
            'type': 'integer'
        }
    }
}

storeDb = {
    'type': "object",
    'properties': {
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        }
    }
}

productDb = {
    'type': 'object',
    'properties': {
        'store_id': {
            'type': 'integer'
        },
        'name': {
            'type': 'string'
        },
        'description': {
            'type': 'string'
        },
        'price': {
            'type': 'integer'
        },
        'denomination': {
            'type': 'string'
        },
        'category': {
            'type': 'string'
        },
        'tags': {
            'type': 'object'
        }
    }
}


def validate_store(data):
    try:
        validate(data, storeDb)
        return {'msg': 'success'}
    except SchemaError as e:
        return {'msg': 'error', 'error': e.message}
    except ValidationError as e:
        return {'msg': 'error', 'error': e.message}


def validate_product(data):
    try:
        validate(data, productDb)
        return {'msg': 'success'}
    except SchemaError as e:
        return {'msg': 'error', 'error': e.message}
    except ValidationError as e:
        return {'msg': 'error', 'error': e.message}


def validate_merchant(data):
    try:
        validate(data, merchantDb)
        return {'msg': 'success'}
    except SchemaError as e:
        return {'msg': "error", "error": e.message}
    except ValidationError as e:
        return {'msg': 'error', 'error': e.message}

