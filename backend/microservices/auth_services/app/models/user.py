from datetime import date
from uuid import uuid4

from sqlalchemy import BigInteger, Date, Enum, Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.schemas.enums import GenderEnum
from core.database import Base
from core.database.mixins import TimeStampMixin, UserAuditMixin


class User(Base, TimeStampMixin, UserAuditMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        default=uuid4,
        unique=True,
        nullable=False,
    )
    email: Mapped[str] = mapped_column(Unicode(320), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Unicode(128), nullable=False)
    username: Mapped[str] = mapped_column(Unicode(32), nullable=False, unique=True)
    profile_image_url: Mapped[str] = mapped_column(Unicode(150), nullable=True)
    phone_number: Mapped[str] = mapped_column(Unicode(20), nullable=True)
    first_name: Mapped[str] = mapped_column(Unicode(50), nullable=True)
    last_name: Mapped[str] = mapped_column(Unicode(50), nullable=True)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=True)
    gender: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum, create_type=False), nullable=True
    )

    def __repr__(self):
        return f"uuid={self.uuid}, username={self.username}, email={self.email})"

    def __str__(self):
        return self.__repr__()
