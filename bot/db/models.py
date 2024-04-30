from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, Time, DateTime
from enum import Enum
from datetime import datetime


class Base(AsyncAttrs, DeclarativeBase):
    pass


class UserStatus(Enum):
    """
    Класс с возможными статусами пользователя
    """
    alive = 'alive'
    dead = 'dead'
    finished = 'finished'


class User(Base):
    """
    Модель пользователя
    """
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    status: Mapped[str] = mapped_column(default=UserStatus.alive.value)
    status_updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    stage: Mapped[int] = mapped_column(default=1)
    last_message_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    def __repr__(self):
        return f'<User ::  id: {self.id}; status: {self.status}>'
