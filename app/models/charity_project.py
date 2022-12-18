from sqlalchemy import Column, String, Text

from app.core.db import Base
from app.models.base import CommonFields


class CharityProject(Base, CommonFields):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
