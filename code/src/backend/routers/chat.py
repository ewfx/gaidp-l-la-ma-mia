import os
from fastapi import APIRouter
from dto.response_dto import ResponseDTO as dto
from dto.message_dto import MessageDTO
from pymongo import MongoClient
from services.base_mongo_service import BaseMongoService
from dotenv import load_dotenv
from services.LLM.chat_services import update_rules

router = APIRouter(prefix="/chat")

load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
print("MongoDB connected")
#http://127.0.0.1:8000/chat/
@router.post("/")
def chat_service(request: MessageDTO):
    message = request.message
    print("Message received: ", message)
    updated_rule = update_rules(message)
    return dto(isSuccess=True, data=updated_rule)

@router.post("/update")
def update_rule_in_db(updated_rule: dict):
    """
    Endpoint to update the rule in the database.

    Args:
        updated_rule (dict): The updated rule to be saved.

    Returns:
        dict: Success or failure response.
    """
    try:
        # Logic to update the rule in the database
        # For example, using MongoDB: TODO
        # db = mongo_client["your_database_name"]
        # collection = db["your_collection_name"]
        # result = collection.update_one(
        #     {"constraint": updated_rule["constraint"]},  # Match the rule
        #     {"$set": updated_rule},  # Update the rule
        #     upsert=True,  # Insert if it doesn't exist
        # )
        # if result.modified_count > 0 or result.upserted_id:
        #     return dto(isSuccess=True, data="Rule updated successfully.")
        # else:
        #     return dto(isSuccess=False, data="No changes were made.")
        return dto(isSuccess=True, data="Rule updated successfully.")
    except Exception as e:
        return dto(isSuccess=False, data=f"Failed to update rule: {str(e)}")