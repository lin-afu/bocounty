from flask import Blueprint, jsonify, request
from app.utils import database
from app.utils.auth_util import login_required, get_user_by_token, admin_required
from app.models import Account
from app.utils.respons_util import make_error_response
from app.utils.enum_util import APIStatusCode
import sqlite3

coupon_api = Blueprint("coupon_api", __name__)


@coupon_api.route("/", methods=["GET"])
@login_required
def get_all():
    coupon_list: list = get_list()
    return jsonify({
        "status": 0,
        "coupon": coupon_list
    })


@coupon_api.route("/", methods=["POST"])
@admin_required
def add_coupon():
    user: Account = get_user_by_token()
    payload: dict = request.json
    require_list = ["close_time", "start_time", "price", "count", "name"]
    for requirement in require_list:
        if requirement not in payload.keys():
            return make_error_response(APIStatusCode.Wrong_Format, f"missing {requirement} column")

    create(
        publisher_id=user.id,
        close_time=payload["close_time"],
        start_time=payload["start_time"],
        describe=payload.get("describe"),
        price=payload["price"],
        count=payload["count"],
        name=payload["name"]
    )

    return jsonify({
        "status": 0
    })


@coupon_api.route("/<int:id>", methods=["GET"])
def get_coupon(id):
    coupon = find(id)

    if coupon is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason='coupon not exist')

    return jsonify({
        "status": 0,
        **coupon
    })


@coupon_api.route("/<int:id>", methods=["PUT"])
@admin_required
def edit_coupon(id):
    user: Account = get_user_by_token()
    coupon = find(id)

    if coupon is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason='coupon not exist')

    json: dict = request.json

    columns = {"start_time", "close_time", "price", "count", "name", "describe"}

    for key in json.keys():
        if key not in columns:
            make_error_response(APIStatusCode.Wrong_Format, reason='unknown format')
        else:
            coupon[key] = json[key]

    update(
        id=coupon["raw_id"],
        close_time=coupon["close_time"],
        start_time=coupon["start_time"],
        describe=coupon["describe"],
        price=coupon["price"],
        count=coupon["count"],
        name=coupon["name"]
    )

    return jsonify({
        "status": 0
    })


@coupon_api.route("/<int:id>", methods=["DELETE"])
@admin_required
def delete_coupon(id):
    coupon = find(id)

    if coupon is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason='coupon not exist')

    delete(id)

    return jsonify({
        "status": 0
    })


@coupon_api.route("/receive/<int:id>", methods=["POST"])
@login_required
def take(id):
    user: Account = get_user_by_token()
    coupon = find(id)

    if coupon is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason='coupon not exist')

    price = coupon.get("price")
    if user.bocoin < price:
        return make_error_response(APIStatusCode.CoinNotEnough, "user has not enough coin")

    count = coupon.get("count")
    remain_coin = user.bocoin - price
    receive(coupon.get("raw_id"), user.id, count, remain_coin)

    return jsonify({
        "status": 0,
    })


def get_list():
    cursor: sqlite3.Cursor = database.get_cursor()

    columns = ["raw_id", "publisher_id", "start_time", "close_time", "describe", "price", "count", "name"]
    return [dict(zip(columns, row)) for row in cursor.execute(f"""SELECT * FROM 'coupon_type'""")]


def find(id):
    cursor: sqlite3.Cursor = database.get_cursor()
    cursor.execute(f"""
            SELECT *
            FROM 'coupon_type'
            WHERE raw_id = {id}
        """)

    columns = ["raw_id", "publisher_id", "start_time", "close_time", "describe", "price", "count", "name"]
    data: tuple = cursor.fetchone()

    if data is None:
        return None

    return dict(zip(columns, data))


def create(publisher_id: str, start_time: str, close_time: str, price: int, count: int, name: str, describe: str = ''):
    connection = database.get_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        INSERT INTO coupon_type (publisher_id, start_time, close_time, price, count, name, describe)
        VALUES ('{publisher_id}', '{start_time}', '{close_time}', {price}, {count}, '{name}', '{describe}')
    """)

    connection.commit()


def receive(type_id, owner_id, count, price):
    connection = database.get_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
            INSERT INTO Coupon (type_id, owner_id)
            VALUES ('{type_id}', '{owner_id}')
        """)

    cursor.execute(f"""
        UPDATE account SET bocoin={price}
        WHERE id={owner_id}
    """)

    if count == 1:
        cursor.execute(f"""
            DELETE FROM coupon_type 
            WHERE raw_id={type_id}
        """)
    else:
        cursor.execute(f"""
            UPDATE coupon_type SET count = {count - 1}
            WHERE raw_id = {type_id}
        """)

    connection.commit()


def update(id: int, start_time: str, close_time: str, price: int, count: int, name: str, describe: str = ''):
    connection = database.get_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
                UPDATE coupon_type SET
                start_time = '{start_time}',
                close_time = '{close_time}',
                price = {price},
                count = {count},
                name = '{name}',
                describe='{describe}'
                WHERE raw_id={id}
            """)

    connection.commit()


def delete(id: int):
    connection = database.get_connection()
    cursor = connection.cursor()
    cursor.execute(f"""
        DELETE FROM coupon_type 
        WHERE raw_id={id}
    """)

    connection.commit()
