from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class AbstractModel(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
