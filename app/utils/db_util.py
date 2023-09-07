import pymysql
from Enums.FlaskConfigEnum import FlaskConfigEnum as ConfigEnum
from flask import Config


class DatabaseUtils:
    def __init__(self, config: Config):
        db_setting = config[ConfigEnum.SQL]
        self.database_host = db_setting["Host"]
        self.database_User = db_setting["User"]
        self.database_Password = db_setting["Password"]
        self.database_Database = db_setting["Database"]
        self.conn = pymysql.connect(host=self.database_host,
                                    user=self.database_User,
                                    password=self.database_Password,
                                    database=self.database_Database)

    def command_excute(self, command: str, param: dict) -> list:
        """
            這個函數可以讓你使用 MySQL 的指令，並將回傳結果轉成一個 dict 回傳

            param:
                - command: MySQL 的指令，需要可以正常運作
                - param: 參數化的參數
            return:
                - 一個包含結果的 dict。
        """
        with self.conn.cursor() as cursor:
            cursor.execute(command, param)
            self.conn.commit()
            if cursor.description is not None:
                field_name = [name[0] for name in cursor.description]
                result = cursor.fetchall()
                result_list = []
                for data in result:
                    result_list.append(dict(zip(field_name, list(data))))
                return result_list
            else:
                return []
