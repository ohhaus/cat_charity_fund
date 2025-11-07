from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.donation import Donation
from app.schemas.donation import DonationCreate, DonationUpdate


class CRUDDonation(CRUDBase[Donation, DonationCreate, DonationUpdate]):
    async def get_by_user(
        self, session: AsyncSession, user_id: int
    ) -> Sequence[Donation]:
        user_donations = await session.execute(
            select(Donation).where(Donation.user_id == user_id)
        )
        return user_donations.scalars().all()

    async def get_active_donations(self, session: AsyncSession):
        active_donations = await session.execute(
            select(Donation)
            .where(Donation.fully_invested.is_(False))
            .order_by(Donation.create_date)
        )
        return active_donations.scalars().all()


donation_crud = CRUDDonation(Donation)
