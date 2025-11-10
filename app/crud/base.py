from typing import Any, Dict, Generic, Optional, Sequence, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import Base


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Базовый CRUD класс для работы с данными.

    Предоставляет стандартные операции создания, чтения,
    обновления и удаления.
    """

    def __init__(self, model: Type[ModelType]) -> None:
        """Инициализирует CRUD с указанной моделью.

        Args:
            model: Класс модели SQLAlchemy.
        """
        self.model = model

    async def create(
        self,
        obj_in: CreateSchemaType,
        session: AsyncSession,
        extra_data: Optional[Dict[str, Any]] = None,
    ) -> ModelType:
        """Создает новый объект в базе данных.

        Args:
            obj_in: Схема создания объекта.
            session: Асинхронная сессия базы данных.
            extra_data: Дополнительные данные для объекта.

        Returns:
            Созданный объект.
        """
        obj_data = obj_in.dict()
        if extra_data:
            obj_data.update(extra_data)
        db_obj = self.model(**obj_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def get(
        self, obj_id: int, session: AsyncSession
    ) -> Optional[ModelType]:
        """Получает объект по ID.

        Args:
            obj_id: ID объекта.
            session: Асинхронная сессия БД.

        Returns:
            Найденный объект или None.
        """
        result = await session.execute(
            select(self.model).where(self.model.id == obj_id)
        )
        return result.scalar_one_or_none()

    async def get_multi(self, session: AsyncSession) -> Sequence[ModelType]:
        """Получает все объекты из БД.

        Args:
            session: Асинхронная сессия БД.

        Returns:
            Список всех объектов.
        """
        result = await session.execute(select(self.model))
        return result.scalars().all()

    async def find_by(
        self, session: AsyncSession, **filter_kwargs: Any
    ) -> Sequence[ModelType]:
        """Находит объекты по заданным фильтрам.

        Args:
            session: Асинхронная сессия БД.
            **filter_kwargs: Критерии фильтрации.

        Returns:
            Список найденных объектов.

        Example:
            >>> await crud.find_by(session, user_id=1)
        """
        query = select(self.model)
        for key, value in filter_kwargs.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        result = await session.execute(query)
        return result.scalars().all()

    async def find_one_by(
        self, session: AsyncSession, **filter_kwargs: Any
    ) -> Optional[ModelType]:
        """Находит один объект по заданным фильтрам.

        Args:
            session: Асинхронная сессия БД.
            **filter_kwargs: Критерии фильтрации.

        Returns:
            Найденный объект или None.

        Example:
            >>> await crud.find_one_by(session, name='Project')
        """
        query = select(self.model)
        for key, value in filter_kwargs.items():
            if hasattr(self.model, key):
                query = query.where(getattr(self.model, key) == value)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    async def update(
        self,
        db_obj: ModelType,
        obj_in: UpdateSchemaType,
        session: AsyncSession,
    ) -> ModelType:
        """Обновляет существующий объект.

        Args:
            db_obj: Объект для обновления.
            obj_in: Схема обновления с новыми данными.
            session: Асинхронная сессия БД.

        Returns:
            Обновленный объект.
        """
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
        self, db_obj: ModelType, session: AsyncSession
    ) -> ModelType:
        """Удаляет объект из БД.

        Args:
            db_obj: Объект для удаления.
            session: Асинхронная сессия БД.

        Returns:
            Удаленный объект.
        """
        await session.delete(db_obj)
        await session.commit()
        return db_obj
