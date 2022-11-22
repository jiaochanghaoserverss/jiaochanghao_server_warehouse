import jwt
import time
from django.conf import settings


class InvalidJWTPayload(Exception):
    pass


class InvalidJWTSign(Exception):
    pass


class JWTUtil:

    def __init__(self, secret_key: str, headers: dict = None):
        self.__secret_key = secret_key
        self.payload_class = settings.APP_PAYLOAD
        self.headers = headers

    def encode(self, payload: dict):
        d = self.get_available_payload(payload)
        return jwt.encode(d, self.__secret_key, headers=self.headers)

    def decode(self, token: str) -> settings.JWT_PAYLOAD:
        try:
            d = jwt.decode(token, self.__secret_key, verify=True)
        except jwt.ExpiredSignatureError:
            raise InvalidJWTSign('token expired')
        except (jwt.InvalidSignatureError, jwt.exceptions.DecodeError):
            raise InvalidJWTSign
        return self.payload_class(**d)

    def get_available_payload(self, payload):
        try:
            d = self.payload_class(**payload)
            return d.get_available()
        except:
            raise InvalidJWTPayload


class AppTokenService:
    jwt_util = JWTUtil(settings.JWT_SECRET_KEY)

    @classmethod
    def create_token(cls, user_id: int, expire=settings.JWT_EXPIRE_IN):
        expire_at = int(time.time()) + expire
        return cls.jwt_util.encode({'user_id': user_id, 'exp': expire_at})

    @classmethod
    def get_payload(cls, token):
        return cls.jwt_util.decode(token)
