from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.sql import func


class AbstractModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)


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

    seller: Mapped['Seller'] = relationship(back_populates='user', uselist=False)

    def __repr__(self) -> str:
        return f'User<{self.id}> {self.name} + {self.surname}'


class Seller(AbstractModel):
    __tablename__ = 'sellers'

    user: Mapped['User'] = relationship(back_populates='seller', uselist=False)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    mobile: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    company_name: Mapped[str] = mapped_column(unique=True, nullable=False)
    company_description: Mapped[str] = mapped_column(Text, nullable=False)

    bank_name: Mapped[str] = mapped_column(nullable=False)
    tin: Mapped[str] = mapped_column(String(10), unique=True, nullable=False)     # Tax Identification Number
    bic: Mapped[str] = mapped_column(String(9), nullable=False)           # Bank Identified Code
    trrc: Mapped[str] = mapped_column(String(9), nullable=False)          # Tax Registration Reason Code
    an: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)           # AccountNumber

    passport_scan: Mapped[str] = mapped_column(String(130), nullable=False, unique=True)
    tc_scan: Mapped[str] = mapped_column(String(130), nullable=False, unique=True)       # Trademark Certificate

    additional: Mapped[str | None] = mapped_column(Text, nullable=True)
    time_created = mapped_column(DateTime(timezone=True), server_default=func.now())

    # If approved, is allowed to sell products
    is_approved: Mapped[bool] = mapped_column(default=False)

    def __repr__(self):
        return f'User<{self.user_id}> Seller<{self.id}>'
