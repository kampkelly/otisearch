from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func

from src.database.base_class import Base


class DataSync(Base):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)
    is_active = Column(Boolean, default=True)
