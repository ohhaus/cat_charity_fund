from sqlalchemy import Column, String, Text

from app.models.base_investment import BaseInvestment


class CharityProject(BaseInvestment):
    """
    Модель благотворительного проекта.

    Представляет благотворительный проект, для которого
    собираются пожертвования. Наследуется от BaseInvestment.

    Attributes:
        name: Уникальное название проекта (макс 100 символов)
        description: Подробное описание проекта и его целей
        full_amount: Требуемая сумма (из BaseInvestment)
        invested_amount: Уже собранная сумма (из BaseInvestment)
        fully_invested: Флаг полного финансирования
        create_date: Дата создания проекта (из BaseInvestment)
        close_date: Дата закрытия проекта (из BaseInvestment)
    """

    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self) -> str:
        """Возвращает строковое представление объекта."""
        return (
            f'{super().__repr__()}'
            f'name={self.name}, '
            f'description={self.description[:30]!r}'
        )
