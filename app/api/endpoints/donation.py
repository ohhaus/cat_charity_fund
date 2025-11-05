from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB
from app.services.investing import invest


router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True,
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation_in, session, extra_data={'user_id': user.id}
    )

    active_projects = await charity_project_crud.get_active_projects(session)
    invest(target=new_donation, sources=active_projects)

    await session.commit()
    await session.refresh(new_donation)

    return new_donation


@router.get(
    '/',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    user=Depends(current_superuser),
):
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def get_my_donations(
    user=Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    return await donation_crud.get_by_user(session, user.id)
