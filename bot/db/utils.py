from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from bot.settings import DBConfig
from .models import Base


class SessionFactory:
    """
    Класс для создания сессий подключения к базе дыннх
    """
    CONN_URL = DBConfig.conn_url()

    def __init__(self, ):
        self.engine = create_async_engine(self.CONN_URL, echo=DBConfig.ECHO)
        self.session = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )


async def create_db():
    """
    Функция для создания таблиц в базе данных
    :return:
    """
    engine = create_async_engine(DBConfig.conn_url(), echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
