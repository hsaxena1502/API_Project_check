"""Test cases for the RESTful API objects endpoints."""
import pytest


def test_get_all_objects(api_client):
    """Test retrieving all objects."""
    response = api_client.get_objects()
    assert isinstance(response, list), "Response should be a list of objects"


def test_create_and_get_object(api_client):
    """Test creating a new object and then retrieving it."""
    # Test data
    test_data = {
        "name": "Apple MacBook Pro 16",
        "data": {
            "year": 2019,
            "price": 1849.99,
            "CPU model": "Intel Core i9",
            "Hard disk size": "1 TB"
        }
    }
    
    # Create object
    created = api_client.create_object(test_data)
    assert "id" in created, "Response should contain an 'id' field"
    
    # Get created object
    retrieved = api_client.get_object(created["id"])
    
    # Verify data
    assert retrieved["name"] == test_data["name"]
    assert retrieved["data"] == test_data["data"]


def test_update_object(api_client):
    """Test updating an existing object."""
    # Create initial object
    test_data = {
        "name": "Test Object",
        "data": {
            "key1": "value1",
            "key2": 100
        }
    }
    created = api_client.create_object(test_data)
    
    # Update data
    update_data = {
        "name": "Updated Test Object",
        "data": {
            "key1": "updated_value",
            "key2": 200,
            "new_key": "new_value"
        }
    }
    
    # Perform update
    updated = api_client.update_object(created["id"], update_data)
    
    # Verify update
    assert updated["name"] == update_data["name"]
    assert updated["data"] == update_data["data"]


def test_delete_object(api_client):
    """Test deleting an object."""
    # Create object to delete
    test_data = {"name": "Object to delete", "data": {"key": "value"}}
    created = api_client.create_object(test_data)
    
    # Delete the object
    delete_response = api_client.delete_object(created["id"])
    
    # Verify delete response
    assert delete_response.get("message") == f"Object with id = {created['id']} has been deleted."
    
    # Verify object is deleted
    with pytest.raises(Exception) as exc_info:
        api_client.get_object(created["id"])
    
    assert "404" in str(exc_info.value), "Should raise 404 for deleted object"
