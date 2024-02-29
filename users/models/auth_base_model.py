from sqlalchemy import Column, Integer, DateTime, func
from datetime import datetime

from core.db import Base


class AuthBaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, index=True)
    updated_at = Column(DateTime, nullable=True, default=None, onupdate=datetime.now)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
