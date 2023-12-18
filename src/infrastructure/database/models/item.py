import decimal
from typing import Any

from sqlalchemy import JSON, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database.base import AbstractModel
from src.infrastructure.database.models import partner  # noqa: F401

from .base import time_created


class Category(AbstractModel):
    __tablename__ = "categories"

    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)

    data: Mapped[dict[str, Any]] = mapped_column(JSON)
    items: Mapped[list["Item"]] = relationship(back_populates="category")

    def __repr__(self):
        return self.title


class Item(AbstractModel):
    __tablename__ = "items"

    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(nullable=False)
    data: Mapped[dict[str, Any]] = mapped_column(JSON)

    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    category: Mapped["Category"] = relationship(back_populates="items")

    partner_id: Mapped[int] = mapped_column(ForeignKey("partners.id", ondelete="CASCADE"))
    partner: Mapped["partner.Partner"] = relationship(back_populates="items")  # noqa: F811

    time_created: Mapped[time_created]

    def __repr__(self):
        return self.title
