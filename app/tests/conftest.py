import os
import pytest

# CRITICAL: Force an isolated local SQLite file database for testing 
# before any other application modules load and attempt to connect!
TEST_DB_URL = "sqlite:///./test.db"
os.environ["DATABASE_URL"] = TEST_DB_URL

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app

# Create clean testing database engine
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db():
    # Build database schema from scratch for this test
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop everything cleanly when the test completes
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("./test.db"):
            try:
                os.remove("./test.db")
            except OSError:
                pass

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
