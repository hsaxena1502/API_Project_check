"""Test utilities and helpers."""
import random
import string
from typing import Any, Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.pycharm_api.models.user import User
from src.pycharm_api.core.security import get_password_hash


def random_lower_string(length: int = 32) -> str:
    """Generate a random lowercase string of specified length."""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def random_email() -> str:
    """Generate a random email."""
    return f"{random_lower_string(8)}@{random_lower_string(8)}.com"


def user_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> Dict[str, str]:
    """Get authentication headers for a user."""
    data = {"username": email, "password": password}
    r = client.post("/api/v1/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    return {"Authorization": f"Bearer {auth_token}"}


def create_random_user(db: Session) -> User:
    """Create a random user in the database."""
    email = random_email()
    password = random_lower_string(12)
    user_in = {
        "email": email,
        "password": password,
        "full_name": random_lower_string(12).capitalize(),
    }
    user = User(
        email=user_in["email"],
        hashed_password=get_password_hash(user_in["password"]),
        full_name=user_in["full_name"],
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


class TestUser:
    """Test user with authentication."""
    
    def __init__(self, client: TestClient, db: Session):
        self.client = client
        self.db = db
        self.user = create_random_user(db)
        self.password = "testpass123"
        self.user.hashed_password = get_password_hash(self.password)
        db.add(self.user)
        db.commit()
        db.refresh(self.user)
        self.headers = user_authentication_headers(
            client=client, email=self.user.email, password=self.password
        )
    
    def get_auth_headers(self) -> Dict[str, str]:
        """Get authentication headers for this user."""
        return self.headers
    
    def get_user_data(self) -> Dict[str, Any]:
        """Get user data as a dictionary."""
        return {
            "id": self.user.id,
            "email": self.user.email,
            "full_name": self.user.full_name,
            "is_active": self.user.is_active,
        }
