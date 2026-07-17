from pydantic import BaseModel, Field, EmailStr
from typing import Any, List, Optional

class ClassroomResponse(BaseModel):
    id: int
    class_code: str
    class_name: str

    class Config:
        from_attributes = True


class ApiResponse(BaseModel):
    statusCode: int
    message: str
    data: Optional[Any] = None
    error: Optional[str] = None
    path: str 