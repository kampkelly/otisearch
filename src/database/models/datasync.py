from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from src.database.base_class import Base


class DataSync(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    is_active = Column(Boolean, default=True)
