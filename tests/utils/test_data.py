"""Test data for API tests."""
from typing import Dict, Any

from pydantic import EmailStr

from src.pycharm_api.models.user import UserCreate


def user_data_factory(
    email: str = "test@example.com",
    password: str = "testpass123",
    full_name: str = "Test User"
) -> Dict[str, Any]:
    """Generate test user data."""
    return {
        "email": email,
        "password": password,
        "full_name": full_name,
    }


def create_user_payload(
    email: str = "test@example.com",
    password: str = "testpass123",
    full_name: str = "Test User"
) -> Dict[str, str]:
    """Create a user creation payload."""
    return {
        "email": email,
        "password": password,
        "full_name": full_name,
    }


def user_create_factory(
    email: str = "test@example.com",
    password: str = "testpass123",
    full_name: str = "Test User"
) -> UserCreate:
    """Create a UserCreate instance for testing."""
    return UserCreate(
        email=EmailStr(email),
        password=password,
        full_name=full_name,
    )


def random_email() -> str:
    """Generate a random email for testing."""
    import uuid
    return f"test_{uuid.uuid4().hex[:8]}@example.com"


def auth_headers(client: Any, email: str, password: str) -> Dict[str, str]:
    """Get authentication headers for a test user."""
    response = client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
