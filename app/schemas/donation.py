from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, Extra


class DonationBase(BaseModel):
    comment: Optional[str] = Field(None, min_length=1, max_length=100)
    full_amount: PositiveInt

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationUpdate(DonationCreate):
    pass


class DonationDB(DonationBase):
    id: int
    comment: Optional[str] = Field(None, min_length=1, max_length=100)
    create_date: Optional[datetime]

    class Config:
        orm_mode = True


class DonationSuperuserDB(DonationDB):
    fully_invested: bool
    close_date: Optional[datetime]
    user_id: int
    invested_amount: Optional[int]
