"""API router configuration."""
from fastapi import APIRouter

# Create main API router
router = APIRouter()

# Import and include your route modules here
# Example:
# from . import users, items
# router.include_router(users.router, prefix="/users", tags=["users"])
# router.include_router(items.router, prefix="/items", tags=["items"])

# Example root endpoint
@router.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to the API"}
