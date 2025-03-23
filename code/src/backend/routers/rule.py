from fastapi import APIRouter, HTTPException
from dto.response_dto import ResponseDTO as dto
from models.rule_input_model import RuleInputModel  # Import the model

router = APIRouter(prefix="/rule")

# Mock database for demonstration
mock_rules_db = [
    {"id": 1, "rule": "Rule 1 description"},
    {"id": 2, "rule": "Rule 2 description"},
]

@router.get("")
def get_rules():
    return dto(isSuccess=True, data=mock_rules_db)

@router.post("/rule")
def create_or_update_rule(rule: RuleInputModel):
    for existing_rule in mock_rules_db:
        if existing_rule["id"] == rule.id:
            existing_rule["rule"] = rule.rule
            return dto(isSuccess=True, data={"message": "Rule updated successfully", "rule": existing_rule})
    
    new_rule = {"id": rule.id, "rule": rule.rule}
    mock_rules_db.append(new_rule)
    return dto(isSuccess=True, data={"message": "Rule created successfully", "rule": new_rule})