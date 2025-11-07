from typing import Optional

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def check_name_duplicate(
    name: str,
    session: AsyncSession,
    current_project_id: Optional[int] = None,
) -> None:
    existing_project = await charity_project_crud.get_by_name(name, session)
    if existing_project and existing_project.id != current_project_id:
        raise HTTPException(
            status_code=400, detail='Проект с таким именем уже существует.'
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(status_code=404, detail='Проект не найден.')
    return project


async def check_project_not_closed(project: CharityProject):
    if project.fully_invested:
        raise HTTPException(status_code=400, detail='Проект уже закрыт.')


async def check_full_amount_not_less_than_invested(
    project: CharityProject,
    new_full_amount: Optional[int],
):
    if (new_full_amount is not None and
            new_full_amount < project.invested_amount):
        raise HTTPException(
            status_code=400,
            detail='Требуемая сумма не может быть меньше уже вложенной.',
        )


async def check_project_can_be_deleted(project: CharityProject):
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=400, detail='Закрытый проект нельзя удалить!'
        )
