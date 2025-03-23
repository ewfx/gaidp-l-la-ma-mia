from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello from FastAPI backend!"}

@router.get("/status")
def get_status():
    return {"status": "Backend is running"}