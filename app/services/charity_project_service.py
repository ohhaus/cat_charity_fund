from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.charity_project import CharityProject
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectUpdate,
)
from app.services.investing import invest


class CharityProjectService:
    """
    Сервис для управления благотворительными проектами.

    Содержит бизнес-логику для создания, обновления и
    удаления проектов, а также автоматического инвестирования.
    """

    async def create_project(
        self,
        project_data: CharityProjectCreate,
        session: AsyncSession,
    ) -> CharityProject:
        """
        Создает новый проект и автоматически инвестирует средства.

        Args:
            project_data: Данные для создания проекта
            session: Асинхронная сессия базы данных

        Returns:
            CharityProject: Созданный и проинвестированный проект
        """
        new_project = await charity_project_crud.create(
            project_data, session, extra_data=None
        )

        active_donations = await donation_crud.get_active_donations(session)
        updated_donations = invest(
            target=new_project, sources=active_donations
        )

        session.add_all(updated_donations)
        await session.commit()
        await session.refresh(new_project)

        return new_project

    async def update_project(
        self,
        project: CharityProject,
        project_update: CharityProjectUpdate,
        session: AsyncSession,
    ) -> CharityProject:
        """
        Обновляет проект и проверяет статус финансирования.

        Если после обновления проект достиг полного финансирования,
        автоматически закрывает его.

        Args:
            project: Проект для обновления
            project_update: Данные для обновления
            session: Асинхронная сессия базы данных

        Returns:
            CharityProject: Обновленный проект
        """
        updated_project = await charity_project_crud.update(
            project, project_update, session
        )

        if self._is_fully_funded(updated_project):
            self._close_project(updated_project)

        active_donations = await donation_crud.get_active_donations(session)
        updated_donations = invest(
            target=updated_project, sources=active_donations
        )

        session.add_all(updated_donations)
        await session.commit()
        await session.refresh(updated_project)

        return updated_project

    async def delete_project(
        self,
        project: CharityProject,
        session: AsyncSession,
    ) -> CharityProject:
        """
        Удаляет благотворительный проект.

        Args:
            project: Проект для удаления
            session: Асинхронная сессия базы данных

        Returns:
            CharityProject: Удаленный проект
        """
        deleted_project = await charity_project_crud.remove(project, session)
        return deleted_project

    async def get_all_projects(
        self, session: AsyncSession
    ) -> List[CharityProject]:
        """
        Получает все благотворительные проекты.

        Args:
            session: Асинхронная сессия базы данных

        Returns:
            List[CharityProject]: Список всех проектов
        """
        projects = await charity_project_crud.get_multi(session)
        return list(projects)

    async def get_project_by_id(
        self, project_id: int, session: AsyncSession
    ) -> Optional[CharityProject]:
        """
        Получает проект по его ID.

        Args:
            project_id: ID проекта
            session: Асинхронная сессия базы данных

        Returns:
            Optional[CharityProject]: Найденный проект или None
        """
        return await charity_project_crud.get(project_id, session)

    def _is_fully_funded(self, project: CharityProject) -> bool:
        """
        Проверяет, достиг ли проект полного финансирования.

        Args:
            project: Проект для проверки

        Returns:
            bool: True, если проект полностью профинансирован
        """
        return project.invested_amount >= project.full_amount

    def _close_project(self, project: CharityProject) -> None:
        """
        Закрывает проект, устанавливая флаг и дату закрытия.

        Args:
            project: Проект для закрытия
        """
        project.fully_invested = True
        project.close_date = datetime.now(timezone.utc)


charity_project_service = CharityProjectService()
