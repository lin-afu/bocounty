import jwt
import secrets
from flask import Config


class JWTGenerator:

    def __init__(self, key: str = None) -> None:
        if key is None:
            self.secret_key = secrets.token_hex()
        else:
            self.secret_key = key

    def generate_token(self, values: dict) -> str:
        return jwt.encode(values, self.secret_key, algorithm='HS256')

    def check_token_valid(self, token: str) -> bool:
        try:
            data = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return True
        except:
            return False

    def get_token_detail(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=['HS256'])
