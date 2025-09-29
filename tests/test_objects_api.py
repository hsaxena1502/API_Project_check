"""
Tests for the Objects API.
"""
import json
import pytest
from pathlib import Path
from datetime import datetime

from src.api.objects_api import ObjectsAPI
from src.utils.config import load_test_data

# Load test data
test_data = load_test_data("test_objects.json")

@pytest.fixture
def objects_api():
    """Fixture to provide an initialized ObjectsAPI client."""
    return ObjectsAPI()

class TestObjectsAPI:
    """Test suite for the Objects API."""
    
    def test_get_all_objects(self, objects_api):
        """Test getting all objects."""
        response = objects_api.get_all_objects()
        assert isinstance(response, list)
    
    def test_create_and_retrieve_object(self, objects_api):
        """Test creating and retrieving an object."""
        # Create a new object
        new_object = test_data["valid_object"].copy()
        new_object["created_at"] = datetime.utcnow().isoformat()
        
        # Create the object
        created = objects_api.create_object(new_object)
        assert created["name"] == new_object["name"]
        assert "id" in created
        
        # Retrieve the object
        retrieved = objects_api.get_object(created["id"])
        assert retrieved["id"] == created["id"]
        assert retrieved["name"] == new_object["name"]
        
        # Clean up
        objects_api.delete_object(created["id"])
    
    def test_update_object(self, objects_api):
        """Test updating an object."""
        # Create a test object
        new_object = test_data["valid_object"].copy()
        created = objects_api.create_object(new_object)
        
        try:
            # Update the object
            update_data = test_data["update_data"].copy()
            updated = objects_api.update_object(created["id"], update_data)
            
            # Verify the update
            assert updated["name"] == update_data["name"]
            assert updated["data"] == update_data["data"]
            
            # Verify the update persisted
            retrieved = objects_api.get_object(created["id"])
            assert retrieved["name"] == update_data["name"]
        finally:
            # Clean up
            objects_api.delete_object(created["id"])
    
    def test_delete_object(self, objects_api):
        """Test deleting an object."""
        # Create a test object
        new_object = test_data["valid_object"].copy()
        created = objects_api.create_object(new_object)
        
        # Delete the object
        assert objects_api.delete_object(created["id"]) is True
        
        # Verify the object is deleted
        with pytest.raises(Exception):
            objects_api.get_object(created["id"])
    
    def test_partial_update(self, objects_api):
        """Test partially updating an object."""
        # Create a test object
        new_object = test_data["valid_object"].copy()
        created = objects_api.create_object(new_object)
        
        try:
            # Partially update the object
            update_data = test_data["partial_update"].copy()
            updated = objects_api.patch_object(created["id"], update_data)
            
            # Verify the partial update
            assert updated["name"] == update_data["name"]
            assert updated["data"] == new_object["data"]  # Should remain unchanged
        finally:
            # Clean up
            objects_api.delete_object(created["id"])
