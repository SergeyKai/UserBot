import os
from dataclasses import dataclass

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())


@dataclass
class DBConfig:
    """
    Конфигурации базы данных
    """
    HOST: str = os.environ.get('HOST')
    PORT: int = os.environ.get('PORT')
    USER: str = os.environ.get('USER')
    PASSWORD: str = os.environ.get('PASSWORD')
    DATABASE: str = os.environ.get('DATABASE')
    ECHO: bool = True if os.environ.get('ECHO') == 'True' else False

    @classmethod
    def conn_url(cls):
        return f'postgresql+asyncpg://{cls.USER}:{cls.PASSWORD}@{cls.HOST}:{cls.PORT}/{cls.DATABASE}'


@dataclass
class Config:
    APP_ID: int = os.environ.get('APP_ID')
    APP_HASH: str = os.environ.get('APP_HASH')
