import os
from fastapi import APIRouter
from dto.response_dto import ResponseDTO as dto
from pymongo import MongoClient
from services.base_mongo_service import BaseMongoService
from dotenv import load_dotenv

router = APIRouter(prefix="/file")

# Initialize MongoDB client
load_dotenv()
MONGO_URI = os.environ.get("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
print("MongoDB connected")

@router.post("/")
def upload_pdf():
    return dto(isSuccess=True, data={"message": "file uploaded successfully"})

@router.get("/list")
def get_list():
    try:            
        # Create a service for the "data_field" collection in the "my_database" database
        data_field_service = BaseMongoService(mongo_client, "PDF_Index")
        # Retrieve all documents in the collection
        documents = data_field_service.get_all()
        return dto(isSuccess=True, data=documents)
    except Exception as e:
        return dto(isSuccess=False, errorMessage=str(e))

@router.get("/schedule")
def get_schedules_by_file_id(fileId: str):
    return dto(isSuccess=True, data={"message": f"schedules for file {fileId}"})

@router.get("/section")
def get_sections_by_schedule_id(sectionId: str):
    return dto(isSuccess=True, data={"message": f"sections for schedule {sectionId}"})