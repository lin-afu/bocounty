from dataclasses import dataclass
from flask import request
from functools import wraps
from datetime import datetime, timedelta, timezone
import re
from app.utils.enum_util import APIStatusCode
from app.utils.respons_util import make_error_response
from app.utils import get_now


@dataclass
class CreateOrderPayload:
    title: str
    close_time: str
    exec_time: str
    price: int
    intro: str

    def __post_init__(self):
        self.close_time = str(datetime.fromisoformat(self.close_time) + timedelta(days=1, seconds=-1))
        print(type(datetime.fromisoformat(self.close_time)))
        print(type(get_now()))
        if datetime.fromisoformat(self.close_time) < get_now():
            raise TypeError

        if self.exec_time != 'None':
            self.exec_time = str(datetime.fromisoformat(self.exec_time))
            if datetime.fromisoformat(self.exec_time) < get_now():
                print('exec_time too early')
                raise TypeError
            if datetime.fromisoformat(self.exec_time) < datetime.fromisoformat(self.close_time):
                print('exec_time earlier close')
                raise TypeError

        if self.price < 1:
            raise TypeError

    @property
    def get_close_time(self) -> datetime:
        return datetime.fromisoformat(self.close_time)

    @property
    def get_exec_time(self) -> datetime:
    # def get_exec_time(self) -> datetime | None:
        return None if self.exec_time == 'None' else datetime.fromisoformat(self.exec_time)


@dataclass
class ListOrderPayload:
    type: int

    def __post_init__(self):
        if (self.type < 0) or (self.type > 3):
            raise TypeError


def verify_create_form(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        request_json: dict = request.json

        if request_json is None:
            return make_error_response(APIStatusCode.Wrong_Format, reason="request body isn't exist")

        try:
            payload = CreateOrderPayload(**request_json)
        except TypeError:
            return make_error_response(APIStatusCode.Wrong_Format, reason="argument type wrong")
        except ValueError:
            return make_error_response(APIStatusCode.Wrong_Format, reason='argument format wrong')

        return func(*args, **kwargs)

    return wrap
