import uuid

from flask import Blueprint, jsonify, request
from app.utils.auth_util import login_required, get_user_by_token
from app.utils.order_util import verify_create_form, CreateOrderPayload, ListOrderPayload
from app.utils.respons_util import make_error_response
from app.utils.enum_util import APIStatusCode, OrderListCode
from app.utils import get_now
from app.database import db
from app.models import Order, Account, Involve
from datetime import datetime, timedelta, timezone

order_api = Blueprint("order_api", __name__)


@order_api.route("/getUserOrder", methods=["GET"])
@login_required
def get_user_order():
    user: Account = get_user_by_token()

    list = db.session.query(Order.id, Order.status, Order.title, Order.start_time).filter(
        Order.owner_id == user.id
    ).all()

    res_list = [
        dict(zip(["id", "status", "title", "start_time"], row))
        for row in list
    ]

    return jsonify({
        "status": 0,
        "list": res_list
    })


@order_api.route("/getOpenOrder", methods=["GET"])
@login_required
def get_open_order():
    user: Account = get_user_by_token()

    orders = db.session.query(Order.id, Order.status, Order.title, Order.start_time).filter(
        Order.owner_id != user.id,
        Order.status == 0,
        ~db.session.query(Involve).filter(
            Involve.involver_id == user.id,
            Involve.order_id == Order.id,
        ).exists()
    ).all()

    order_info = [
        dict(zip(["id", "status", "title", "start_time"], row))
        for row in orders
    ]

    return jsonify({
        "status": 0,
        "list": order_info
    })


@order_api.route("/getOrderInvolve", methods=["GET"])
@login_required
def get_order_involve():
    user: Account = get_user_by_token()

    orders = db.session.query(Order.id, Order.status, Order.title, Order.start_time, Involve.chatroom_id).join(
        Involve,
        Involve.order_id == Order.id
    ).filter(
        Involve.involver_id == user.id
    ).all()

    order_info = [
        dict(zip(["id", "status", "title", "start_time", "chatroom_id"], row))
        for row in orders
    ]

    return jsonify({
        "status": 0,
        "list": order_info
    })


# @order_api.route("/getOrderList", methods=['GET'])
# @login_required
# def get_order_list(*args, **kwargs):
#     try:
#         request_json: dict = request.json
#         payload = ListOrderPayload(**request_json)
#     except TypeError:
#         return make_error_response(APIStatusCode.Wrong_Format, reason='wrong id data type')
#
#     user: Account = get_user_by_token()
#
#     typecode = OrderListCode(payload.type)
#     order_list = []
#     if typecode == OrderListCode.UsersOrder:
#         order_list = Order.query.filter(
#             Order.owner_id == user.id
#         ).all()
#
#     elif typecode == OrderListCode.InvolveInOrder:
#         involve_query = Involve.query.filter(
#             Involve.involver_id == user.id
#         ).subquery()
#
#         order_list = Order.query.join(
#             involve_query,
#             involve_query.c.order_id == Order.id
#         ).all()
#
#     elif typecode == OrderListCode.OpenOrder:
#         order_list = Order.query.join(
#             Involve,
#             Involve.order_id == Order.id,
#             isouter=True
#         ).filter(
#             Involve.involver_id != user.id,
#             Order.owner_id != user.id,
#             Order.status == 1
#         ).all()
#
#     order_info = [
#         dict(zip(['id', 'title', 'status'], [row.id, row.title, row.status]))
#         for row in order_list
#     ]
#     return jsonify({
#         "status": 0,
#         "orders": order_info
#     })


@order_api.route('/getOrderInfo/<id>', methods=["GET"])
@login_required
def get_order_info(id):
    order_info: (Order, str) = db.session.query(Order, Account.name). \
        join(Account, Account.id == Order.owner_id). \
        filter(Order.id == id). \
        first()

    if order_info is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason="The order with given id is not exist!")

    order = order_info[0]

    return jsonify({
        "status": 0,
        "title": order.title,
        "owner_id": order.owner_id,
        "owner_name": order_info[1],
        "start_time": order.start_time,
        "close_time": order.close_time,
        "exec_time": order.exec_time,
        "intro": order.intro
    })


@order_api.route('/changeOrderState', methods=['POST'])
@login_required
def change_order_state(*args, **kwargs):
    pass


@order_api.route('/createOrder', methods=['POST'])
@login_required
@verify_create_form
def create_order(*args, **kwargs):
    request_json: dict = request.json
    payload: CreateOrderPayload = CreateOrderPayload(**request_json)

    user: Account = get_user_by_token()

    if user.bocoin < payload.price:
        return make_error_response(APIStatusCode.CoinNotEnough, reason='coin not enough')

    user.bocoin = user.bocoin - payload.price
    db.session.commit()

    new_id = uuid.uuid4().hex
    new_order = Order(
        id=new_id,
        owner_id=user.id,
        title=payload.title,
        intro=payload.intro,
        price=payload.price,
        close_time=payload.close_time,
        exec_time=payload.exec_time,
        start_time=str(get_now())
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({
        "status": 0,
        "id": new_id
    })


@order_api.route('/deleteOrder/<id>', methods=["GET"])
@login_required
def del_order(id):
    user: Account = get_user_by_token()

    order: Order = Order.query.filter(
        Order.id == id
    ).first()

    if order is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason="The order with given id is not exist!")
    elif user.id == 1:
        db.session.delete(order)
        db.session.commit()
    elif order.owner_id != user.id:
        return make_error_response(APIStatusCode.InvalidAccess, reason="Access others Order!")
    else:
        db.session.delete(order)
        db.session.commit()
    return jsonify({
        "status": 0
    })


@order_api.route("/joinOrder/<id>", methods=["POST"])
@login_required
def join_order(id):
    order_id = id
    user: Account = get_user_by_token()

    involve: Involve = Involve.query.filter(
        Involve.involver_id == user.id,
        Involve.order_id == order_id
    ).first()

    if involve is not None:
        return make_error_response(APIStatusCode.AlreadyExec, reason="user has already join this order!")

    order: Order = Order.query.filter(
        Order.id == order_id
    ).first()

    if order is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason="order with given id is not exist!")

    if order.status != 0:
        return make_error_response(APIStatusCode.InvalidAccess, reason="Order has been closed!")

    new_chat_id = uuid.uuid4().hex

    new_involve = Involve(
        chatroom_id=new_chat_id,
        order_id=order_id,
        involver_id=user.id
    )

    db.session.add(new_involve)
    db.session.commit()

    return jsonify({
        "status": 0,
        "chat_id": new_chat_id
    })
