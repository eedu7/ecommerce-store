from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, declared_attr, mapped_column


class UserAuditMixin:
    """Mixin class to add created_by, updated_by, deleted_by to models."""

    @declared_attr
    def created_by(cls) -> Mapped[BigInteger]:
        return mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    @declared_attr
    def updated_by(cls) -> Mapped[BigInteger]:
        return mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)

    @declared_attr
    def deleted_by(cls) -> Mapped[BigInteger | None]:
        return mapped_column(BigInteger, ForeignKey("users.id"), nullable=True)
