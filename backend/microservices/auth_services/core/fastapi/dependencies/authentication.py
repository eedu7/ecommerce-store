from fastapi import Depends, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from core.exceptions import CustomException


class AuthenticationRequiredException(CustomException):
    code = status.HTTP_401_UNAUTHORIZED
    error_code = status.HTTP_401_UNAUTHORIZED
    message = "Authentication required"


class AuthenticationRequired:
    def __init__(self, token: HTTPAuthorizationCredentials = Depends(HTTPBearer)):
        if not token:
            raise AuthenticationRequiredException()
