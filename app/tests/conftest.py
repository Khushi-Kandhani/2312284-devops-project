import os
import pytest

# CRITICAL: Force an isolated, pure in-memory SQLite database for testing.
# This completely bypasses file-system read-only and permission blocks!
TEST_DB_URL = "sqlite:///:memory:"
os.environ["DATABASE_URL"] = TEST_DB_URL

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Create clean testing database engine in RAM
# Static pool is required for in-memory SQLite to share the connection across threads safely
from sqlalchemy.pool import StaticPool
engine = create_engine(
    TEST_DB_URL, 
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # 1. Build database schema in RAM from scratch
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        # 2. Close session cleanly
        session.close()
        
        # 3. Wipe the schema so the next test gets a perfectly pristine slate
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db):
    def _get_test_db():
        try:
            yield db
        finally:
            pass
            
    # Safely swap out production DB connections for our mock DB session instance
    app.dependency_overrides[get_db] = _get_test_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
