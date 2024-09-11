from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from src.database.base_class import Base


class Database(Base):
    postgres_url = Column(String, nullable=False)
    database_name = Column(String, nullable=False)
    datasync_id = Column(UUID(as_uuid=True), ForeignKey('datasync.id'), nullable=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id'), nullable=True)
    tables = relationship("Table", back_populates="database")

    def __repr__(self):
        tables_repr = f", tables=[{', '.join(repr(table) for table in self.tables)}]" if self.tables else ""
        return f"<Database(id={self.id}, postgres_url='{self.postgres_url}', database_name='{self.database_name}', datasync_id={self.datasync_id}, user_id={self.user_id}{tables_repr})>"
