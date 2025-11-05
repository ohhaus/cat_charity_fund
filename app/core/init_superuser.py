import asyncio

from app.core.db import get_async_session
from app.core.user import UserManager, get_user_db


SUPERUSER_EMAIL = 'root@admin.ru'
SUPERUSER_PASSWORD = 'root'


async def create_superuser():
    async for session in get_async_session():
        async with session:
            user_db = await get_user_db(session).__anext__()
            manager = UserManager(user_db)

            existing_user = await manager.get_by_email(SUPERUSER_EMAIL)
            if existing_user:
                print('Суперпользователь уже существует.')
                return

            user_dict = {
                'email': SUPERUSER_EMAIL,
                'password': SUPERUSER_PASSWORD,
                'is_superuser': True,
                'is_active': True,
                'is_verified': True,
            }

            user = await manager.create(user_dict)
            print(f'Суперпользователь {user.email} создан.')
