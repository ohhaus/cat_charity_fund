from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    """
    Схема для чтения данных пользователя.

    Используется для возврата информации о пользователе
    в API ответах.

    Attributes:
        id: Уникальный идентификатор пользователя
        email: Email адрес пользователя
        is_active: Флаг активности пользователя
        is_superuser: Флаг суперпользователя
        is_verified: Флаг верификации email адреса
    """

    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    """
    Схема для создания нового пользователя.

    Наследуется от BaseUserCreate и использует стандартные
    поля:
    - email: Email адрес (обязательное поле)
    - password: Пароль (обязательное поле)

    Note:
        Дополнительные поля валидации определены в
        BaseUserCreate.
    """


class UserUpdate(schemas.BaseUserUpdate):
    """
    Схема для обновления данных пользователя.

    Наследуется от BaseUserUpdate и позволяет обновлять:
    - email: Новый email адрес (опционально)
    - password: Новый пароль (опционально, из базового класса)

    Note:
        Все поля опциональны, обновляются только переданные
        значения.
    """

    email: Optional[EmailStr] = None
