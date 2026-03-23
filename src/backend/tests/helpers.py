"""Shared test utilities for backend tests.

Provides helper context managers and functions used across multiple test modules.
"""

from contextlib import contextmanager

from app.main import app
from app.utils.jwt_handler import get_current_user_id


@contextmanager
def override_get_current_user_id(user_id: int):
    """Temporarily override get_current_user_id dependency to return user_id."""

    async def _override():
        return user_id

    app.dependency_overrides[get_current_user_id] = _override
    try:
        yield
    finally:
        app.dependency_overrides.pop(get_current_user_id, None)
