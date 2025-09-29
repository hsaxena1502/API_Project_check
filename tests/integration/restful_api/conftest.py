"""Pytest configuration and fixtures for RESTful API tests."""
import pytest
import requests
from typing import Generator

BASE_URL = "https://api.restful-api.dev"


class RestfulAPIClient:
    """Client for interacting with the RESTful API."""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })
    
    def get_objects(self) -> dict:
        """Get all objects."""
        response = self.session.get(f"{self.base_url}/objects")
        response.raise_for_status()
        return response.json()
    
    def get_object(self, object_id: str) -> dict:
        """Get a specific object by ID."""
        response = self.session.get(f"{self.base_url}/objects/{object_id}")
        response.raise_for_status()
        return response.json()
    
    def create_object(self, data: dict) -> dict:
        """Create a new object."""
        response = self.session.post(
            f"{self.base_url}/objects",
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def update_object(self, object_id: str, data: dict) -> dict:
        """Update an existing object."""
        response = self.session.put(
            f"{self.base_url}/objects/{object_id}",
            json=data
        )
        response.raise_for_status()
        return response.json()
    
    def delete_object(self, object_id: str) -> dict:
        """Delete an object."""
        response = self.session.delete(f"{self.base_url}/objects/{object_id}")
        response.raise_for_status()
        return response.json()


@pytest.fixture(scope="session")
def api_client() -> Generator[RestfulAPIClient, None, None]:
    """
    Fixture that provides a configured API client.
    
    Yields:
        RestfulAPIClient: Configured client for making API requests
    """
    client = RestfulAPIClient(BASE_URL)
    yield client
    # Cleanup code if needed
    client.session.close()
