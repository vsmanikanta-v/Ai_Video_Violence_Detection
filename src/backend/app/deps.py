"""Shared FastAPI dependencies for RBAC and auth."""

from typing import Annotated

from app.models.auth import User
from app.services.auth_service import get_user_by_id
from app.utils.jwt_handler import get_current_user_id
from fastapi import Depends, HTTPException, status


async def require_admin(user_id: Annotated[int, Depends(get_current_user_id)]) -> User:
    """Require ADMIN role; raise 403 for non-admin. Use in admin-only routes."""
    user = get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return user
