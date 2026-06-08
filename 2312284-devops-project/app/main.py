from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from .database import engine, Base, get_db
from .models import Student

Base.metadata.create_all(bind=engine)
app = FastAPI(title="DevOps Student Microservice")

class StudentCreate(BaseModel):
    name: str
    reg_no: str
    email: str

class StudentResponse(BaseModel):
    id: int
    name: str
    reg_no: str
    email: str

    class Config:
        from_attributes = True

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    
    return {
        "status": "ok", 
        "db": db_status, 
        "student": "2312284" 
    }

@app.post("/students", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.reg_no == student.reg_no).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Registration number already exists")
    
    new_student = Student(name=student.name, reg_no=student.reg_no, email=student.email)
    db.add(new_student)
    db.commit()
    db.refresh(new_student)
    return new_student

@app.get("/students", response_model=List[StudentResponse])
def get_all_students(db: Session = Depends(get_db)):
    return db.query(Student).all()

@app.get("/students/{reg_no}", response_model=StudentResponse)
def get_student_by_reg(reg_no: str, db: Session = Depends(get_db)):
    student = db.query(Student).filter(Student.reg_no == reg_no).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
