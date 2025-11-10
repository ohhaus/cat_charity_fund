from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)


class CRUDCharityProject(
    CRUDBase[CharityProject, CharityProjectCreate, CharityProjectUpdate]
):
    """CRUD для работы с благотворительными проектами.

    Предоставляет методы для создания, получения, обновления
    и удаления благотворительных проектов.
    """

    async def get_by_name(
        self, project_name: str, session: AsyncSession
    ) -> Optional[CharityProject]:
        """Получает проект по его имени.

        Args:
            project_name: Имя проекта для поиска.
            session: Асинхронная сессия базы данных.

        Returns:
            Найденный проект или None.
        """
        return await self.find_one_by(session, name=project_name)

    async def get_active_projects(
        self, session: AsyncSession
    ) -> Sequence[CharityProject]:
        """Получает все активные проекты.

        Проекты возвращаются отсортированными по дате создания.

        Args:
            session: Асинхронная сессия базы данных.

        Returns:
            Список активных проектов.
        """
        result = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date)
        )
        return result.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
