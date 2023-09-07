import os

SECRET_KEY: bytes = os.urandom(24)
SQLALCHEMY_DATABASE_URI: str = "sqlite:///" + os.path.join(os.path.abspath("."), "bocountry.sqlite")
STORAGE_PATH: str = os.path.join(os.path.abspath("."), "storage")
SETTING_FILE: str = os.path.join(os.path.abspath("."), "setting.json")
DBFLUSH: bool = False
DEBUG: bool = True
