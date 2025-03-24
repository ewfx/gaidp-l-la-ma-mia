from fastapi import APIRouter
from dto.response_dto import ResponseDTO as dto
from pydantic import BaseModel
from .file import router as file_router 
from .rule import router as rule_router  
from .chat import router as chat_router
from .anomaly import router as anomaly_router

class RefinementInputModel(BaseModel):
    id: int
    refinement_statement: str

router = APIRouter()

# Include routes from file_manager.py
router.include_router(file_router, tags=["File Router"])
router.include_router(rule_router, tags=["Rule Router"])
router.include_router(chat_router, tags=["Chat Router"])
router.include_router(anomaly_router, tags=["Anomaly Detection"])

@router.get("/health")
def get_status():
    return dto(isSuccess=True, data={"status": "up"})