import asyncio

from fastapi_users import exceptions

from app.core.db import get_async_session
from app.core.user import UserManager, get_user_db
from app.schemas.user import UserCreate


SUPERUSER_EMAIL = 'root@admin.ru'
SUPERUSER_PASSWORD = 'root'


async def create_superuser(
    email: str = SUPERUSER_EMAIL,
    password: str = SUPERUSER_PASSWORD,
):
    """Создает суперпользователя, если его нет."""
    async for session in get_async_session():
        async with session:
            user_db = await get_user_db(session).__anext__()
            manager = UserManager(user_db)

            try:
                # Проверяем, существует ли пользователь
                await manager.get_by_email(email)
                print('Суперпользователь уже существует.')
                return
            except exceptions.UserNotExists:
                # Пользователь не найден — создаем
                user_create = UserCreate(
                    email=email,
                    password=password,
                    is_superuser=True,
                    is_active=True,
                    is_verified=True,
                )
                user = await manager.create(user_create)
                print(f'Суперпользователь {user.email} создан.')


if __name__ == '__main__':
    asyncio.run(create_superuser())
