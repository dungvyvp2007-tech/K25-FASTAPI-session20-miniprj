from fastapi import FastAPI, Depends, status, Request
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database.data import Base, engine, get_db

import models
from schemas.ClassroomModel import ApiResponse
from schemas.StudentModel import StudentCreate, StudentDetailResponse
from service.StudentService import StudentService

Base.metadata.create_all(bind=engine)

app = FastAPI(title="API Quản Lý Sinh Viên")

@app.get("/students", response_model=ApiResponse, status_code=status.HTTP_200_OK)
def get_students(request: Request, db: Session = Depends(get_db)):
    student_service = StudentService(db)
    students = student_service.get_all_students()
    student_data = [StudentDetailResponse.model_validate(s) for s in students]
    
    return {
        "statusCode": 200,
        "message": "Lấy danh sách sinh viên thành công!",
        "data": student_data,
        "error": None,
        "path": request.url.path
    }

@app.post("/students", response_model=ApiResponse, status_code=status.HTTP_201_CREATED)
def create_student(request: Request, student_in: StudentCreate, db: Session = Depends(get_db)):
    student_service = StudentService(db)

    if not student_service.check_class_exists(student_in.class_id):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={
                "statusCode": 404,
                "message": "Không tìm thấy lớp học!",
                "data": None,
                "error": "ERR-CLASS-01",
                "path": request.url.path
            }
        )

    if student_service.check_student_code_exists(student_in.student_code):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={
                "statusCode": 400,
                "message": "Mã sinh viên đã tồn tại!",
                "data": None,
                "error": "ERR-STUDENT-01",
                "path": request.url.path
            }
        )

    new_student = student_service.create_student(student_in)
    student_detail = StudentDetailResponse.model_validate(new_student)

    return {
        "statusCode": 201,
        "message": "Thêm mới sinh viên thành công!",
        "data": student_detail,
        "error": None,
        "path": request.url.path
    } 