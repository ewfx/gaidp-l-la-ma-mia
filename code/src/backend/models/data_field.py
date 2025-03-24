from pydantic import BaseModel, Field
from typing import List, Optional
from bson import ObjectId

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

# @agastya I added this
class Rule(BaseModel):
    field: str 
    rule: str
    query: str
    page: int
# Prithvi
# class Rule(BaseModel):
#     rule: str
#     query: str

class DataField(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id")
    columnName: str
    description: str
    rules: List[Rule]

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}