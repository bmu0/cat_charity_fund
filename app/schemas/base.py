from typing import Optional
from datetime import datetime

from pydantic import BaseModel, validator


class CommonFieldsModel(BaseModel):
    full_amount: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    @validator('full_amount')
    def full_amount_is_positive(cls, value):
        if value <= 0:
            raise ValueError('Пожертвование должно быть больше 0')
        return value