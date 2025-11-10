from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_full_amount_not_less_than_invested,
    check_name_duplicate,
    check_project_can_be_deleted,
    check_project_exists,
    check_project_not_closed,
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.models import User
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.charity_project_service import charity_project_service


router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    summary='Создать благотворительный проект',
)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    """Создает новый благотворительный проект.

    Доступно только суперпользователям.
    """
    await check_name_duplicate(project.name, session)
    return await charity_project_service.create_project(project, session)


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
    summary='Получить список всех проектов',
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех благотворительных проектов.

    Доступно всем пользователям, включая анонимных.
    """
    return await charity_project_service.get_all_projects(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Обновить благотворительный проект',
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    """Обновляет существующий благотворительный проект.

    Доступно только суперпользователям.
    Нельзя обновлять закрытые проекты.
    """
    project = await check_project_exists(project_id, session)
    await check_project_not_closed(project)

    if project_in.name:
        await check_name_duplicate(
            project_in.name,
            session,
            project_id,
        )
    await check_full_amount_not_less_than_invested(
        project,
        project_in.full_amount,
    )

    return await charity_project_service.update_project(
        project, project_in, session
    )


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    summary='Удалить благотворительный проект',
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    """Удаляет благотворительный проект.

    Доступно только суперпользователям.
    Нельзя удалять проекты, в которые внесены средства.
    """
    project = await check_project_exists(project_id, session)
    await check_project_can_be_deleted(project)
    return await charity_project_service.delete_project(project, session)
