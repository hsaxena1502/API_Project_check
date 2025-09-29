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
    
    # Database settings
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_NAME = os.getenv("DB_NAME", "fastapi_db")
    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
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
def load_test_data(filename: str) -> Dict[str, Any]:
    """Load test data from JSON or YAML file."""
    file_path = Config.TEST_DATA_DIR / filename
    with open(file_path, 'r', encoding='utf-8') as f:
        if file_path.suffix.lower() == '.json':
            import json
            return json.load(f)
        elif file_path.suffix.lower() in ('.yaml', '.yml'):
            return yaml.safe_load(f)
        else:
            raise ValueError(f"Unsupported file format: {file_path.suffix}")

# Create a settings instance to be imported by other modules
settings = Config()
