from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database.base_class import Base


class Database(Base):
    postgres_url = Column(String, nullable=False)
    database_name = Column(String, nullable=False)
    datasync_id = Column(UUID(as_uuid=True), ForeignKey('datasync.id'), nullable=True)
