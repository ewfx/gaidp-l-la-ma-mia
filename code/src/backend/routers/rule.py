import os
import re
from fastapi import APIRouter, HTTPException
from dto.response_dto import ResponseDTO as dto
from models.rule_get_request_model import RuleGetRequestModel
from models.rule_input_model import RuleInputModel
from pymongo import MongoClient
from services.base_mongo_service import BaseMongoService
from dotenv import load_dotenv

router = APIRouter(prefix="/file")

# Initialize MongoDB client
load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)

router = APIRouter(prefix="/rule")
# http://127.0.0.1:8000/rule?pdf=PDFName&schedule=ScheduleA&category=USAutoLoan
@router.get("")
def get_rules(pdfName: str = None, schedule: str = None, category: str = None):
    try:
        if not pdfName or not schedule or not category:
            raise HTTPException(status_code=400, detail="Missing required parameters: pdfName, schedule, category")
        
        # Remove the .pdf extension from pdfName
        sanitized_pdf_name = re.sub(r'\.pdf$', '', pdfName, flags=re.IGNORECASE)

        # Generate the sanitized collection name for rules
        rules_collection_name = f"{sanitized_pdf_name}_{schedule}_{category}"
        rules_collection_name = re.sub(r'[^a-zA-Z0-9_]', '', rules_collection_name)  # Keep only alphanumeric characters and underscores
        rules_service = BaseMongoService(mongo_client, rules_collection_name)

        # Fetch all rules from the rules collection
        rules = rules_service.get_all()
        return dto(isSuccess=True, data=rules)
    except Exception as e:
        return dto(isSuccess=False, errorMessage=str(e))

@router.post("")
def create_or_update_rule(rule: RuleInputModel):    
    return dto(isSuccess=True, data={"message": "Rule created successfully", "rule": "temp"})


# @agastya just started working on this, see if better way
# @router.post("/add_rule")
# def add_rule(rule: RuleInputModel):
#     try:
        