from flask import current_app, Blueprint, request, jsonify
from app.utils.auth_util import login_required
from app.utils.respons_util import make_error_response
from app.utils.enum_util import APIStatusCode, DrawType
from app.utils.auth_util import get_user_by_token
from app.utils import get_now
from app.database import db
from app.models import Item, PoolItem, Pool, OwnItem, Account
from sqlalchemy import func
import random

item_api = Blueprint("item_api", __name__)


@item_api.route('/getPoolItemList/<id>', methods=["GET"])
@login_required
def get_pool_item_list(id):
    pool_id = id

    pool: Pool = Pool.query.filter(
        Pool.id == id
    ).first()

    if pool is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason="The pool with given id is not exist!")

    items = db.session.query(Item.id, Item.name, Item.photo). \
        join(PoolItem, PoolItem.item_id == Item.id). \
        join(Pool, Pool.id == PoolItem.pool_id). \
        filter(Pool.id == pool_id).all()

    item_info = [
        dict(zip(['id', 'name', 'photo'], [row.id, row.name, row.photo]))
        for row in items
    ]

    return jsonify({
        "status": 0,
        "items": item_info
    })


@item_api.route('/drawCards', methods=['POST'])
@login_required
def draw_cards(*args, **kwargs):
    request_json: dict = request.json

    user: Account = get_user_by_token()

    if 'pool' not in request_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason='missing \'pool\' argument!')

    if 'type' not in request_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason='missing \'type\' argument!')

    pool_id: int = request_json['pool']
    type: DrawType = DrawType(request_json['type'])

    items: list = db.session.query(Item.id, Item.name, Item.photo). \
        join(PoolItem, PoolItem.item_id == Item.id). \
        join(Pool, Pool.id == PoolItem.pool_id). \
        filter(Pool.id == pool_id)

    picked_items = []
    # index_max = len(items) - 1
    index_max = items.count() - 1
    times = 1 if type == DrawType.single else 10
    
    picked_coin = 0
    if times == 1:
        picked_coin=10
    else: 
        picked_coin=90
    
    if user.bocoin>picked_coin:
        user.bocoin=user.bocoin-picked_coin

        now_time = get_now()
        for i in range(times):
            picked_index = random.randint(0, index_max)
            picked_item: Item = items[picked_index]
            picked_items.append(picked_item)

            own_item_count = OwnItem.query.filter(
                OwnItem.user_id == user.id,
                OwnItem.item_id == picked_item.id   
            ).count()
            if own_item_count == 0:
                db.session.add(OwnItem(
                    user_id=user.id,
                    item_id=picked_item.id,
                    get_time=str(now_time)
                ))
        db.session.commit()
        picked_item_info = [
        dict(zip(['id', 'name', 'photo'], [row.id, row.name, row.photo]))
        for row in picked_items
        ]

        return jsonify({
            "status": 0,
            "list": picked_item_info
        })

    else:
        user.bocoin=user.bocoin
        return jsonify({
            "status": 0,
            "list": []
        })

    


@item_api.route('/listPool', methods=['GET'])
@login_required
def list_pool(*args, **kwargs):
    pools_and_counts = db.session.query(Pool.id, Pool.name, Pool.photo, func.count(Item.id)). \
        join(PoolItem, PoolItem.pool_id == Pool.id, isouter=True). \
        join(Item, Item.id == PoolItem.item_id, isouter=True). \
        group_by(Pool.id).all()
    pools_info = [
        dict(zip(['id', 'name', 'photo', 'num'], row))
        for row in pools_and_counts
    ]
    return jsonify({
        "status": 0,
        "pools": pools_info
    })
