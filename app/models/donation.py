from datetime import UTC, datetime, timezone

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Text,
)

from app.models.base_investment import BaseInvestment


class Donation(BaseInvestment):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text, nullable=True)
