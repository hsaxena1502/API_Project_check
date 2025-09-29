"""
Integration tests for the Objects API using Page Object Model.
"""
import pytest
from restapi_automation.models.object_model import ObjectModel
from restapi_automation.core.base_client import BaseAPIClient
from restapi_automation.pages.objects_page import ObjectsPage

@pytest.fixture
def api_client():
    """Create an API client for testing."""
    return BaseAPIClient(
        base_url="https://api.example.com/v1",
        headers={"Content-Type": "application/json"}
    )

@pytest.fixture
def objects_page(api_client):
    """Create an ObjectsPage instance for testing."""
    return ObjectsPage(api_client)

def test_get_all_objects(objects_page):
    """Test getting all objects."""
    objects = objects_page.get_all_objects()
    assert isinstance(objects, list)


def test_create_and_get_object(objects_page):
    """Test creating and retrieving an object."""
    # Create test data
    test_object = ObjectModel(
        name="Test Object",
        data={"key": "value"}
    )
    
    # Test create
    created = objects_page.create_object(test_object)
    assert created.id is not None
    assert created.name == test_object.name
    
    # Test get
    fetched = objects_page.get_object(created.id)
    assert fetched.id == created.id
    assert fetched.name == test_object.name


def test_update_object(objects_page):
    """Test updating an object."""
    # Create initial object
    test_object = ObjectModel(name="Initial Name")
    created = objects_page.create_object(test_object)
    
    # Update object
    created.name = "Updated Name"
    updated = objects_page.update_object(created)
    
    # Verify update
    assert updated.name == "Updated Name"
    fetched = objects_page.get_object(created.id)
    assert fetched.name == "Updated Name"


def test_delete_object(objects_page):
    """Test deleting an object."""
    # Create test object
    test_object = ObjectModel(name="To be deleted")
    created = objects_page.create_object(test_object)
    
    # Delete object
    assert objects_page.delete_object(created.id)
    
    # Verify deletion (should raise 404)
    with pytest.raises(Exception) as exc_info:
        objects_page.get_object(created.id)
    assert "404" in str(exc_info.value)


def test_options_request(objects_page):
    """Test OPTIONS request."""
    options = objects_page.get_object_options()
    assert isinstance(options, dict)
    assert 'allow' in options  # Standard OPTIONS response header
