from uuid import uuid4

from sqlalchemy import BigInteger, Boolean, Unicode
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), default=uuid4, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(Unicode(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    username: Mapped[str] = mapped_column(Unicode(255), nullable=False, unique=True)
    profile_image_url: Mapped[str] = mapped_column(Unicode(255), nullable=True)
    phone_number: Mapped[str] = mapped_column(Unicode(255), nullable=True)

    def __repr__(self):
        return f"User(id={self.id}, uuid={self.uuid}, username={self.username}, email={self.email})"

    def __str__(self):
        return self.__repr__()
