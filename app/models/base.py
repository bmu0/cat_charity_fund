from sqlalchemy import Boolean, Column, Integer


class CommonFields():
    full_amount = Column(Integer)
    invested_amount = Column(Integer, default=0)
    fully_invested = Column(Boolean, default=False)
