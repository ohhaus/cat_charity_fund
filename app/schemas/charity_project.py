from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CharityProjectBase(BaseModel):
    name: str | None = Field(None, max_length=100)
    description: str | None = Field(None)
    full_amount: int | None = Field(None, gt=0)

    model_config = ConfigDict(extra='forbid')


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., max_length=100)
    description: str = Field(...)
    full_amount: int = Field(..., gt=0)


class CharityProjectUpdate(CharityProjectBase):
    @field_validator('full_amount')
    def validate_positive(cls, value):
        if value is not None and value <= 0:
            raise ValueError('full_amount должно быть больше 0')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int = Field(0, ge=0)
    fully_invested: bool = False
    created_date: datetime
    closed_at: datetime | None = None
    name: str
    description: str
    full_amount: int

    model_config = ConfigDict(from_attributes=True)
