"""
API client for the /objects endpoint.
"""
from typing import Dict, Any, List, Optional
from .client import APIClient

class ObjectsAPI:
    """Client for interacting with the /objects API endpoint."""
    
    def __init__(self, client: APIClient = None):
        """Initialize with an API client."""
        self.client = client or APIClient()
    
    def get_all_objects(self) -> List[Dict[str, Any]]:
        """Get all objects.
        
        Returns:
            List of all objects
        """
        response = self.client.get("objects")
        return response.json()
    
    def get_object(self, object_id: str) -> Dict[str, Any]:
        """Get a specific object by ID.
        
        Args:
            object_id: The ID of the object to retrieve
            
        Returns:
            The requested object
        """
        response = self.client.get(f"objects/{object_id}")
        return response.json()
    
    def create_object(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new object.
        
        Args:
            data: The object data to create
            
        Returns:
            The created object with ID
        """
        response = self.client.post("objects", json_data=data)
        return response.json()
    
    def update_object(self, object_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing object.
        
        Args:
            object_id: The ID of the object to update
            data: The updated object data
            
        Returns:
            The updated object
        """
        response = self.client.put(f"objects/{object_id}", json_data=data)
        return response.json()
    
    def delete_object(self, object_id: str) -> bool:
        """Delete an object.
        
        Args:
            object_id: The ID of the object to delete
            
        Returns:
            True if deletion was successful
        """
        response = self.client.delete(f"objects/{object_id}")
        return response.status_code == 200
    
    def patch_object(self, object_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Partially update an object.
        
        Args:
            object_id: The ID of the object to update
            data: The fields to update
            
        Returns:
            The patched object
        """
        response = self.client.patch(f"objects/{object_id}", json_data=data)
        return response.json()
