from sqlalchemy import Column, Integer, Text, String, Boolean, DateTime, JSON
from sqlalchemy.sql import func

from src.database.base_class import Base


class Setting(Base):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    email = Column(String, nullable=False)
    secret_key = Column(String, nullable=False)
    db_user = Column(String, nullable=True)
    db_name = Column(String, nullable=True)
    db_password = Column(String, nullable=True)
    db_host = Column(String, nullable=True)
    db_port = Column(Integer, nullable=True)
    db_table = Column(String, nullable=True)
    db_schema = Column(JSON, nullable=True)
    es_index = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
