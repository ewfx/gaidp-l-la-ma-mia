from fastapi import APIRouter
from dto.response_dto import ResponseDTO as dto
from pydantic import BaseModel
from .file import router as file_router 
from .rule import router as rule_router  

class RefinementInputModel(BaseModel):
    id: int
    refinement_statement: str

router = APIRouter()

# Include routes from file_manager.py
router.include_router(file_router, tags=["File Router"])
router.include_router(rule_router, tags=["Rule Router"])

@router.get("/health")
def get_status():
    return dto(isSuccess=True, data={"status": "up"})