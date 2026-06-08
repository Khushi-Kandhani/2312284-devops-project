import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Fall back to PostgreSQL only if no test environment overrides it
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/devops_db")

# 2. CRITICAL: SQLite needs 'check_same_thread: False', PostgreSQL will crash if you pass it.
# This check keeps both environments perfectly happy!
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
