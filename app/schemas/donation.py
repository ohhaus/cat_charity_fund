from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None, description='Комментарий')
    full_amount: Optional[int] = Field(
        None, gt=0, description='Полная сумма пожертвования'
    )

    class Config:
        extra = 'forbid'


class DonationCreate(DonationBase):
    full_amount: int = Field(
        ..., gt=0, description='Обязательная сумма пожертвования'
    )


class DonationUpdate(DonationBase):
    @validator('full_amount')
    def validate_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError('full_amount должно быть больше 0')
        return value


class DonationUserDB(DonationBase):
    id: int
    create_date: datetime
    full_amount: int

    class Config:
        orm_mode = True


class DonationDB(DonationBase):
    id: int
    user_id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None
    full_amount: int

    class Config:
        orm_mode = True
