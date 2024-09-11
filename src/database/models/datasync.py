from sqlalchemy import Column, Boolean, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from src.database.base_class import Base


class DataSync(Base):
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    is_active = Column(Boolean, default=True)
    schema = Column(JSON, nullable=True)
