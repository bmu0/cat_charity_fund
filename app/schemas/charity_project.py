from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: str
    full_amount: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    # close_date: Optional[datetime]

    @validator('full_amount')
    def full_amount_must_be_positive(cls, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)


# Новый класс для обновления объектов.
class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectCreate):
    id: int

    class Config:
        orm_mode = True
