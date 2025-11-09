from datetime import datetime, timezone

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Integer

from app.core.db import Base


class BaseInvestment(Base):
    """
    Базовая абстрактная модель для инвестиций.

    Предоставляет общие поля для моделей, связанных с
    инвестициями и распределением средств (проекты и
    пожертвования).

    Attributes:
        full_amount: Полная требуемая/внесенная сумма
        invested_amount: Уже инвестированная/распределенная сумма
        fully_invested: Флаг полного инвестирования
        create_date: Дата и время создания записи
        close_date: Дата и время закрытия

    Constraints:
        - full_amount должна быть больше 0
        - invested_amount в диапазоне от 0 до full_amount
    """

    __abstract__ = True

    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
    create_date = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    close_date = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        CheckConstraint('full_amount > 0', name='check_full_amount_positive'),
        CheckConstraint(
            '0 <= invested_amount <= full_amount',
            name='check_invested_amount_range',
        ),
    )

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта."""
        return (
            f'{type(self).__name__} '
            f'full_amount={self.full_amount}, '
            f'invested_amount={self.invested_amount}, '
            f'fully_invested={self.fully_invested}, '
            f'create_date={self.create_date}, '
            f'close_date={self.close_date}'
        )
