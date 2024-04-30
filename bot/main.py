from datetime import datetime, timedelta

from pyrogram.types import Message
from pyrogram import Client, errors, filters

from bot.db.crud import UserCrud
from bot.db.models import UserStatus, User
from bot.settings import Config
from bot.db.utils import create_db

import asyncio

app = Client(
    name='my_account',
    api_id=Config.APP_ID,
    api_hash=Config.APP_HASH,
)

messages = {
    'msg1': 'Текст1',
    'msg2': 'Текст2',
    'msg3': 'Текст3',
}

triggers = ['прекрасно', 'ожидать']


def check_triggers(text: str) -> bool:
    """
    проверка сообщения пользователя на наличие тригеров
    :param text: сообщение пользователя
    :return:
    """
    for trigger in triggers:
        if trigger in text.lower():
            return True
    return False


@app.on_message(filters.private)
async def handle_message(client: Client, message: Message) -> None:
    """
    Функция для регистрации пользователей в воронку
    если пользователь уже был зарегистрирован идет проверка
    сообщения по ключевым словам
    :param client:
    :param message:
    :return:
    """
    u_crud = UserCrud()
    user_id = message.from_user.id
    if not await u_crud.get(pk=user_id):
        print('=' * 30)
        print('created')
        print('=' * 30)
        await u_crud.create(
            id=user_id
        )
    elif check_triggers(message.text):
        user: User = await u_crud.get(pk=user_id)
        user.status = UserStatus.finished.value
        user.status_updated_at = datetime.utcnow()
        user.stage = 1
        await u_crud.update(user)


async def stage_handler(user: User) -> None:
    """
    Функция проверяет статус пользователя и
    отправляет соответствующее сообщение
    при неудачной попытке отправить собщение пользователю
    устанавливается статус dead
    :param user: объект ОРМ
    :return:
    """
    u_crud = UserCrud()
    delta = datetime.utcnow() - user.last_message_at
    try:
        if user.stage == 3 and delta >= timedelta(days=1, hours=2):
            await app.send_message(user.id, messages['msg3'])
            user.last_message = datetime.utcnow()
            user.status = UserStatus.finished.value
            user.status_updated_at = datetime.utcnow()

        elif user.stage == 2 and delta >= timedelta(minutes=39):
            await app.send_message(user.id, messages['msg2'])
            user.stage = 3
            user.last_message = datetime.utcnow()

        elif user.stage == 1 and delta >= timedelta(minutes=6):
            await app.send_message(user.id, messages['msg1'])
            user.stage = 2
            user.last_message = datetime.utcnow()

    except errors.UserBlocked or errors.UserDeactivated:
        u_crud = UserCrud()
        user.status = UserStatus.dead.value
        user.status_updated_at = datetime.utcnow()
        await u_crud.update(user)

    await u_crud.update(user)


async def funnel() -> None:
    """
    воронка
    Перебирает в цикле всех пользователей со статусом alive
    :return:
    """
    while True:
        users = await UserCrud().get_all_alive()

        for user in users:
            await stage_handler(user)

        await asyncio.sleep(5)


async def main() -> None:
    """
    Функция запуска
    :return:
    """
    await create_db()
    await app.start()
    await funnel()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
