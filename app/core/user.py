import logging
from typing import AsyncGenerator, Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


logger = logging.getLogger(__name__)


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> AsyncGenerator[SQLAlchemyUserDatabase, None]:
    """
    Генератор базы данных пользователей.

    Args:
        session: Асинхронная сессия базы данных

    Yields:
        SQLAlchemyUserDatabase: База данных пользователей
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """
    Создает стратегию JWT для аутентификации.

    Returns:
        JWTStrategy: Стратегия JWT с настройками из конфигурации
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Менеджер пользователей с валидацией и событиями."""

    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        """
        Валидирует пароль пользователя.

        Args:
            password: Пароль для проверки
            user: Пользователь или схема создания пользователя

        Raises:
            InvalidPasswordException: Если пароль не валиден
        """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        """
        Обработчик события после регистрации пользователя.

        Args:
            user: Зарегистрированный пользователь
            request: HTTP-запрос (опционально)
        """
        logger.info(f'Пользователь {user.email} зарегистрирован.')


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> AsyncGenerator[UserManager, None]:
    """
    Генератор менеджера пользователей.

    Args:
        user_db: База данных пользователей

    Yields:
        UserManager: Менеджер пользователей
    """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
