from flask import Blueprint, current_app, request, jsonify
from app.models import Account, Item, OwnItem, PickedItem
from app.database import db
from app.utils.auth_util import login_required, get_user_by_token
from app.utils.enum_util import APIStatusCode, EquipAction
from app.utils.respons_util import make_error_response
from app.utils.database import get_cursor, get_connection

account_api = Blueprint("acc_api", __name__)


@account_api.route('/getUserInfo/<id>', methods=['GET'])
@account_api.route('/getUserInfo', methods=['GET'])
@login_required
def get_user_info(id=None):
    if id is not None:
        user: Account = Account.query.filter(
            Account.id == id
        ).first()
    else:
        user: Account = get_user_by_token()

    if user is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason="user isn't exist")
    return jsonify({
        'status': 0,
        'id': user.id,
        'name': user.name,
        'intro': user.intro,
        'bocoin': user.bocoin
    })


@account_api.route('/checkUserVerify', methods=['GET'])
@login_required
def check_user_verify(*args, **kwargs):
    user: Account = get_user_by_token()
    if user is None:
        return make_error_response(APIStatusCode.NotLogin, reason='require login')

    verify_state = 1 if user.mail_verify == 1 else 0

    return jsonify({
        "status": 0,
        "verify": verify_state
    })


@account_api.route('/getUserItem', methods=['GET'])
@login_required
def get_user_item(*args, **kwargs):
    user: Account = get_user_by_token()

    item_list = db.session.query(Item.id, Item.name, Item.type, Item.photo). \
        join(OwnItem, OwnItem.item_id == Item.id). \
        join(Account, Account.id == OwnItem.user_id). \
        filter(Account.id == user.id).all()

    item_info = [
        dict(zip(["item_id", "name", "type", "photo"], row))
        for row in item_list
    ]

    return jsonify({
        'status': 0,
        "list": item_info
    })


@account_api.route('/getUserOutlook/<id>', methods=["GET"])
@account_api.route("/getUserOutlook", methods=["GET"])
@login_required
def get_user_outlook(id=None):
    if id is not None:
        user: Account = Account.query.filter(Account.id == id).first()
    else:
        user: Account = get_user_by_token()

    item_list = db.session.query(Item.id, Item.name, Item.photo, Item.type). \
        join(PickedItem, Item.id == PickedItem.item_id). \
        join(Account, Account.id == PickedItem.user_id). \
        filter(PickedItem.user_id == user.id). \
        all()

    items_info = [
        dict(zip(['id', 'name', 'photo', 'type'], row))
        for row in item_list
    ]

    return jsonify({
        "status": 0,
        "list": items_info
    })


@account_api.route('/getUserCoin', methods=['GET'])
@login_required
def get_user_coin(*args, **kwargs):
    user: Account = get_user_by_token()

    return jsonify({
        'status': 0,
        'num': user.bocoin
    })


@account_api.route('/changeUserInfo', methods=['POST'])
@login_required
def change_user_info(*args, **kwargs):
    user: Account = get_user_by_token()

    req_json: dict = request.json
    if 'name' in req_json.keys():
        user.name = req_json['name']
    if 'intro' in req_json.keys():
        user.intro = req_json['intro']
    db.session.commit()

    return jsonify({
        'status': 0
    })


@account_api.route('/changeUserOutlook', methods=['POST'])
@login_required
def change_user_outlook(*args, **kwargs):
    request_json: dict = request.json
    if "list" not in request_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason='missing \'list\' argument!')

    item_list = request_json['list']

    user: Account = get_user_by_token()
    for item in item_list:
        if "id" not in item.keys():
            return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'id' argument!")
        if 'action' not in item.keys():
            return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'action' argument!")

        item_id = item['id']
        action = EquipAction(item['action'])

        item_data: Item = Item.query.filter(
            Item.id == item_id
        ).first()

        if item_data is None:
            return make_error_response(APIStatusCode.InstanceNotExist, reason="The item with given id is not exist!")
        old_item: PickedItem = PickedItem.query.join(
            Item,
            Item.id == PickedItem.item_id
        ).filter(
            PickedItem.user_id == user.id,
            Item.type == item_data.type
        ).first()

        if old_item is not None:
            db.session.delete(old_item)

        if action == EquipAction.euqip:
            db.session.add(PickedItem(
                user_id=user.id,
                item_id=item_data.id
            ))
    db.session.commit()
    return jsonify({
        "status": 0
    })


@account_api.route('/listCoupon', methods=['GET'])
@login_required
def get_coupon_list():
    user: Account = get_user_by_token()
    cursor = get_cursor()

    column = ['id', 'name', 'describe', "close_time"]

    return jsonify({
        "status": 0,
        "coupon": [
            dict(zip(column, row)) for row in cursor.execute(f"""
                SELECT coupon_type.raw_id, coupon_type.name, coupon_type.describe, coupon_type.close_time
                FROM Coupon, coupon_type
                WHERE 
                    Coupon.type_id = coupon_type.raw_id AND
                    Coupon.owner_id = '{user.id}'
            """)
        ]
    })


@account_api.route("/useCoupon/<int:id>", methods=['POST'])
@login_required
def use_coupon(id):
    user: Account = get_user_by_token()
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(f"""
        SELECT *
        FROM coupon_type
        WHERE raw_id={id}
    """)

    data = cursor.fetchone()

    if data is None:
        return make_error_response(APIStatusCode.Wrong_Format, "coupon not found")
    column = ['raw_id', 'type_id', 'owner_id']

    coupon = dict(zip(column, data))

    if coupon.get("owner_id") == user.id:
        return make_error_response(APIStatusCode.InvalidAccess, "can't not access coupon")

    cursor.execute(f"""
        DELETE FROM coupon_type 
        WHERE raw_id={id}
    """)
    connection.commit()

    return jsonify({
        "status": 0
    })
