from datetime import UTC, datetime
from typing import Any

from app.models import User
from core.repository import BaseRepository


class UserRepository(BaseRepository[User]):
    """
    User repository provides all the database operations for the User model.
    """

    async def get_by_username(
        self, username: str, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by username.

        :param username: Username.
        :param join_: Join relations.
        :return: User.
        """
        query = self._query(join_)
        query = query.filter(User.username == username)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    async def get_by_email(
        self, email: str, join_: set[str] | None = None
    ) -> User | None:
        """
        Get user by email.

        :param email: Email.
        :param join_: Join relations.
        :return: User.
        """
        query = self._query(join_)
        query = query.filter(User.email == email)

        if join_ is not None:
            return await self.all_unique(query)

        return await self._one_or_none(query)

    async def update_last_login(self, user: User) -> None:
        """
        Update the last login time of the user.

        :param user: The user instance.
        :return: None.
        """
        user.last_login_at = datetime.now(UTC)
        self.session.add(user)

    async def update_user(self, user: User, attributes: dict[str, Any]) -> User:
        """
        Update user details.

        :param user: User instance.
        :param kwargs: User details.
        :return: User.
        """
        for field, value in attributes.items():
            if hasattr(user, field):
                setattr(user, field, value)
        self.session.add(user)
