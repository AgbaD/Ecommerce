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
            'type': 'string'
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
        'merchant_id': {
            'type': 'integer'
        },
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
            'type': 'string'
        },
        'denomination': {
            'type': 'string'
        },
        'category': {
            'type': 'string'
        },
        'tags': {
            'type': 'string'
        }
    }
}

userDb = {
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string',
            'format': 'email'
        },
        'fullname': {
            'type': 'string'
        },
        'phone': {
            'type': 'string'
        },
        'address': {
            'type': 'string'
        },
        'password': {
            'type': 'string'
        }
    }
}


def validate_user(data):
    try:
        validate(data, userDb)
        return {'mag': 'success'}
    except SchemaError as e:
        return {'msg': 'error', 'error': e.message}
    except ValidationError as e:
        return {'msg': 'error', 'error': e.message}


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

