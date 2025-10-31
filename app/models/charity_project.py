from sqlalchemy import Column, String, Text

from app.models.base_investment import BaseInvestment


class CharityProject(BaseInvestment):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (
            f'{super().__repr__()}'
            f'name={self.name}, '
            f'description={self.description[:30]!r}'
        )
