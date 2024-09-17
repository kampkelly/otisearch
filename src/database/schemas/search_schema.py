from pydantic import BaseModel, UUID4, field_validator, ValidationError
from typing import List, Optional, Dict, Any, Union


class SemanticSearch(BaseModel):
    query: str
    datasync_id: str
