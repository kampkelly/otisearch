from sqlalchemy import ARRAY, Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database.base_class import Base


class Table(Base):
    table_name = Column(String, nullable=False)
    columns = Column(ARRAY(String), default=[])
    es_index = Column(String, nullable=True)
    database_id = Column(UUID(as_uuid=True), ForeignKey('database.id'), nullable=True)
