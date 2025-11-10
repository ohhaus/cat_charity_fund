import asyncio
import logging
from typing import Optional

from fastapi_users import exceptions

from app.core.config import settings
from app.core.db import get_async_session
from app.core.user import UserManager, get_user_db
from app.schemas.user import UserCreate


logger = logging.getLogger(__name__)


async def create_superuser(
    email: Optional[str] = None,
    password: Optional[str] = None,
) -> None:
    """Создает суперпользователя, если его нет.

    Args:
        email: Email (по умолчанию из настроек).
        password: Пароль (по умолчанию из настроек).
    """
    if email is None:
        email = settings.first_superuser_email
    if password is None:
        password = settings.first_superuser_password

    async for session in get_async_session():
        async with session:
            user_db = await get_user_db(session).__anext__()
            manager = UserManager(user_db)

            try:
                await manager.get_by_email(email)
                logger.info('Суперпользователь уже существует.')
                return
            except exceptions.UserNotExists:
                user_create = UserCreate(
                    email=email,
                    password=password,
                    is_superuser=True,
                    is_active=True,
                    is_verified=True,
                )
                user = await manager.create(user_create)
                logger.info(f'Суперпользователь {user.email} создан.')


async def create_first_superuser() -> None:
    """Создает первого суперпользователя из настроек."""
    await create_superuser(
        email=settings.first_superuser_email,
        password=settings.first_superuser_password,
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(create_first_superuser())
