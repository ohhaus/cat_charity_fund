from http import HTTPStatus
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
    """
    Проверяет уникальность имени проекта.

    Выбрасывает исключение, если проект с таким именем уже
    существует (исключая случай обновления существующего
    проекта).

    Args:
        name: Имя проекта для проверки
        session: Асинхронная сессия базы данных
        current_project_id: ID текущего проекта (при обновлении)

    Raises:
        HTTPException: Если проект с таким именем уже существует
    """
    existing_project = await charity_project_crud.get_by_name(name, session)
    if existing_project and existing_project.id != current_project_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует.',
        )


async def check_project_exists(
    project_id: int,
    session: AsyncSession,
) -> CharityProject:
    """
    Проверяет существование проекта по его ID.

    Args:
        project_id: ID проекта для проверки
        session: Асинхронная сессия базы данных

    Returns:
        CharityProject: Найденный проект

    Raises:
        HTTPException: Если проект не найден
    """
    project = await charity_project_crud.get(project_id, session)
    if not project:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден.',
        )
    return project


async def check_project_not_closed(project: CharityProject) -> None:
    """
    Проверяет, что проект не закрыт.

    Args:
        project: Проект для проверки

    Raises:
        HTTPException: Если проект уже закрыт
    """
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект уже закрыт.',
        )


async def check_full_amount_not_less_than_invested(
    project: CharityProject,
    new_full_amount: Optional[int],
) -> None:
    """
    Проверяет, что новая сумма не меньше уже вложенной.

    Args:
        project: Проект для проверки
        new_full_amount: Новая требуемая сумма (может быть None)

    Raises:
        HTTPException: Если новая сумма меньше уже вложенной
    """
    if (
        new_full_amount is not None
        and new_full_amount < project.invested_amount
    ):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Требуемая сумма не может быть меньше уже вложенной.',
        )


async def check_project_can_be_deleted(project: CharityProject) -> None:
    """
    Проверяет возможность удаления проекта.

    Проект нельзя удалить, если:
    - В него уже были внесены средства (invested_amount > 0)
    - Проект закрыт (fully_invested = True)

    Args:
        project: Проект для проверки

    Raises:
        HTTPException: Если проект нельзя удалить
    """
    if project.invested_amount > 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    if project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя удалить!',
        )
