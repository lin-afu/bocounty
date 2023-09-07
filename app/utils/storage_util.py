import base64
import os
import uuid

from flask import current_app
from enum import Enum
import re


class StorgeCode(Enum):
    POOL = 'pool'
    ITEM = 'item'

def storage_photo(raw_data: str, code: StorgeCode) -> str:
# def storage_photo(raw_data: str, code: StorgeCode) -> str | None:
    split = re.split(r'[,;]\s*', raw_data)
    if len(split) != 3:
        return None
    data_type, encode_form, data = split

    if encode_form != 'base64':
        return None
    elif not re.match('^data:image/*', data_type):
        return None
    else:
        file_type = data_type[11:]
        photo_name = '%s.%s' % (uuid.uuid4().hex, file_type)
        decode_data = base64.b64decode(data)
        storage_write_bytes(photo_name, decode_data, code)
        return "%s/%s" % (code.value, photo_name)

# def transform_path(path: str):
#     if path[:8] == '/storage':
#         return path[9:]


def is_file_excite(filename: str, code: StorgeCode):
    file_path = full_path(filename, code)
    return os.path.exists(file_path)


def storage_delete(filename: str, code: StorgeCode):
    file_path = full_path(filename, code)
    if is_file_excite(file_path, code):
        os.remove(file_path)


def storage_write_bytes(filename: str, data: bytes, code: StorgeCode) -> None:
    file_path = full_path(filename, code)
    with open(file_path, 'wb') as f:
        f.write(data)


def storage_write(filename: str, data: str, code: StorgeCode) -> None:
    file_path = full_path(filename, code)
    with open(file_path, 'w') as f:
        f.write(data)


def full_path(filename: str, code: StorgeCode):
    return os.path.join(current_app.config['STORAGE_PATH'], code.value, filename)
