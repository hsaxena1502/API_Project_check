"""Configuration management for the API tests."""
import os
from pathlib import Path
from typing import Dict, Any
import yaml
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Base directory of the project
BASE_DIR = Path(__file__).parent.parent.parent

class Config:
    """Configuration class for API tests."""
    
    # API settings
    BASE_URL = os.getenv("API_BASE_URL", "https://api.example.com/v1")
    TIMEOUT = int(os.getenv("API_TIMEOUT", "10"))
    
    # Auth settings
    API_KEY = os.getenv("API_KEY", "")
    
    # Test settings
    TEST_DATA_DIR = BASE_DIR / "tests" / "test_data"
    
    @classmethod
    def get_headers(cls) -> Dict[str, str]:
        """Get default headers for API requests."""
        return {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {cls.API_KEY}" if cls.API_KEY else ""
        }

# Load test data
def load_test_data(filename: str) -> Any:
    """Load test data from JSON or YAML file."""
    filepath = Config.TEST_DATA_DIR / filename
    with open(filepath, 'r', encoding='utf-8') as f:
        if filepath.suffix.lower() == '.json':
            import json
            return json.load(f)
        elif filepath.suffix.lower() in ('.yaml', '.yml'):
            return yaml.safe_load(f)
    raise ValueError(f"Unsupported file format: {filepath.suffix}")
