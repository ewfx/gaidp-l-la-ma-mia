from pydantic import BaseModel

class RuleGetRequestModel(BaseModel):
    pdf: str
    schedule: str
    category: str
    