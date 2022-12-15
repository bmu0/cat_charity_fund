from sqlalchemy import Column, String, Text

from app.models.base import CommonFields
from app.core.db import Base


class CharityProject(Base, CommonFields):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
