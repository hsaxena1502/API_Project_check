"""Base API client for making HTTP requests."""
import json
from typing import Any, Dict, Optional, Union
import requests
from requests import Response
from src.utils.config import Config

class APIClient:
    """Base API client with common HTTP methods."""
    
    def __init__(self, base_url: str = None, headers: Dict[str, str] = None):
        """Initialize the API client with base URL and headers."""
        self.base_url = base_url or Config.BASE_URL
        self.session = requests.Session()
        self.session.headers.update(Config.get_headers())
        if headers:
            self.session.headers.update(headers)
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Response:
        """Send HTTP request and return response."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        # Add timeout if not specified
        if 'timeout' not in kwargs:
            kwargs['timeout'] = Config.TIMEOUT
            
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response
    
    def get(self, endpoint: str, **kwargs) -> Response:
        """Send GET request."""
        return self._request('GET', endpoint, **kwargs)
    
    def post(self, endpoint: str, data: Any = None, json_data: Any = None, **kwargs) -> Response:
        """Send POST request."""
        return self._request('POST', endpoint, data=data, json=json_data, **kwargs)
    
    def put(self, endpoint: str, data: Any = None, json_data: Any = None, **kwargs) -> Response:
        """Send PUT request."""
        return self._request('PUT', endpoint, data=data, json=json_data, **kwargs)
    
    def delete(self, endpoint: str, **kwargs) -> Response:
        """Send DELETE request."""
        return self._request('DELETE', endpoint, **kwargs)
    
    def patch(self, endpoint: str, data: Any = None, json_data: Any = None, **kwargs) -> Response:
        """Send PATCH request."""
        return self._request('PATCH', endpoint, data=data, json=json_data, **kwargs)
