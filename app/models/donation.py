from sqlalchemy import Column, ForeignKey, Integer, Text

from app.models.base import CommonFields
from app.core.db import Base


class Donation(Base, CommonFields):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)
