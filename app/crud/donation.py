from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    """CRUD для работы с пожертвованиями.

    Предоставляет методы для создания, получения, обновления
    и удаления пожертвований.
    """

    async def get_by_user(
        self, session: AsyncSession, user_id: int
    ) -> Sequence[Donation]:
        """Получает все пожертвования конкретного пользователя.

        Args:
            session: Асинхронная сессия базы данных.
            user_id: ID пользователя.

        Returns:
            Список пожертвований пользователя.
        """
        return await self.find_by(session, user_id=user_id)

    async def get_active_donations(
        self, session: AsyncSession
    ) -> Sequence[Donation]:
        """Получает все активные пожертвования.

        Пожертвования возвращаются отсортированными по дате
        создания.

        Args:
            session: Асинхронная сессия базы данных.

        Returns:
            Список активных пожертвований.
        """
        result = await session.execute(
            select(Donation)
            .where(Donation.fully_invested.is_(False))
            .order_by(Donation.create_date)
        )
        return result.scalars().all()


donation_crud = CRUDDonation(Donation)
