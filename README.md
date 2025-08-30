# Go REST API with Python Tests

This is a simple RESTful API built with Go and tested with Python's pytest framework.

## Features

- CRUD operations for items
- CORS support
- Comprehensive test coverage
- Clean code structure

## Prerequisites

- Go 1.21 or higher
- Python 3.7 or higher
- pip (Python package installer)

## Setup

### 1. Install Go Dependencies

```bash
cd go-rest-api
go mod download
```

### 2. Install Python Dependencies

```bash
pip install -r requirements.txt
```

## Running the API

Start the Go API server:

```bash
cd go-rest-api
go run main.go
```

The server will start on `http://localhost:8000`

## API Endpoints

- `GET /api/items` - Get all items
- `GET /api/items/{id}` - Get a specific item
- `POST /api/items` - Create a new item
- `PUT /api/items/{id}` - Update an existing item
- `DELETE /api/items/{id}` - Delete an item
- `OPTIONS /api/items` - CORS preflight request

## Running Tests

Make sure the API server is running, then run the tests:

```bash
pytest tests/ -v --html=test_report.html
```

This will run all tests and generate an HTML test report.

## Test Coverage

The test suite covers:
- Getting all items
- Getting a single item
- Creating a new item
- Updating an existing item
- Deleting an item
- CORS support
- Error handling for non-existent items

## Project Structure

```
.
├── go-rest-api/
│   ├── handlers/      # Request handlers
│   ├── models/        # Data models
│   ├── utils/         # Utility functions
│   ├── go.mod        # Go module file
│   └── main.go       # Main application file
├── tests/
│   └── test_api.py   # Test cases
├── requirements.txt  # Python dependencies
└── README.md        # This file
```
