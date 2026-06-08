from sqlalchemy import Column, Integer, String
from .database import Base

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    reg_no = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=False)
