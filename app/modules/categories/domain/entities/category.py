from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.domain.base_entity import BaseEntity


class Category(BaseEntity):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(255), nullable=False)
    slug: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    color: Mapped[str | None] = mapped_column(String(7), nullable=True)