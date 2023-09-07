from flask import Flask, render_template, redirect
from flask_socketio import SocketIO

socket = SocketIO(logger=True, engineio_logger=True, manage_session=False)


def create_app(config_filename=None):
    main = Flask(__name__, template_folder='./template', static_folder='./src')
    if config_filename is None:
        main.config.from_pyfile('config.py')
    else:
        main.config.from_pyfile(config_filename)
    from app.utils.setting_util import SettingUtil
    setter = SettingUtil(main.config)
    main.config["setting"] = setter.load_setting()
    main.config["verify_code"] = {}

    from app.utils.jwt_util import JWTGenerator
    main.config['jwt_gen']: JWTGenerator = JWTGenerator()

    from app.database import db, create_db
    db.init_app(main)

    # from app.models import models
    with main.app_context():
        create_db(flush=main.config['DBFLUSH'])
        # for i in main.config:
        # print("--->created DB!",main.config)

    from app.api.auth import auth_api
    from app.api.account import account_api
    from app.api.admin import admin_api
    from app.api.order import order_api
    from app.api.item import item_api
    from app.api.message import message_api

    main.register_blueprint(auth_api)
    main.register_blueprint(account_api)
    main.register_blueprint(admin_api)
    main.register_blueprint(order_api)
    main.register_blueprint(item_api)
    main.register_blueprint(message_api)

    from app.utils.email_util import send_verify_email
    from app.models import Account
    @main.route("/test")
    def test():
        user = Account.query.filter(Account.student_id == "109590027").first()
        send_verify_email(user)
        return "", 200

    from .websocket import chat
    socket.init_app(main)
    return main
