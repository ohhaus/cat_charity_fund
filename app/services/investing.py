from typing import Sequence, TypeVar

from app.models.base_investment import BaseInvestment


InvestableType = TypeVar('InvestableType', bound=BaseInvestment)


def invest(
    target: InvestableType, sources: Sequence[InvestableType]
) -> list[InvestableType]:
    """Перераспределяет средства между источниками и целью."""
    updated = []
    for src in sources:
        if target.fully_invested:
            break

        invest_value = min(
            target.full_amount - target.invested_amount,
            src.full_amount - src.invested_amount,
        )
        if invest_value <= 0:
            continue

        target.invested_amount += invest_value
        src.invested_amount += invest_value
        src.close_investment()
        target.close_investment()
        updated.append(src)

    return updated
