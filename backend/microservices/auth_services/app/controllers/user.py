from datetime import datetime
from typing import Any, Dict
from uuid import UUID

from app.models import User
from app.repositories import UserRepository
from core.controller import BaseController
from core.database import Propagation, Transactional


class UserController(BaseController[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(model=User, repository=user_repository)
        self.user_repository = user_repository

    async def get_by_username(self, username: str) -> User:
        return await self.user_repository.get_by_username(username)

    async def get_by_email(self, email: str) -> User:
        return await self.user_repository.get_by_email(email)

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_last_login(self, email: str) -> None:
        user = await self.get_by_email(email)
        if user:
            await self.user_repository.update_user(
                user, {"last_login_at": datetime.utcnow()}
            )

    @Transactional(propagation=Propagation.REQUIRED)
    async def update_user(self, user_uuid: UUID, data: Dict[str, Any]) -> bool:
        user = await self.get_by_uuid(user_uuid)
        if user:
            await self.user_repository.update_user(
                user,
                {
                    **data,
                    "updated_by": user.id,
                    "updated_at": datetime.utcnow(),
                },
            )
            return True
        return False
