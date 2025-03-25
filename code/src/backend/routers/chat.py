import os
from fastapi import APIRouter
from dto.response_dto import ResponseDTO as dto
from dto.message_dto import MessageDTO
from pymongo import MongoClient
from services.base_mongo_service import BaseMongoService
from dotenv import load_dotenv
from services.LLM.chat_services import update_rules
import re

router = APIRouter(prefix="/chat")

load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
print("MongoDB connected")
#http://127.0.0.1:8000/chat/
@router.post("/")
def chat_service(message: str = None, pdfName: str = None, schedule: str = None, category: str = None):
    print("Message received: ", message)
    updated_rule = update_rules(message, pdfName, schedule, category)
    return dto(isSuccess=True, data=updated_rule)

@router.post("/update")
def update_rule_in_db(updated_rule: dict, pdfName: str = None, schedule: str = None, category: str = None):
    """
    Endpoint to update the rule in the database.

    Args:
        updated_rule (dict): The updated rule to be saved.
        pdfName (str): The name of the PDF.
        schedule (str): The schedule name.
        category (str): The category name.

    Returns:
        dict: Success or failure response.
    """
    try:
        print("Updated rule received: ", updated_rule)

        # Remove the .pdf extension from pdfName
        sanitized_pdf_name = re.sub(r'\.pdf$', '', pdfName, flags=re.IGNORECASE)

        # Generate the sanitized collection name
        collection_name = f"{sanitized_pdf_name}_{schedule}_{category}"
        collection_name = re.sub(r'[^a-zA-Z0-9_]', '', collection_name)  # Keep only alphanumeric characters and underscores

        # Initialize MongoDB service
        mongo_service = BaseMongoService(mongo_client, collection_name)

        # Remove the `_id` field from the updated rule to avoid errors
        if "_id" in updated_rule['updated_rule']:
            updated_rule['updated_rule'].pop("_id")

        # Convert the `query` field to a string
        if "query" in updated_rule['updated_rule']:
            updated_rule['updated_rule']["query"] = str(updated_rule['updated_rule']["query"])

        # Update the rule in the database
        result = mongo_service.collection.update_one(
            {"fieldName": updated_rule['updated_rule']["fieldName"]},  # Match the rule by fieldName
            {"$set": updated_rule['updated_rule']},  # Update the rule
            upsert=True  # Insert if it doesn't exist
        )

        if result.modified_count > 0 or result.upserted_id:
            return dto(isSuccess=True, data="Rule updated successfully.")
        else:
            return dto(isSuccess=False, data="No changes were made.")
    except Exception as e:
        return dto(isSuccess=False, data=f"Failed to update rule: {str(e)}")