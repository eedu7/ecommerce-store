from datetime import datetime, timedelta
from http import HTTPStatus

from jose import ExpiredSignatureError, JWTError, jwt

from core.config import config
from core.exceptions import CustomException


class JWTDecodeError(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    message = "Invalid Token"


class JWTExpiredError(CustomException):
    code = HTTPStatus.UNAUTHORIZED
    message = "Invalid Token"


class JWTHandler:
    secret_key = config.JWT_SECRET_KEY
    algorithm = config.JWT_ALGORITHM
    expired_minutes = config.JWT_EXPIRE_MINUTES
    expire = datetime.utcnow() + timedelta(minutes=expired_minutes)

    @staticmethod
    def encode(payload: dict) -> str:
        payload.update({"exp": JWTHandler.expire})
        return jwt.encode(
            payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm
        )

    @staticmethod
    def decode(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
            )
        except ExpiredSignatureError:
            raise JWTExpiredError("Token has expired")
        except JWTError as e:
            raise JWTDecodeError() from e

    @staticmethod
    def decode_expire(token: str) -> dict:
        try:
            return jwt.decode(
                token,
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
                options={"verify_exp": False},
            )
        except JWTError as e:
            raise JWTDecodeError() from e
