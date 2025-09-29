#!/bin/bash

# Exit on error
set -e

# Set Python path
export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run tests with coverage
pytest tests/ -v --cov=src --cov-report=term-missing --cov-report=html

echo "\nTest coverage report generated in htmlcov/index.html"
