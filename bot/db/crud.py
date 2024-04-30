from typing import Union, Sequence

from sqlalchemy import select

from bot.db.models import User, UserStatus
from bot.db.utils import SessionFactory


class BaseCrud:
    """
    model: must be overwriting in subclass. Must be cls of model ORM
    model: должен быть переопределен в классах наследниках. Должен быть классом модели ОРМ
    """
    model = None

    async def get(self, pk: int) -> model:
        """
        :param pk: int: id of instance of model
        :param pk: int: Идентификатор записи в БД.
        :return: object of model orm or None
        :return: Экземпляр модели ORM, если объект найден, или None, если объект не найден.
        """
        async with SessionFactory().session() as session:
            stmt = select(self.model).where(self.model.id == pk)
            return await session.scalar(stmt)

    async def all(self) -> Sequence:
        """
        :return: list of objects model
        :return: Список объектов модели
        """
        async with SessionFactory().session() as session:
            stmt = select(self.model)
            result = await session.scalars(stmt)
            return result.all()

    async def create(self, **kwargs) -> Union[model, None]:
        """
        :param kwargs: dict: arguments for creation new instance of model
        :param kwargs: dict: аргументы для создания нового экземпляра модели
        :return: the instance model, if successfully created and saved, else None
        :return: экземпляр модели, если успешно создан и сохранен, иначе None.
        """
        async with SessionFactory().session() as session:
            try:
                obj = self.model(**kwargs)
                session.add(obj)
                await session.commit()
                return obj
            except Exception as e:
                print(e)
                await session.rollback()
                return None

    async def update(self, obj) -> model:
        """
        :param obj: object ORM
        :param obj: объект ORM
        """
        async with SessionFactory().session() as session:
            session.add(obj)
            await session.commit()

    async def delete(self, pk: int) -> None:
        """
        :param pk: int: id of instance of model
        :param pk: int: Идентификатор записи в БД.
        :return: None
        """
        async with SessionFactory().session() as session:
            obj = await self.get(pk)
            await session.delete(obj)
            await session.commit()


class UserCrud(BaseCrud):
    """
    CRUD для взаимодействия с таблицей пользователей
    """
    model = User

    async def get_all_alive(self) -> Sequence:
        """
        Метод для получения пользователей со статусов alive
        :return:
        """
        async with SessionFactory().session() as session:
            stmt = select(self.model).where(self.model.status == UserStatus.alive.value)
            result = await session.scalars(stmt)
            return result.all()
