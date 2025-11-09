from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models.user import User
from app.schemas.donation import DonationCreate, DonationDB, DonationUserDB
from app.services.donation_service import donation_service


router = APIRouter()


@router.post(
    '/',
    response_model=DonationUserDB,
    response_model_exclude_none=True,
    summary='Сделать пожертвование',
)
async def create_donation(
    donation_in: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    """
    Создает новое пожертвование от текущего пользователя.

    Средства автоматически распределяются по активным
    благотворительным проектам.
    """
    return await donation_service.create_donation(donation_in, user, session)


@router.get(
    '/',
    response_model=List[DonationDB],
    response_model_exclude_none=True,
    summary='Получить список всех пожертвований',
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    """
    Возвращает список всех пожертвований в системе.

    Доступно только суперпользователям.
    """
    return await donation_service.get_all_donations(session)


@router.get(
    '/my',
    response_model=List[DonationUserDB],
    response_model_exclude_none=True,
    summary='Получить список моих пожертвований',
)
async def get_my_donations(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список пожертвований текущего пользователя."""
    return await donation_service.get_user_donations(user.id, session)
