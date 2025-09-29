# REST API Test Automation Framework

A robust and maintainable API testing framework built with Python and pytest. This framework is designed for testing RESTful APIs with a clean, scalable architecture.

## Features

- **Modular Design**: Separated API clients, models, and utilities
- **Configuration Management**: Environment-based configuration
- **Test Data Management**: JSON-based test data management
- **Comprehensive Testing**: Built-in support for various test scenarios
- **Type Hints**: Better code completion and type checking

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Project Structure

```
.
├── src/                    # Source code
│   ├── api/               # API clients
│   ├── models/            # Data models
│   └── utils/             # Utility functions
├── tests/                 # Test files
│   ├── test_data/         # Test data files
│   ├── conftest.py        # Pytest fixtures
│   └── test_*.py          # Test cases
├── .env.example          # Example environment variables
├── requirements.txt      # Project dependencies
└── pytest.ini           # Pytest configuration
```

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

## Running Tests

Run all tests:
```bash
pytest -v
```

Run tests with coverage report:
```bash
pytest --cov=src --cov-report=term-missing
```

## Writing Tests

Example test case:

```python
def test_get_all_objects(objects_api):
    """Test getting all objects."""
    response = objects_api.get_all_objects()
    assert isinstance(response, list)
```

## Configuration

Edit `.env` to configure the API endpoint and other settings:

```
API_BASE_URL=https://api.example.com/v1
API_KEY=your_api_key_here
API_TIMEOUT=10
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
