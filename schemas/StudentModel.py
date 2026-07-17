from pydantic import BaseModel, Field, EmailStr
from schemas.ClassroomModel import ClassroomResponse

class StudentCreate(BaseModel):
    student_code: str = Field(..., min_length=3, max_length=20, description="Mã sinh viên từ 3-20 ký tự")
    full_name: str = Field(..., min_length=2, max_length=100, description="Tên sinh viên từ 2-100 ký tự")
    email: EmailStr = Field(..., description="Email bắt buộc và đúng định dạng")
    class_id: int = Field(..., ge=1, description="class_id phải lớn hơn hoặc bằng 1")

class StudentDetailResponse(BaseModel):
    id: int
    student_code: str
    full_name: str
    email: str
    classroom: ClassroomResponse

    class Config:
        from_attributes = True 