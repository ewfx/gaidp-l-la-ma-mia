from fastapi import APIRouter
from dto.response_dto import ResponseDTO as dto

router = APIRouter(prefix="/file")

@router.post("/")
def uploadPdf():
    return dto(isSuccess=True, data={"message": "file uploaded successfully"})

@router.get("/list")
def GetList():
    return dto(isSuccess=True, data={"message": "pdf response"})

@router.get("/schedule")
def getSchedulesByFile(fileId: str):
    return dto(isSuccess=True, data={"message": f"schedules for file {fileId}"})

@router.get("/section")
def getSectionsBySchedule(sectionId: str):
    return dto(isSuccess=True, data={"message": "sections for schedule {sectionId}"})