from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column
from app.core.db import Base
from app.core.mixins import UUIDMixin, TimestampMixin

class Society(UUIDMixin, TimestampMixin, Base):
    __tablename__ = "societies"

    name: Mapped[str] = mapped_column(String(200))
    address: Mapped[str | None] = mapped_column(String(500))