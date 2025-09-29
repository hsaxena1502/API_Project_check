"""
Pytest configuration and fixtures for testing the FastAPI application.
"""
import os
import time
from tests.utils import TestUser
from tests.utils import user_authentication_headers
from datetime import datetime, timedelta
from typing import Dict, Generator, Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event
from sqlalchemy.orm import Session, sessionmaker
from jose import jwt

from src.api.main import app  # Updated import path to the correct module
from src.utils.config import Config as settings  # Updated import path
from src.models.base import Base  # Updated import path
from src.api.core.database import get_db, SessionLocal  # Import get_db from database module
from src.models.user import User  # Updated import path
from src.api.core.security import get_password_hash, create_access_token  # Updated import path

# Override database URL for testing
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create test engine
engine = create_engine(
    TEST_SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Test user data
TEST_USER_EMAIL = "test@example.com"
TEST_USER_PASSWORD = "testpass123"
TEST_USER_FULL_NAME = "Test User"

# Apply migrations at beginning and end of testing
@pytest.fixture(scope="session", autouse=True)
def apply_migrations():
    """Apply database migrations for testing."""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    try:
        os.unlink("test.db")
    except FileNotFoundError:
        pass

@pytest.fixture(scope="function")
def db_session() -> Generator[Session, None, None]:
    """
    Create a fresh database session with a rollback at the end of each test.
    """
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Start a nested transaction
    nested = connection.begin_nested()
    
    # Make sure the session is using the same connection
    session.begin_nested()
    
    @event.listens_for(session, 'after_transaction_end')
    def end_savepoint(session, transaction):
        nonlocal nested
        if not nested.is_active:
            nested = connection.begin_nested()
    
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture(scope="function")
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client that uses the test database session.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up overrides
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
async def async_client():
    """Create an async test client."""
    from httpx import AsyncClient
    from src.api.main import app
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client

# Mock external services
@pytest.fixture(scope="function")
def mock_external_service(monkeypatch):
    """Mock external service calls."""
    # Example: Mock an external API call
    def mock_get(*args, **kwargs):
        class MockResponse:
            @staticmethod
            def json():
                return {"key": "mocked_value"}
            
            status_code = 200
        
        return MockResponse()
    
    monkeypatch.setattr("requests.get", mock_get)
    return mock_get


# Authentication test fixtures
@pytest.fixture
def test_user(db_session: Session) -> User:
    """Create a test user in the database."""
    email = "test@example.com"
    password = "testpass123"
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        full_name="Test User",
        is_active=True,
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


@pytest.fixture
def test_user_headers(client: TestClient, test_user: User) -> Dict[str, str]:
    """Get authentication headers for the test user."""
    return user_authentication_headers(
        client=client, email=test_user.email, password="testpass123"
    )


@pytest.fixture
def authorized_client(client: TestClient, test_user_headers: Dict[str, str]) -> TestClient:
    """Get a test client with authentication headers."""
    client.headers.update(test_user_headers)
    return client


@pytest.fixture
def test_user_client(client: TestClient, db_session: Session) -> TestUser:
    """Get a test user with authentication."""
    return TestUser(client=client, db=db_session)


# Override application dependencies for testing
def override_get_db():
    """Override the get_db dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
