from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None, min_length=1, max_length=100)
    full_amount: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    close_date: Optional[datetime]
    user_id: Optional[int]

    @validator('full_amount')
    def full_amount_must_be_positive(cls, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


class DonationCreate(DonationBase):
    pass


# Новый класс для обновления объектов.
class DonationUpdate(DonationBase):
    pass


class DonationDB(DonationCreate):
    id: int

    class Config:
        orm_mode = True
