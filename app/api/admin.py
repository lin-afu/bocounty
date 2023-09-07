from flask import Blueprint, request, jsonify, current_app
import uuid
from sqlalchemy import func
from app.utils.auth_util import admin_required
from app.utils.storage_util import StorgeCode, storage_photo, storage_delete
from app.utils.respons_util import make_error_response
from app.utils.enum_util import APIStatusCode, ModifyAction
from app.database import db
from app.models import Pool, Item, PoolItem

admin_api = Blueprint('admin_api', __name__)


@admin_api.route('/createPool', methods=['POST'])
@admin_required
def create_pool(*args, **kwargs):
    req_json: dict = request.json

    new_pool_id = uuid.uuid4().hex

    if "name" not in req_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'name' argument!")
    new_pool_name = request.json['name']

    if "photo" not in req_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'photo' argument!")
    new_pool_photo_path = storage_photo(req_json['photo'], StorgeCode.POOL)

    if new_pool_photo_path is None:
        return make_error_response(APIStatusCode.Wrong_Format, reason='the format of photo data is not correct')

    new_pool = Pool(
        id=new_pool_id,
        name=new_pool_name,
        photo=new_pool_photo_path,
    )
    db.session.add(new_pool)
    db.session.commit()
    return jsonify({
        "status": 0,
        "pool_id": new_pool_id
    })


@admin_api.route('/deletePool/<id>', methods=['POST'])
@admin_required
def delete_pool(id):
    pool: Pool = Pool.query.filter(
        Pool.id == id
    ).first()

    if pool is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason="pool isn't exist")
    else:
        db.session.delete(pool)
        db.session.commit()
        return jsonify({
            "status": 0
        })


@admin_api.route('/modifyPoolItem', methods=['POST'])
@admin_required
def modify_pool_item(*args, **kwargs):
    request_json: dict = request.json

    modify_items = request_json['modify_list']
    pool_id = request_json['id']

    check_pool: int = Pool.query.filter(
        Pool.id == request_json['id']
    ).count()

    if check_pool == 0:
        return make_error_response(APIStatusCode.InstanceNotExist, reason='Pool %d not exist' % pool_id)

    # db.session.begin()
    for info in modify_items:
        # print(info)
        check_item: int = Item.query.filter(
            Item.id == info['id']
        ).count()

        if check_item == 0:
            return make_error_response(APIStatusCode.InstanceNotExist,
                                       reason='Item %d not exist!' % request_json['id'])

        if ModifyAction(info['action']) == ModifyAction.Add:

            check_exist: int = PoolItem.query.filter(
                PoolItem.pool_id == pool_id,
                PoolItem.item_id == info['id']
            ).count()

            if check_exist == 0:
                db.session.add(PoolItem(
                    pool_id=pool_id,
                    item_id=info['id']
                ))
        else:
            del_pool_item: PoolItem = PoolItem.query.filter(
                PoolItem.pool_id == pool_id,
                PoolItem.item_id == info['id']
            ).first()

            if del_pool_item is not None:
                db.session.delete(del_pool_item)
    db.session.commit()
    return jsonify({
        "status": 0
    })


@admin_api.route('/listItem', methods=['GET'])
@admin_required
def list_item(*args, **kwargs):
    item_row = db.session.query(Item.id, Item.name, Item.photo, Item.type)
    item_list = [
        dict(zip(['id', 'name', 'photo', 'type'], row))
        for row in item_row
    ]
    return jsonify({
        "status": 0,
        "item_list": item_list
    })


@admin_api.route('/createItem', methods=['POST'])
@admin_required
def create_item(*args, **kwargs):
    req_json: dict = request.json

    new_item_id = uuid.uuid4().hex
    if "name" not in req_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'name' argument!")
    new_item_name = req_json['name']

    if "type" not in req_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'type' argument!")
    new_item_type = req_json['type']

    if "photo" not in req_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="missing 'photo' argument!")
    new_item_photo = storage_photo(req_json['photo'], StorgeCode.ITEM)

    new_item = Item(
        id=new_item_id,
        name=new_item_name,
        type=new_item_type,
        photo=new_item_photo
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({
        "status": 0,
        "id": new_item_id
    })


@admin_api.route('/deleteItem/<id>', methods=['POST'])
@admin_required
def del_item(id):
    item: Item = Item.query.filter(
        Pool.id == id
    ).first()

    if item is None:
        return make_error_response(APIStatusCode.InstanceNotExist, reason="The item with the given id is not exist!")
    else:
        db.session.delete(item)
        db.session.commit()
    return jsonify({
        "status": 0
    })


@admin_api.route('/modifyItemInfo', methods=['POST'])
@admin_required
def modify_item_info(*args, **kwargs):
    req_json: dict = request.json

    if "id" not in req_json.keys():
        return make_error_response(APIStatusCode.Wrong_Format, reason="The item with given id is not exist!")

    item = Item.query.filter(
        Item.id == req_json['id']
    ).first()

    if item is None:
        return '', 406

    keys = req_json.keys()
    if 'name' in keys:
        item.name = req_json['name']
    if 'type' in keys:
        item.type = req_json['type']
    if 'photo' in keys:
        old_path = item.photo[5:]
        storage_delete(old_path, StorgeCode.ITEM)
        new_path = storage_photo(req_json['photo'], StorgeCode.ITEM)
        if new_path is None:
            return '', 406
        item.photo = new_path
    db.session.commit()
    return jsonify({
        'status': 0
    })
