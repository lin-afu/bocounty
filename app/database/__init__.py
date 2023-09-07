import uuid

from flask import current_app
import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def check_db():
    full_file_path = os.path.join(os.getcwd(), 'bocountry.sqlite')
    print(full_file_path, os.path.exists(full_file_path))
    print("check")
    return os.path.exists(full_file_path)


def create_default_admin(student_id="123456789", name="預設管理員"):
    print("created Admin!")
    from app.models import Account
    admin_id = uuid.uuid4().hex
    db.session.add(Account(
        id=admin_id,
        student_id=student_id,
        name=name,
        password='8c6976e5b5410415bde908bd4dee15dfb167a9c873fc4bb8a81f6f2ab448a918',  # admin
        permission=1,
        bocoin=100
    ))
    db.session.commit()
    print(student_id,admin_id)


def create_db(flush=False):
    # print("you are in here!")
    # print("123123123",db)
    if flush or (not check_db()):
        with current_app.app_context():
            if flush:
                print('flush database')
                db.drop_all()
            print('create database')
            db.create_all()
            # create_default_admin()
    if flush:
        create_default_admin()
