from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    """
    Базовая схема благотворительного проекта.

    Содержит общие поля для всех операций с проектами.
    Все поля опциональны для возможности частичного обновления.

    Attributes:
        name: Название проекта (максимум 100 символов)
        description: Описание проекта и его целей
        full_amount: Требуемая сумма для проекта (больше 0)
    """

    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = 'forbid'


class CharityProjectCreate(CharityProjectBase):
    """
    Схема для создания нового благотворительного проекта.

    Все поля обязательны для заполнения при создании проекта.

    Attributes:
        name: Название проекта (обязательное, 1-100 символов)
        description: Описание проекта (обязательное, минимум 1)
        full_amount: Требуемая сумма (обязательное, больше 0)

    Raises:
        ValueError: Если name или description содержат только пробелы
    """

    name: str = Field(..., max_length=100, min_length=1)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    @validator('name', 'description')
    def validate_not_empty(cls, value: Optional[str]) -> str:
        """
        Валидирует, что поля name и description не пустые.

        Args:
            value: Значение поля для проверки

        Returns:
            str: Валидное значение поля

        Raises:
            ValueError: Если значение содержит только пробелы
        """
        if value is not None and not value.strip():
            raise ValueError('Поле не может быть пустым')
        return value


class CharityProjectUpdate(CharityProjectBase):
    """
    Схема для обновления существующего проекта.

    Все поля опциональны, обновляются только переданные
    значения. Нельзя обновлять закрытые проекты.

    Attributes:
        name: Новое название проекта (опционально, макс 100)
        description: Новое описание проекта (опционально)
        full_amount: Новая требуемая сумма (опционально, > 0)

    Raises:
        ValueError: Если name или description только пробелы
        ValueError: Если full_amount <= 0
    """

    @validator('name', 'description')
    def validate_not_empty(cls, value: Optional[str]) -> Optional[str]:
        """
        Валидирует, что поля name и description не пустые.

        Args:
            value: Значение поля для проверки

        Returns:
            Optional[str]: Валидное значение поля или None

        Raises:
            ValueError: Если значение содержит только пробелы
        """
        if value is not None and not value.strip():
            raise ValueError('Поле не может быть пустым')
        return value

    @validator('full_amount')
    def validate_positive(cls, value: Optional[int]) -> Optional[int]:
        """
        Валидирует, что требуемая сумма положительная.

        Args:
            value: Значение суммы для проверки

        Returns:
            Optional[int]: Валидное значение суммы или None

        Raises:
            ValueError: Если значение меньше или равно 0
        """
        if value is not None and value <= 0:
            raise ValueError('full_amount должно быть больше 0')
        return value


class CharityProjectDB(CharityProjectBase):
    """
    Схема для возврата данных проекта из базы данных.

    Содержит все поля проекта, включая служебные данные о
    финансировании и датах создания/закрытия.

    Attributes:
        id: Уникальный идентификатор проекта
        name: Название проекта
        description: Описание проекта
        full_amount: Требуемая сумма для проекта
        invested_amount: Уже собранная сумма (по умолчанию 0)
        fully_invested: Флаг полного финансирования (False)
        create_date: Дата и время создания проекта
        close_date: Дата закрытия (None, если проект активен)
    """

    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None
    name: str
    description: str
    full_amount: int

    class Config:
        orm_mode = True
