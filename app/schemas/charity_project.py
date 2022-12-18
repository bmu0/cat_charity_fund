from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: str
    full_amount: int
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]
    # close_date: Optional[datetime]

    class Congig:
        extra = Extra.forbid


class CharityProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: int
    # invested_amount: int

    @validator('description')
    def description_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Имя переговорки не может быть пустым!')
        return value

    @validator('full_amount')
    def full_amount_must_be_positive(cls, value):
        if int(value) < 1:
            raise ValueError('full_amount < 0')
        return value


# Новый класс для обновления объектов.
class CharityProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[int]

    @validator('description')
    def description_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Описание не может быть пустым!')
        return value

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectDB(CharityProjectBase):
    id: int
    close_date: Optional[datetime]

    class Config:
        orm_mode = True
