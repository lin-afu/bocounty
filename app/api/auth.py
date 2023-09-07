import json
import time
from datetime import datetime, timedelta
import hashlib
import uuid
from app.utils import get_now
from app.utils.jwt_util import JWTGenerator
from app.utils.respons_util import make_error_response
from app.utils.enum_util import APIStatusCode

from flask import Blueprint, jsonify, make_response, Response, request, current_app

from app.database import db
from app.models import Account, OwnItem, PickedItem

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/Register", methods=['POST'])
def register():
    """
        註冊使用者並且確認Email是否重複
        tags:
            - Register
        produces:
            - application/json
        parameters:
            - name: str
            - email: str
            - password: str
    """
    request_json: dict = request.json
    if "student_id" not in request_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'student_id' argument!")

    if "name" not in request_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'name' argument!")

    if "password" not in request_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'password' argument!")

    # 確認帳號使否重複
    user_count = Account.query.filter(
        Account.student_id == request.json["student_id"]
    ).count()

    if user_count != 0:
        return jsonify({
            'cause': 101
        })

    account_info = request.json
    account_info['password'] = hashlib.sha256(request.json['password'].encode("utf-8")).hexdigest()

    # 插入新的帳號
    new_id = uuid.uuid4().hex

    if account_info['student_id']=="0000":
        bocoin_=1000
    else:
        bocoin_=0

    new_account = Account(
        id=new_id,
        student_id=account_info['student_id'],
        name=account_info['name'],
        password=account_info['password'],
        intro="留下你的自我介紹吧!",
        bocoin=bocoin_

    )
    # 插入初始服裝[1,2,9,20,15,16,21,30]
    now_time = get_now()
    new_item_list = [1,2,9,20,15,16,21,30]
    for i in new_item_list:
        new_own_item = OwnItem(
            user_id = new_id,
            item_id = i,
            get_time = str(now_time)
        )
        db.session.add(new_own_item)
        db.session.commit()

    # 建立初始外觀[1,9,15,4]
    new_outlook_list = [1,9,15,21]
    for i in new_outlook_list:
        new_outlook = PickedItem(
             user_id = new_id,
             item_id = i
        )
        db.session.add(new_outlook)
        db.session.commit()

    db.session.add(new_account)
    db.session.commit()

    # token = factory.JWTGenerator.generate_token({"user_id": new_id})
    res = make_response(json.dumps({"cause": 0}))

    token_setter(name="User_Token", respond=res,
                 payload={"user_id": new_id})
    # res.set_cookie("User_Token", token, expires=time.time() + 60 * 60)
    return res


@auth_api.route("/Login", methods=['POST'])
def login():
    auth_info: dict = request.json
    if "student_id" not in auth_info.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'student_id' argument!")
    if "password" not in auth_info.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'password' argument!")
    print(hashlib.sha256(request.json['password'].encode("utf-8")).hexdigest())
    auth_info['password'] = hashlib.sha256(request.json['password'].encode("utf-8")).hexdigest()
    # 確認有沒有此account
    user: Account = Account.query.filter(
        Account.student_id == auth_info['student_id'],
        Account.password == auth_info['password']
    ).first()

    if user is not None:
        res = make_response(json.dumps({"status": 0,"user_id": user.id}))
        token_setter(name="User_Token", respond=res,
                     payload={"user_id": user.id})
        return res
    else:
        return make_error_response(APIStatusCode.WrongLoginInfo, reason='wrong password or id!')


@auth_api.route("/Loginadmin", methods=['POST'])
def loginadmin():
    """
        用於驗證使用者登入資訊，並發放token

        :parameter:
            - name: str
            - email: str
            - password: str
        :return:
            - application/json
    """
    auth_info = request.json
    auth_info['password'] = hashlib.sha256(request.json['password'].encode("utf-8")).hexdigest()
    # 確認有沒有此account
    user: Account = Account.query.filter(
        Account.student_id == auth_info['student_id'],
        Account.password == auth_info['password'],
        Account.permission == 1
    ).first()

    if user is not None:
        res = make_response(json.dumps({"status": 0,"user_id": user.id}))
        token_setter(name="User_Token", respond=res,
                     payload={"user_id": user.id})
        return res
    else:
        return make_error_response(APIStatusCode.WrongLoginInfo, reason='wrong password or id!')


@auth_api.route("/Logoff", methods=['POST'])
def logoff():
    jwt_gen: JWTGenerator = current_app.config['jwt_gen']

    if request.cookies.get('User_Token') is None:
        return "", 401
    if not jwt_gen.check_token_valid(request.cookies.get('User_Token')):
        return "", 401

    res = make_response(json.dumps({
        "status": 0
    }))
    res.set_cookie("User_Token", "", expires=time.time() - 1)
    return res


def token_setter(
        name: str,
        respond: Response,
        payload: dict,
        time: timedelta = timedelta(days=1)) -> None:
    jwt_gen: JWTGenerator = current_app.config['jwt_gen']
    jwt = jwt_gen.generate_token(payload)
    respond.set_cookie(name, value=jwt, expires=datetime.now() + time)
