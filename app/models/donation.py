from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base_investment import BaseInvestment


class Donation(BaseInvestment):
    """
    Модель пожертвования пользователя.

    Представляет пожертвование, сделанное пользователем для
    благотворительных проектов. Наследуется от BaseInvestment.

    Attributes:
        user_id: ID пользователя (внешний ключ)
        comment: Необязательный комментарий к пожертвованию
        full_amount: Сумма пожертвования (из BaseInvestment)
        invested_amount: Распределенная сумма (из BaseInvestment)
        fully_invested: Флаг полного распределения
        create_date: Дата создания (из BaseInvestment)
        close_date: Дата полного распределения (из BaseInvestment)
    """

    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    comment = Column(Text, nullable=True)
