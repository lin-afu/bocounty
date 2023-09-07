from flask import make_response, jsonify, abort
from app.utils.enum_util import APIStatusCode


def make_error_response(code: APIStatusCode, reason: str = ''):
    return make_response(jsonify({
        'status': code.value.api_code,
        'reason': reason
    }), code.value.http_code)
