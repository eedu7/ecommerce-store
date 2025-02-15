from datetime import UTC, datetime
from uuid import UUID

from pydantic import EmailStr

from app.models import User
from app.repositories import UserRepository
from app.schemas.extras.token import Token
from core.cache import Cache
from core.config import config
from core.controller import BaseController
from core.database import Propagation, Transactional
from core.exceptions import (BadRequestException, NotFoundException,
                             UnauthorizedException)
from core.security import JWTHandler, PasswordHandler


class AuthController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    @Transactional(propagation=Propagation.REQUIRED)
    async def register(self, email: EmailStr, password: str, username: str) -> User:
        # Check if user exists with email
        user = await self.user_repository.get_by_email(email)

        if user:
            raise BadRequestException("User already exists with this email")

        # Check if user exists with username
        user = await self.user_repository.get_by_username(username)

        if user:
            raise BadRequestException("User already exists with this username")

        password = PasswordHandler.hash(password)

        return await self.user_repository.create(
            {
                "email": email,
                "password": password,
                "username": username,
                "last_login_at": datetime.now(),
            }
        )

    async def login(
        self, email: EmailStr, password: str, verify_password: bool = True
    ) -> tuple[Token, User]:
        user = await self.user_repository.get_by_email(email)

        if not user:
            raise BadRequestException("No user found")

        if not PasswordHandler.verify(user.password, password) and verify_password:
            raise BadRequestException("Invalid credentials")

        return Token(
            access_token=JWTHandler.encode(
                payload={"user_id": user.id},
                expire_minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
            ),
            refresh_token=JWTHandler.encode(
                payload={"sub": "refresh_token", "user_id": user.id},
                expire_minutes=config.JWT_REFRESH_TOKEN_EXPIRE_DAYS_IN_MINUTES,
            ),
            expires_in=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        ), user

    async def logout(self, access_token: str):
        payload = JWTHandler.decode(access_token)

        jti, exp = payload.get("jti", None), payload.get("exp", None)

        ttl = exp - int(datetime.now(UTC).timestamp())

        cache_key = f"blacklist::{jti}"

        await Cache.backend.set("1", cache_key, ttl=ttl)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_password(
        self, user: User, current_password: str, new_password: str
    ):
        from icecream import ic

        if not PasswordHandler.verify(user.password, current_password):
            raise BadRequestException("Current password is incorrect.")
        try:
            await self.user_repository.update_user(
                user,
                {"password": PasswordHandler.hash(new_password), "updated_by": User.id},
            )
            return True
        except Exception as e:
            raise BadRequestException(str(e))

    async def refresh_token(self, refresh_token: str) -> Token:
        refresh_token = JWTHandler.decode(refresh_token)
        if refresh_token.get("sub") != "refresh_token":
            raise UnauthorizedException("Invalid refresh token")

        user_id = refresh_token.get("user_id", None)

        return Token(
            access_token=JWTHandler.encode(
                payload={"user_id": user_id},
                expire_minutes=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES,
            ),
            refresh_token=JWTHandler.encode(
                payload={"sub": "refresh_token", "user_id": user_id},
                expire_minutes=config.JWT_REFRESH_TOKEN_EXPIRE_DAYS_IN_MINUTES,
            ),
            expires_in=config.JWT_ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        )
