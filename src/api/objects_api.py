"""
API client for the /objects endpoint.
"""
from typing import Dict, Any, List, Optional, Type, TypeVar
from dataclasses import dataclass
from .client import APIClient

T = TypeVar('T', bound='ObjectModel')

@dataclass
class ObjectModel:
    """Base model for API objects."""
    id: str = ""
    name: str = ""
    data: Dict[str, Any] = None
    
    @classmethod
    def from_dict(cls: Type[T], data: Dict[str, Any]) -> T:
        """Create an ObjectModel from a dictionary."""
        return cls(**data)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary."""
        return {k: v for k, v in self.__dict__.items() if not k.startswith('_')}


class ObjectsPage:
    """Page Object for the /objects endpoint."""
    
    def __init__(self, client: APIClient):
        """Initialize with an API client."""
        self.api = ObjectsAPI(client)
    
    def get_all_objects(self) -> List[ObjectModel]:
        """Get all objects.
        
        Returns:
            List of ObjectModel instances
        """
        objects_data = self.api.get_all_objects()
        return [ObjectModel.from_dict(obj) for obj in objects_data]
        
    def get_object_options(self) -> Dict[str, Any]:
        """Get available HTTP methods and other options for the objects endpoint.
        
        Returns:
            Dictionary containing the allowed HTTP methods and other options
        """
        return self.api.get_options()
    
    def get_object(self, object_id: str) -> ObjectModel:
        """Get a specific object by ID.
        
        Args:
            object_id: The ID of the object to retrieve
            
        Returns:
            The requested ObjectModel instance
        """
        obj_data = self.api.get_object(object_id)
        return ObjectModel.from_dict(obj_data)
    
    def create_object(self, data: Dict[str, Any]) -> ObjectModel:
        """Create a new object.
        
        Args:
            data: The object data to create
            
        Returns:
            The created ObjectModel instance with ID
        """
        obj_data = self.api.create_object(data)
        return ObjectModel.from_dict(obj_data)
    
    def update_object(self, object_id: str, data: Dict[str, Any]) -> ObjectModel:
        """Update an existing object.
        
        Args:
            object_id: The ID of the object to update
            data: The data to update
            
        Returns:
            The updated ObjectModel instance
        """
        obj_data = self.api.update_object(object_id, data)
        return ObjectModel.from_dict(obj_data)
    
    def delete_object(self, object_id: str) -> bool:
        """Delete an object.
        
        Args:
            object_id: The ID of the object to delete
            
        Returns:
            True if deletion was successful
        """
        return self.api.delete_object(object_id)
    
    def get_options(self) -> Dict[str, Any]:
        """Get available HTTP methods and other options.
        
        Returns:
            Dictionary of available options
        """
        return self.api.get_options()

class ObjectsAPI:
    """Client for interacting with the /objects API endpoint."""
    
    def __init__(self, client: APIClient = None):
        """Initialize with an API client.
        
        Args:
            client: Optional APIClient instance. If not provided, a new one will be created.
        """
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
        response = self.client.patch(f"objects/{object_id}", json=data)
        return response.json()

    def get_options(self) -> Dict[str, Any]:
        """Get available HTTP methods and other options for the objects endpoint.
        
        Returns:
            Dictionary containing the allowed HTTP methods and other options
        """
        response = self.client.options("objects")
        return response.json()
