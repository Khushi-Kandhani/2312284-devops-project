from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from pydantic import BaseModel
from .database import engine, Base, get_db
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import engine, Base, get_db
from .models import Student

# 1. Define a lifespan manager to safely initialize the database on app startup only
@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

# 2. Pass lifespan to FastAPI initialization
app = FastAPI(title="DevOps Student Microservice", lifespan=lifespan)

# 3. Clean Pydantic schemas
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

# 4. Cleaned and reconstructed Health Check endpoint
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

# 5. Production routing with precise endpoints
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

@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(Student).all()
