from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_name_duplicate, check_project_exists
from app.core.db import get_async_session
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)


router = APIRouter()


@router.post('/', response_model=CharityProjectDB)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session)
):
    projects_list = await charity_project_crud.get_multi(session)
    return projects_list


@router.patch(
    '/{project_id}',
    response_model=CharityProjectUpdate,
    response_model_exclude_none=True,
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    project = await check_project_exists(project_id, session)

    # Добавить проверку на закрытие проекта
    # А также добавить логику финансирования проекта

    return project


@router.delete(
    '/{prject_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def delete_charity_project(
    project_id: int, session: AsyncSession = Depends(get_async_session)
):
    project = await check_project_exists(project_id, session)
    project = await charity_project_crud.remove(project, session)

    return project
