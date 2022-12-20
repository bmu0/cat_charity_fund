from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, validator, PositiveInt


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]

    @validator('description')
    def description_cannot_be_null(cls, value):
        if not value:
            raise ValueError('Описание не может быть пустым!')
        return value

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str
    full_amount: PositiveInt


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя не может быть пустым!')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    close_date: Optional[datetime]
    invested_amount: Optional[int]
    fully_invested: Optional[bool]
    create_date: Optional[datetime]

    class Config:
        orm_mode = True
