from sqlalchemy import UUID, BigInteger, Boolean, DateTime, ForeignKey, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from core.database.mixins import TimeStampMixin


class UserSecurity(Base, TimeStampMixin):
    __tablename__ = "user_security"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.uuid"), nullable=False
    )
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    email_verification_token: Mapped[str] = mapped_column(Unicode(255), nullable=True)
    reset_token: Mapped[str] = mapped_column(Unicode(255), nullable=True)
    reset_token_expiry: Mapped[DateTime] = mapped_column(DateTime, nullable=True)

    def __repr__(self):
        return f"id={self.id}, user_uuid={self.user_uuid}, email_verified={self.email_verified}"

    def __str__(self):
        return self.__repr__()
