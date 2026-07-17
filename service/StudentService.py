from sqlalchemy.orm import Session, joinedload
import models
import schemas

class StudentService:
    def __init__(self, db: Session):
        self.db = db

    def get_all_students(self):
        return self.db.query(models.Student).options(joinedload(models.Student.classroom)).all()

    def check_class_exists(self, class_id: int):
        classroom = self.db.query(models.Classroom).filter(models.Classroom.id == class_id).first()
        return classroom is not None

    def check_student_code_exists(self, student_code: str):
        student = self.db.query(models.Student).filter(models.Student.student_code == student_code).first()
        return student is not None

    def create_student(self, student_in: schemas.StudentModel.StudentCreate):
        new_student = models.Student(
            student_code=student_in.student_code,
            full_name=student_in.full_name,
            email=student_in.email,
            class_id=student_in.class_id
        )
        self.db.add(new_student)
        self.db.commit()
        self.db.refresh(new_student)
        return self.db.query(models.Student).options(joinedload(models.Student.classroom)).filter(models.Student.id == new_student.id).first()   