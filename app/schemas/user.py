from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, EmailStr


class UserRead(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    is_superuser: bool
    is_verified: bool

    class Config:
        orm_mode = True


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    email: Optional[EmailStr] = None
