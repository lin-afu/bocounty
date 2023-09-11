import sqlite3
from os import path, getcwd


def get_connection() -> sqlite3.Connection:
    db_path = path.join(getcwd(), 'bocountry.sqlite')
    return sqlite3.connect(db_path)


def get_cursor() -> sqlite3.Cursor:
    connection: sqlite3.Connection = get_connection()
    return connection.cursor()



class DB:
    def __init__(self):
        db_path = path.join(getcwd(), 'bocountry.sqlite')
        self.connection = sqlite3.connect(db_path)


