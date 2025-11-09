from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class DonationBase(BaseModel):
    """
    Базовая схема пожертвования.

    Содержит общие поля для всех операций с пожертвованиями.
    Все поля опциональны для возможности частичного обновления.

    Attributes:
        comment: Комментарий пользователя к пожертвованию
        full_amount: Полная сумма пожертвования (больше 0)
    """

    comment: Optional[str] = Field(None, description='Комментарий')
    full_amount: Optional[int] = Field(
        None, gt=0, description='Полная сумма пожертвования'
    )

    class Config:
        extra = 'forbid'


class DonationCreate(DonationBase):
    """
    Схема для создания нового пожертвования.

    Сумма пожертвования обязательна для заполнения.
    Комментарий является опциональным полем.

    Attributes:
        full_amount: Сумма пожертвования (обязательное, > 0)
        comment: Комментарий к пожертвованию (опционально)
    """

    full_amount: int = Field(
        ..., gt=0, description='Обязательная сумма пожертвования'
    )


class DonationUpdate(DonationBase):
    """
    Схема для обновления существующего пожертвования.

    Все поля опциональны, обновляются только переданные
    значения.

    Attributes:
        comment: Новый комментарий (опционально)
        full_amount: Новая сумма пожертвования (опционально, > 0)

    Raises:
        ValueError: Если full_amount <= 0
    """

    @validator('full_amount')
    def validate_positive(cls, value: Optional[int]) -> Optional[int]:
        """
        Валидирует, что сумма пожертвования положительная.

        Args:
            value: Значение суммы для проверки

        Returns:
            Optional[int]: Валидное значение суммы или None

        Raises:
            ValueError: Если значение <= 0
        """
        if value is not None and value <= 0:
            raise ValueError('full_amount должно быть больше 0')
        return value


class DonationUserDB(DonationBase):
    """
    Схема для возврата данных пожертвования пользователю.

    Используется для отображения информации о пожертвованиях
    текущему пользователю. Не содержит служебной информации о
    распределении средств.

    Attributes:
        id: Уникальный идентификатор пожертвования
        full_amount: Сумма пожертвования
        comment: Комментарий к пожертвованию (если был указан)
        create_date: Дата и время создания пожертвования
    """

    id: int
    create_date: datetime
    full_amount: int

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    """
    Схема для возврата полных данных пожертвования из БД.

    Содержит все поля пожертвования, включая служебные данные
    о распределении средств по проектам. Доступна только
    суперпользователям.

    Attributes:
        id: Уникальный идентификатор пожертвования
        user_id: ID пользователя, сделавшего пожертвование
        full_amount: Полная сумма пожертвования
        invested_amount: Распределенная сумма (по умолчанию 0)
        fully_invested: Флаг полного распределения (False)
        comment: Комментарий к пожертвованию (если был указан)
        create_date: Дата и время создания пожертвования
        close_date: Дата полного распределения (None, если есть
                    остаток)
    """

    id: int
    user_id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None
    full_amount: int

    class Config:
        orm_mode = True
