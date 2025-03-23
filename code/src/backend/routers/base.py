from fastapi import APIRouter
from dto.response_dto import ResponseDTO as dto
from pydantic import BaseModel
from .file import router as file_manager_router  # Import the router from file_manager.py

class RefinementInputModel(BaseModel):
    id: int
    refinement_statement: str

router = APIRouter()

# Include routes from file_manager.py
router.include_router(file_manager_router, prefix="/file_manager", tags=["File Manager"])

@router.get("/status")
def get_status():
    return dto(isSuccess=True, data={"status": "Backend is running"})