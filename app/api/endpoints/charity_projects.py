from datetime import datetime, timezone
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
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.charity_project import (
    CharityProjectCreate,
    CharityProjectDB,
    CharityProjectUpdate,
)
from app.services.investing import invest


router = APIRouter()


@router.post('/', response_model=CharityProjectDB)
async def create_charity_project(
    project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(
        project, session, extra_data=None
    )

    session.add_all(
        invest(
            target=new_project,
            sources=await donation_crud.get_active_donations(session),
        )
    )
    await session.commit()
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_projects(
    session: AsyncSession = Depends(get_async_session),
):
    projects_list = await charity_project_crud.get_multi(session)
    return projects_list


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def update_charity_project(
    project_id: int,
    project_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
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

    updated_project = await charity_project_crud.update(
        project,
        project_in,
        session,
    )

    if updated_project.invested_amount == updated_project.full_amount:
        updated_project.fully_invested = True
        updated_project.close_date = datetime.now(timezone.utc)

    session.add_all(
        invest(
            target=updated_project,
            sources=await donation_crud.get_active_donations(session),
        )
    )

    await session.commit()
    await session.refresh(updated_project)

    return updated_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
)
async def delete_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    project = await check_project_exists(project_id, session)
    await check_project_can_be_deleted(project)
    project = await charity_project_crud.remove(project, session)

    return project
