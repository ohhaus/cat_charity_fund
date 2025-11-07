from datetime import datetime

from pydantic import BaseModel, Field, field_validator


class CharityProjectBase(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None)
    full_amount: int | None = Field(None, gt=0)

    class Config:
        extra = 'forbid'


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100, min_length=1)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    @field_validator('name', 'description')
    def validate_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Поле не может быть пустым')
        return value


class CharityProjectUpdate(CharityProjectBase):
    @field_validator('name', 'description')
    def validate_not_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError('Поле не может быть пустым')
        return value

    @field_validator('full_amount')
    def validate_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError('full_amount должно быть больше 0')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = False
    create_date: datetime
    close_date: datetime | None = None
    name: str
    description: str
    full_amount: int

    class Config:
        from_attributes = True
