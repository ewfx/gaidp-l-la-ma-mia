from fastapi import APIRouter
from dto.response_dto import ResponseDTO as dto

router = APIRouter(prefix="/file")

@router.post("/")
def upload_pdf():
    return dto(isSuccess=True, data={"message": "file uploaded successfully"})

@router.get("/list")
def get_list():
    return dto(isSuccess=True, data={"message": "pdf response"})

@router.get("/schedule")
def get_schedules_by_file_id(fileId: str):
    return dto(isSuccess=True, data={"message": f"schedules for file {fileId}"})

@router.get("/section")
def get_sections_by_schedule_id(sectionId: str):
    return dto(isSuccess=True, data={"message": f"sections for schedule {sectionId}"})