from sqlalchemy import BigInteger, String
from sqlalchemy.orm import mapped_column, Mapped

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class UsersOrm(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(String(16), nullable=True)
    phone_number: Mapped[str] = mapped_column(nullable=True)
    member: Mapped[bool] = mapped_column(default=False)