from typing import Optional

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
    async def get_by_name(
        self, project_name: str, session: AsyncSession
    ) -> Optional[int]:
        project_id = await session.execute(
            select(CharityProject).where(CharityProject.name == project_name)
        )
        return project_id.scalar_one_or_none()

    async def get_active_projects(self, session: AsyncSession):
        active_projects_list = await session.execute(
            select(CharityProject)
            .where(CharityProject.fully_invested.is_(False))
            .order_by(CharityProject.create_date)
        )
        return active_projects_list.scalars().all()


charity_project_crud = CRUDCharityProject(CharityProject)
