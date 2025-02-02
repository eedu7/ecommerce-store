from uuid import uuid4

from sqlalchemy import UUID, BigInteger, Enum, ForeignKey, Unicode
from sqlalchemy.orm import Mapped, mapped_column

from app.models import User
from app.schemas.enums import AddressType
from core.database import Base
from core.database.mixins import TimeStampMixin, UserAuditMixin


class Address(Base, TimeStampMixin, UserAuditMixin):
    __tablename__ = "address"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, default=uuid4
    )

    user_uuid: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey(User.uuid), nullable=False
    )
    street_address: Mapped[str] = mapped_column(Unicode(255), nullable=False)
    city: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    state: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    zip_code: Mapped[str] = mapped_column(Unicode(20), nullable=True)
    country: Mapped[str] = mapped_column(Unicode(100), nullable=False)
    address_type: Mapped[AddressType] = mapped_column(
        Enum(AddressType, create_type=False), default=AddressType.SHIPPING
    )
