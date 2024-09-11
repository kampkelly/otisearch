from sqlalchemy.orm import relationship
from sqlalchemy import ARRAY, Column, String, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from src.database.base_class import Base


class Table(Base):
    table_name = Column(String, nullable=False)
    columns = Column(ARRAY(String), default=[])
    es_index = Column(String, nullable=True)
    database_id = Column(UUID(as_uuid=True), ForeignKey('database.id'), nullable=True)
    database = relationship("Database", back_populates="tables")
    relationships = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Table(id={self.id}, table_name={self.table_name}, columns={self.columns}, relationships={self.relationships}, es_index={self.es_index}, database_id={self.database_id})>"
