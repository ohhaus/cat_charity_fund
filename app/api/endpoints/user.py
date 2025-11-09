from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate


router = APIRouter()


@router.patch(
    '/me',
    response_model=UserUpdate,
    summary='Обновить данные текущего пользователя',
)
async def patch_current_user(
    update_data: UserUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session),
) -> User:
    """
    Обновляет данные текущего авторизованного пользователя.

    Args:
        update_data: Данные для обновления
        user: Текущий авторизованный пользователь
        session: Асинхронная сессия базы данных

    Returns:
        User: Обновленные данные пользователя
    """
    if update_data.email is not None:
        user.email = update_data.email

    session.add(user)
    await session.commit()
    await session.refresh(user)

    return user


@router.get(
    '/me',
    response_model=UserRead,
    summary='Получить данные текущего пользователя',
)
async def get_current_user(user: User = Depends(current_user)) -> User:
    """
    Возвращает данные текущего авторизованного пользователя.

    Args:
        user: Текущий авторизованный пользователь

    Returns:
        User: Данные текущего пользователя
    """
    return user


@router.get(
    '/{user_id}',
    response_model=UserRead,
    summary='Получить данные пользователя по ID',
)
async def get_user(
    user_id: str,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
) -> User:
    """
    Возвращает данные пользователя по его ID.

    Доступно только суперпользователям.

    Args:
        user_id: ID пользователя
        session: Асинхронная сессия базы данных
        user: Текущий суперпользователь

    Returns:
        User: Данные запрошенного пользователя

    Raises:
        HTTPException: Если пользователь не найден или ID
                       невалидный
    """
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пользователь не найден',
        ) from None

    db_user = await session.get(User, user_id_int)
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пользователь не найден',
        )

    return db_user


@router.patch(
    '/{user_id}',
    response_model=UserUpdate,
    summary='Обновить данные пользователя по ID',
)
async def patch_user(
    user_id: str,
    update_data: UserUpdate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_superuser),
) -> User:
    """
    Обновляет данные пользователя по его ID.

    Доступно только суперпользователям.

    Args:
        user_id: ID пользователя
        update_data: Данные для обновления
        session: Асинхронная сессия базы данных
        user: Текущий суперпользователь

    Returns:
        User: Обновленные данные пользователя

    Raises:
        HTTPException: Если пользователь не найден или ID
                       невалидный
    """
    try:
        user_id_int = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пользователь не найден',
        ) from None

    db_user = await session.get(User, user_id_int)
    if not db_user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Пользователь не найден',
        )

    if update_data.email is not None:
        db_user.email = update_data.email

    if update_data.is_active is not None:
        db_user.is_active = update_data.is_active

    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)

    return db_user
