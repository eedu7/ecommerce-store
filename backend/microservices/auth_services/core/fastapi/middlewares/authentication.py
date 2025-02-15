from jose import JWTError
from starlette.authentication import AuthenticationBackend
from starlette.middleware.authentication import AuthenticationMiddleware as BaseAuthenticationMiddleware
from starlette.requests import HTTPConnection

from app.schemas.extras.current_user import CurrentUser
from core.cache import Cache
from core.exceptions import UnauthorizedException
from core.security import JWTHandler


class AuthBackend(AuthenticationBackend):
    async def authenticate(self, conn: HTTPConnection) -> tuple[bool, CurrentUser | None]:
        current_user = CurrentUser()
        authorization: str = conn.headers.get("Authorization")
        if not authorization:
            return False, current_user

        try:
            scheme, token = authorization.split(" ")
            if scheme.lower() != "bearer":
                return False, current_user
        except ValueError:
            return False, current_user

        if not token:
            return False, current_user

        try:
            payload = JWTHandler.decode(token)
            result = await Cache.backend.get(f"blacklist::{payload['jti']}")
            if result:
                raise UnauthorizedException("Invalid token")
            user_id = payload.get("user_id")
        except JWTError:
            return False, current_user

        current_user.id = user_id
        return True, current_user


class AuthenticationMiddleware(BaseAuthenticationMiddleware):
    pass
