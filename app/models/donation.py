from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)

from app.models.base_investment import BaseInvestment


class Donation(BaseInvestment):
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)
