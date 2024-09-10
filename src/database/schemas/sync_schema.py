from pydantic import BaseModel
from typing import List


class AddDatabase(BaseModel):
    database_id: str = None
    postgres_url: str
    name: str
    tables: List[str] = []
