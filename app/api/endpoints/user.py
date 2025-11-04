from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import (
    auth_backend,
    current_superuser,
    current_user,
    fastapi_users,
)
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, UserUpdate


router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix='/auth/jwt',
    tags=['auth'],
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix='/auth',
    tags=['auth'],
)


@router.patch(
    '/me',
    response_model=UserUpdate,
)
async def patch_current_user(
    update_data: UserUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
):
    if update_data.email is not None:
        user.email = update_data.email

    session.add(user)

    await session.commit()
    await session.refresh(user)
    return user


@router.get(
    '/me',
    response_model=UserRead,
)
async def get_current_user(user: User = Depends(current_user)):
    return user


@router.get('/{user_id}', response_model=UserRead)
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=404, detail='Пользователь не найден'
        ) from None
    db_user = await session.get(User, user_id_int)
    if not db_user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    return db_user


@router.patch('/{user_id}', response_model=UserUpdate)
async def patch_user(
    user_id: str,
    update_data: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
):
    try:
        int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=404, detail='Пользователь не найден'
        ) from None
    db_user = await session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail='Пользователь не найден')
    if update_data.email is not None:
        db_user.email = update_data.email

    if update_data.is_active is not None:
        db_user.is_active = update_data.is_active

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user
