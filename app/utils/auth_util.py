from flask import current_app, request, abort, jsonify
from app.utils.jwt_util import JWTGenerator
from app.utils.respons_util import make_error_response
from app.utils.enum_util import APIStatusCode
from app.models import Account
from functools import wraps


def verify_jwt(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if _get_token_detail() is None:
            return 'require login', 401
        else:
            return func(*args, **kwargs)

    return wrap


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        login_state = check_login()

        if login_state == -1:
            return make_error_response(APIStatusCode.NotLogin, reason='user has not token')
        if login_state == -2:
            return make_error_response(APIStatusCode.NotLogin, reason='user not found')

        return func(*args, **kwargs)

    return wrapper


def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        login_state = check_login(admin=True)

        if login_state == -1:
            return make_error_response(APIStatusCode.NotLogin, reason='user has not token')
        if login_state == -2:
            return make_error_response(APIStatusCode.NotLogin, reason='user not found')
        if login_state == -3:
            return make_error_response(APIStatusCode.NotGrant, reason='user has no permission')

        return func(*args, **kwargs)

    return wrapper


def get_user_by_token():
    token_info = _get_token_detail()
    user: Account = Account.query.filter(
        Account.id == token_info['user_id']
    ).first()
    # print(token_info)
    return user


def check_login(admin=False) -> int:
    token_info = _get_token_detail()
    if token_info is None:
        return -1

    user: Account = Account.query.filter(
        Account.id == token_info['user_id']
    ).first()
    if user is None:
        return -2
    if admin:
        if user.permission != 1:
            return -3
    return 0


def _get_token_detail():
    jwt_gen: JWTGenerator = current_app.config['jwt_gen']
    token = request.cookies.get("User_Token")

    if token is None:
        print('token is None')
        return None

    if not jwt_gen.check_token_valid(token):
        print('Token not valid')
        return None
    # print(request.cookies.get("User_Token"))
    return jwt_gen.get_token_detail(token)
