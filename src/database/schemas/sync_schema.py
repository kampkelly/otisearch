from pydantic import BaseModel, UUID4
from typing import List, Optional


class AddDatabase(BaseModel):
    database_id: Optional[UUID4] = None
    postgres_url: str
    database_name: str
    table: str
    columns: List[str] = []
