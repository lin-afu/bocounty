from .. import socket
from flask_socketio import emit, send, ConnectionRefusedError, join_room, disconnect
from flask import session, request
from app.models import Involve
from app.utils.auth_util import check_login, get_user_by_token, login_required
from app.models import Account


@socket.on('join', namespace='/chat')
def join_chat(data):
    login_state = check_login()
    if login_state != 0:
        raise ConnectionRefusedError("require login!")

    if "chat_id" not in data.keys():
        disconnect()
        return
    user: Account = get_user_by_token()
    chatroom: Involve = Involve.query.filter(
        Involve.chatroom_id == data['chat_id']
    ).first()

    if chatroom is None:
        disconnect()
        return
    join_room(chatroom.chatroom_id)
