from pydantic import BaseModel
from typing import Any, Optional

class ResponseDTO(BaseModel):
    isSuccess: bool
    data: Optional[Any] = None
    errorMessage: Optional[str] = None