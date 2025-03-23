from pydantic import BaseModel

class RuleInputModel(BaseModel):
    id: int
    rule: str