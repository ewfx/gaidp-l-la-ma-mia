import os
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
print("MongoDB connected")

router = APIRouter(prefix="/rule")

@router.get("")
def get_rules(pdf: str, schedule: str, category: str):
    try:
        # Convert query parameters into a RuleGetRequestModel object
        request = RuleGetRequestModel(pdf=pdf, schedule=schedule, category=category)
        
        # Create a service for the "data_field" collection in the "my_database" database
        print(f"collection: {request.pdf}_{request.schedule}_{request.category}")
        data_field_service = BaseMongoService(mongo_client, f"{request.pdf}_{request.schedule}_{request.category}")
        
        # Retrieve all documents in the collection with specific fields
        documents = data_field_service.get_all(
            fields={"_id": 1, "columnName": 1, "description": 1, "rules": 1}
        )
        return dto(isSuccess=True, data=documents)
    except Exception as e:
        return dto(isSuccess=False, errorMessage=str(e))

@router.post("")
def create_or_update_rule(rule: RuleInputModel):    
    return dto(isSuccess=True, data={"message": "Rule created successfully", "rule": "temp"})


# @agastya just started working on this, see if better way
# @router.post("/add_rule")
# def add_rule(rule: RuleInputModel):
#     try:
        