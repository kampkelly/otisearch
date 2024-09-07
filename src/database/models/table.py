from sqlalchemy import ARRAY, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

from src.database.base_class import Base


class Table(Base):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    columns = Column(ARRAY(String), default=[])
    es_index = Column(String, nullable=True)
    database_id = Column(Integer, ForeignKey('database.id'), nullable=True)
