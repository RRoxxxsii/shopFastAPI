from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.database.base import AbstractModel

from . import auth


class Seller(AbstractModel):
    __tablename__ = 'sellers'

    user: Mapped['auth.User'] = relationship(back_populates='seller', uselist=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    mobile: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    company_description: Mapped[str] = mapped_column(Text, nullable=False)

    bank_name: Mapped[str] = mapped_column(nullable=False)
    tin: Mapped[str] = mapped_column(String(12), unique=True, nullable=False)     # Tax Identification Number
    bic: Mapped[str] = mapped_column(String(9), nullable=False)           # Bank Identified Code
    trrc: Mapped[str] = mapped_column(String(9), nullable=False)          # Tax Registration Reason Code
    an: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)           # AccountNumber

    additional: Mapped[str | None] = mapped_column(Text, nullable=True)
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())

    # If approved, is allowed to sell products
    is_approved: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'User<{self.user_id}> Seller<{self.id}>'
