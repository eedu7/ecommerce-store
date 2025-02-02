from sqlalchemy import DateTime, func
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """Mixin class to add created_at, updated_ay, deleted_at timestamp to models."""

    @declared_attr
    def created_at(cls) -> Mapped[DateTime]:
        return mapped_column(DateTime, default=func.now())

    @declared_attr
    def updated_at(cls) -> Mapped[DateTime]:
        return mapped_column(DateTime, default=func.now(), onupdate=func.now())

    @declared_attr
    def deleted_at(cls) -> Mapped[DateTime | None]:
        return mapped_column(DateTime, nullable=True)
