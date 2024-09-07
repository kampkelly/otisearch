from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func

from src.database.base_class import Base


class User(Base):
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    email = Column(String, nullable=False)
    company_name = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    purpose = Column(String, nullable=True)
    cancel_reason = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
