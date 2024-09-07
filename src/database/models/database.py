from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from src.database.base_class import Base


class Database(Base):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    postgres_url = Column(String, nullable=False)
    name = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('datasync.id'), nullable=True)
