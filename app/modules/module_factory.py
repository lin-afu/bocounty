from flask import Config
from utils.jwt_util import JWTGenerator
from utils.crypto_utils import CryptoUtils


# class ModuleFactory(Enum):
#     AppConfig: Configure = current_app.config[FlaskConfigEnum.AppConfig]
#     JWTGenerator: JWTGenerator = current_app.config[FlaskConfigEnum.JWTGenerator]
#     Crypto: CryptoUtils = current_app.config[FlaskConfigEnum.Crypto]

class ModuleFactory:
    def __init__(self, config: Config):
        self.JWTGenerator = JWTGenerator(config)
        self.Crypto = CryptoUtils(config)

