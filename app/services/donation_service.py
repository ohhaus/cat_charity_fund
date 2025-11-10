from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.crud.donation import donation_crud
from app.models.donation import Donation
from app.models.user import User
from app.schemas.donation import DonationCreate
from app.services.investing import invest


class DonationService:
    """Сервис для управления пожертвованиями.

    Содержит бизнес-логику для создания пожертвований и
    автоматического распределения средств по проектам.
    """

    async def create_donation(
        self,
        donation_data: DonationCreate,
        user: User,
        session: AsyncSession,
    ) -> Donation:
        """Создает новое пожертвование и распределяет средства.

        Средства автоматически инвестируются в активные
        благотворительные проекты в порядке их создания (FIFO).

        Args:
            donation_data: Данные для создания пожертвования.
            user: Пользователь, создающий пожертвование.
            session: Асинхронная сессия базы данных.

        Returns:
            Созданное и распределенное пожертвование.
        """
        new_donation = await donation_crud.create(
            donation_data,
            session,
            extra_data={'user_id': user.id},
        )

        active_projects = await charity_project_crud.get_active_projects(
            session
        )
        updated_projects = invest(target=new_donation, sources=active_projects)

        session.add_all(updated_projects)
        await session.commit()
        await session.refresh(new_donation)

        return new_donation

    async def get_all_donations(self, session: AsyncSession) -> List[Donation]:
        """Получает все пожертвования в системе.

        Метод доступен только для суперпользователей.

        Args:
            session: Асинхронная сессия базы данных.

        Returns:
            Список всех пожертвований.
        """
        return list(await donation_crud.get_multi(session))

    async def get_user_donations(
        self, user_id: int, session: AsyncSession
    ) -> List[Donation]:
        """Получает все пожертвования конкретного пользователя.

        Args:
            user_id: ID пользователя.
            session: Асинхронная сессия базы данных.

        Returns:
            Список пожертвований пользователя.
        """
        return list(await donation_crud.get_by_user(session, user_id))


donation_service = DonationService()
