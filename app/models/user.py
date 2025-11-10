from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable

from app.core.db import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    """Модель пользователя приложения.

    Наследуется от SQLAlchemyBaseUserTable и содержит
    стандартные поля для аутентификации и авторизации:
    - id: Уникальный идентификатор пользователя.
    - email: Email пользователя (уникальный).
    - hashed_password: Хешированный пароль.
    - is_active: Флаг активности пользователя.
    - is_superuser: Флаг суперпользователя.
    - is_verified: Флаг верификации email.
    """
