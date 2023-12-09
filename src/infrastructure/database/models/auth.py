from sqlalchemy import Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from src.infrastructure.database.base import AbstractModel

from . import partner


class User(AbstractModel):
    __tablename__ = 'users'

    name: Mapped[str] = mapped_column(String(50), nullable=False)
    surname: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(String(70), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(100), nullable=False)

    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())

    email_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_seller: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_stuff: Mapped[bool] = mapped_column(default=False)

    seller: Mapped['partner.Partner'] = relationship(back_populates='user', uselist=False)
    tokens: Mapped['Token'] = relationship(back_populates='user')


class Token(AbstractModel):
    __tablename__ = 'tokens'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    user: Mapped['User'] = relationship(back_populates='tokens')

    access_token: Mapped[str] = mapped_column(unique=True, index=True)
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return self.access_token
