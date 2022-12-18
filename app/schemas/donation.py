from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None, min_length=1, max_length=100)
    full_amount: Optional[int]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    user_id: Optional[int]


class DonationCreate(DonationBase):
    comment: Optional[str]
    full_amount: int

    @validator('full_amount')
    def full_amount_must_be_positive(cls, value):
        if not value or int(value) < 1:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


# Новый класс для обновления объектов.
class DonationUpdate(DonationCreate):
    pass


class DonationDB(BaseModel):
    id: int
    comment: Optional[str] = Field(None, min_length=1, max_length=100)
    full_amount: Optional[int]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationSuperuserDB(BaseModel):
    id: int
    comment: Optional[str]
    create_date: datetime
    full_amount: int
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    user_id: Optional[int]
    invested_amount: int

    class Config:
        orm_mode = True
