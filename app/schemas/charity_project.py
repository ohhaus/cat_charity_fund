from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = Field(None)
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        extra = 'forbid'


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100, min_length=1)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    @validator('name', 'description')
    def validate_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Поле не может быть пустым')
        return value


class CharityProjectUpdate(CharityProjectBase):
    @validator('name', 'description')
    def validate_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Поле не может быть пустым')
        return value

    @validator('full_amount')
    def validate_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError('full_amount должно быть больше 0')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = False
    create_date: datetime
    close_date: Optional[datetime] = None
    name: str
    description: str
    full_amount: int

    class Config:
        orm_mode = True
