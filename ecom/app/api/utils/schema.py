#!/usr/bin/python3
# Author:   @AgbaD || @agba_dr3

from jsonschema import validate
from jsonschema.exceptions import SchemaError, ValidationError

userLoginSchema = {
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string',
            'format': 'email',
            'minLength': 7
        },
        'password': {
            'type': 'string'
        }
    },
    'required': ['email', 'password'],
    'additionalProperties': False
}

userRegSchema = {
    'type': 'object',
    'properties': {
        'email': {
            'type': 'string',
            'format': 'email',
            'minLength': 7
        },
        'first_name': {
            'type': 'string',
            'minLength': 3
        },
        'last_name': {
            'type': 'string',
            'minLength': 3
        },
        'password': {
            'type': 'string',
            'minLength': 8
        },
        'phone': {
            'type': 'string'
        },
        'address': {
            'type': 'string'
        }
    },
    'required': ['email', 'password', 'first_name',
                 'last_name', 'phone', 'address'],
    'additionalProperties': False
}

userDbSchema = {
    'type': 'object',
    'properties': {
        'public_id': {
            'type': 'string'
        },
        'email': {
            'type': 'string',
            'format': 'email',
            'minLength': 7
        },
        'first_name': {
            'type': 'string',
            'minLength': 3
        },
        'last_name': {
            'type': 'string',
            'minLength': 3
        },
        'password_hash': {
            'type': 'string'
        },
        'phone': {
            'type': 'string',
            'minLength': 8
        },
        'address': {
            'type': 'string'
        },
        'is_admin': {
            'type': 'boolean'
        },
        'is_active': {
            'type': 'boolean'
        }
    },
    'required': ['public_id', 'email', 'password_hash', 'first_name',
                 'last_name', 'phone', 'address'],
    'additionalProperties': False
}


def validate_login(user):
    try:
        validate(user, userLoginSchema)
        return {"msg": "success"}
    except SchemaError as e:
        return {"msg": "error", "error": e.message}
    except ValidationError as e:
        return {"msg": "error", "error": e.message}


def validate_reg(user):
    try:
        validate(user, userRegSchema)
        return {"msg": "success"}
    except SchemaError as e:
        return {"msg": "error", "error": e.message}
    except ValidationError as e:
        p = list(e.schema_path)
        print(p)
        print(len(p))
        if len(p) > 1:
            if p[1] == 'password' and p[2] == 'minLength':
                error_message = "Password too short, minimum length of 8"
                return {"msg": "error", "error": error_message}
            if p[1] == 'first_name' and p[2] == 'minLength':
                error_message = "First name too short, minimum of 3 characters"
                return {"msg": "error", "error": error_message}
            if p[1] == 'last_name' and p[2] == 'minLength':
                error_message = "Last name too short, minimum of 3 characters"
                return {"msg": "error", "error": error_message}
            if p[1] == 'email' and p[2] == 'minLength':
                error_message = "Email too short, minimum length of 7"
                return {"msg": "error", "error": error_message}
        return {"msg": "error", "error": e.message}

