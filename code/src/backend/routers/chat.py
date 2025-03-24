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