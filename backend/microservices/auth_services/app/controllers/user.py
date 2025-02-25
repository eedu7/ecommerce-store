from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController
from core.database import Propagation, Transactional
from core.exceptions import NotFoundException


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def get_by_username(self, username: str) -> User:
        return await self.user_repository.get_by_username(username)

    async def get_by_email(self, email: str) -> User:
        return await self.user_repository.get_by_email(email)

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[User]:
        """
        Returns a list of users
        :param skip: Number of records to skip (for pagination).
        :param limit: Number of records to return.
        :return: List of active users.
        """
        filters = {"deleted_at": None, "deleted_by": None}
        return await self.user_repository.get_all(
            skip=skip, limit=limit, filters=filters
        )

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_last_login(self, email: str) -> None:
        user = await self.get_by_email(email)
        if user:
            await self.user_repository.update_user(
                user, {"last_login_at": datetime.now(timezone.utc).replace(tzinfo=None)}
            )

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_user(self, user_uuid: UUID, data: dict[str, Any]) -> bool:
        user = await self.get_by_uuid(user_uuid)
        if user:
            await self.user_repository.update_user(
                user,
                {
                    **data,
                    "updated_by": user.id,
                },
            )
            return True
        return False

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_profile_image(self, user_uuid: UUID, image_url: str) -> bool:
        user = await self.get_by_uuid(user_uuid)
        if user:
            await self.user_repository.update_user(
                user,
                {
                    "profile_image_url": image_url,
                    "updated_by": user.id,
                },
            )
            return True
        return False

    @Transactional(propagation=Propagation.REQUIRED)
    async def delete_user(self, user_uuid: UUID) -> bool:
        user = await self.get_by_uuid(user_uuid)
        if not user:
            raise NotFoundException("User not found")
        await self.user_repository.update_user(
            user,
            {
                "deleted_at": datetime.now(timezone.utc).replace(tzinfo=None),
                "deleted_by": user.id,
            },
        )
        return True
