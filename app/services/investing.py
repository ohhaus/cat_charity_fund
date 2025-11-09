from datetime import datetime, timezone
from typing import List, Sequence, TypeVar

from app.models.base_investment import BaseInvestment


InvestableType = TypeVar('InvestableType', bound=BaseInvestment)


def close_investment_if_fully_funded(obj: InvestableType) -> None:
    """
    Закрывает инвестицию, если она полностью профинансирована.

    Args:
        obj: Объект инвестиции (проект или пожертвование)
    """
    if obj.invested_amount >= obj.full_amount:
        obj.fully_invested = True
        obj.close_date = datetime.now(timezone.utc)


def invest(
    target: InvestableType, sources: Sequence[InvestableType]
) -> List[InvestableType]:
    """
    Перераспределяет средства между источниками и целью.

    Функция распределяет средства из активных источников
    (пожертвований или проектов) в целевой объект до его
    полного финансирования. Обработка происходит в порядке
    поступления источников (FIFO).

    Args:
        target: Целевой объект (проект или пожертвование)
        sources: Последовательность источников средств

    Returns:
        List[InvestableType]: Список обновленных источников

    Example:
        >>> project = CharityProject(full_amount=1000)
        >>> donations = get_active_donations()
        >>> updated = invest(target=project, sources=donations)
    """
    updated_sources = []

    for source in sources:
        if target.fully_invested:
            break

        available_from_target = target.full_amount - target.invested_amount
        available_from_source = source.full_amount - source.invested_amount
        investment_amount = min(available_from_target, available_from_source)

        if investment_amount <= 0:
            continue

        target.invested_amount += investment_amount
        source.invested_amount += investment_amount

        close_investment_if_fully_funded(source)
        close_investment_if_fully_funded(target)

        updated_sources.append(source)

    return updated_sources
