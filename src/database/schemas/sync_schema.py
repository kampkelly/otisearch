from pydantic import BaseModel, UUID4, field_validator, ValidationError
from typing import List, Optional, Dict, Any, Union


class Relationship(BaseModel):
    name: str
    foreign_key: str
    type: str
    columns: List[str]

    def __getitem__(self, item):
        return getattr(self, item)

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def to_dict(self):
        return self.model_dump()

    class Config:
        orm_mode = True


class AddDatabase(BaseModel):
    database_id: Optional[UUID4] = None
    postgres_url: str
    database_name: str
    table: str
    columns: List[str] = []
    relationships: List[Relationship]

    @field_validator('relationships')
    @classmethod
    def validate_relationships(cls, value: List[Union[Dict[str, Any], Relationship]]) -> List[Relationship]:
        validated_relationships = []
        for item in value:
            # TODO: check each item value
            if isinstance(item, Relationship):
                validated_relationships.append(item)
            elif isinstance(item, dict):
                try:
                    relationship = Relationship(**item)
                    validated_relationships.append(relationship)
                except ValidationError as e:
                    raise ValueError(f"Invalid relationship: {e}")
            else:
                raise ValueError(f"Invalid relationship type: {type(item)}. Expected dict or Relationship.")
        return validated_relationships

    model_config = {
        'arbitrary_types_allowed': True
    }


class TriggerSync(BaseModel):
    datasync_id: str
