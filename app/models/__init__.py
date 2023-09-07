from sqlalchemy import Column, String, Integer, ForeignKey, DATETIME, BLOB
from app.database import db


class Account(db.Model):
    id = Column(String, primary_key=True, nullable=False)
    student_id = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    bocoin = Column(Integer, nullable=False, default=0)
    intro = Column(String, nullable=False, default='')
    mail_verify = Column(String, nullable=False, default=0)
    permission = Column(Integer, nullable=False, default=0)


class Item(db.Model):
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    photo = Column(String, nullable=False)
    # photo = Column(BLOB, nullable=False)
    type = Column(Integer, nullable=False)


class OwnItem(db.Model):
    user_id = Column(ForeignKey(Account.id), primary_key=True)
    item_id = Column(ForeignKey(Item.id), primary_key=True)
    get_time = Column(String, nullable=False)


class PickedItem(db.Model):
    user_id = Column(ForeignKey(Account.id), nullable=False, primary_key=True)
    item_id = Column(ForeignKey(Item.id), nullable=False, primary_key=True)


class Order(db.Model):
    id = Column(String, primary_key=True, nullable=False)
    status = Column(Integer, nullable=False, default=0)
    title = Column(String, nullable=False)
    intro = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    start_time = Column(String, nullable=False)
    close_time = Column(String, nullable=False)
    exec_time = Column(String, nullable=False)
    owner_id = Column(ForeignKey(Account.id, ondelete="CASCADE"))


class Involve(db.Model):
    chatroom_id = Column(String, primary_key=True)
    order_id = Column(ForeignKey(Order.id))
    involver_id = Column(ForeignKey(Account.id))


class Message(db.Model):
    raw_id = Column(Integer, primary_key=True, autoincrement=True)
    chatroom_id = Column(ForeignKey(Involve.chatroom_id), nullable=False)
    sender_id = Column(ForeignKey(Account.id), nullable=False)
    content = Column(String, nullable=False)
    time = Column(String, nullable=False)


class Pool(db.Model):
    id = Column(String, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    photo = Column(String, nullable=False)


class PoolItem(db.Model):
    pool_id = Column(ForeignKey(Pool.id), primary_key=True)
    item_id = Column(ForeignKey(Item.id), primary_key=True)


class Notification(db.Model):
    raw_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(ForeignKey(Account.id))
    type = Column(Integer)
    mention_id = Column(ForeignKey(Account.id))
    chatroom_id = Column(ForeignKey(Involve.chatroom_id))
    due_time = Column(String)
