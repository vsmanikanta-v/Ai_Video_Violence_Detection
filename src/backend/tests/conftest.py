"""Pytest configuration and fixtures for backend tests.

Provides test client, mock database, and test user fixtures.
"""

import os

# Set test environment variables BEFORE any imports (CI may set TEST_DATABASE_URL)
os.environ["JWT_SECRET_KEY"] = "test-secret-key-for-testing-only"
os.environ["JWT_ALGORITHM"] = "HS256"
os.environ["JWT_ACCESS_TOKEN_EXPIRE_MINUTES"] = "30"
os.environ.setdefault("CREATE_DEFAULT_USERS", "false")
os.environ["DATABASE_URL"] = os.environ.get(
    "TEST_DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/test_db"
)
os.environ.setdefault("RATELIMIT_ENABLED", "false")

from datetime import datetime  # noqa: E402

import pytest  # noqa: E402
from app.main import app  # noqa: E402
from app.models.auth import User  # noqa: E402
from app.utils.jwt_handler import create_access_token  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


@pytest.fixture
def test_client():
    """Create a test client for FastAPI app.

    Returns:
        TestClient instance for making test requests
    """
    return TestClient(app)


@pytest.fixture
def test_user():
    """Create a test user object.

    Returns:
        User object for testing
    """
    return User(
        id=1, username="testuser", email="test@example.com", role="USER", created_at=datetime(2026, 2, 12, 10, 0, 0)
    )


@pytest.fixture
def test_admin_user():
    """Create a test admin user object.

    Returns:
        Admin User object for testing
    """
    return User(
        id=2, username="adminuser", email="admin@example.com", role="ADMIN", created_at=datetime(2026, 2, 12, 10, 0, 0)
    )


@pytest.fixture
def user_token(test_user):
    """Real JWT token for test_user (USER role). Avoids register-endpoint boilerplate."""
    return create_access_token({"user_id": test_user.id, "username": test_user.username, "role": test_user.role})


@pytest.fixture
def admin_token(test_admin_user):
    """Real JWT token for test_admin_user (ADMIN role). Avoids register-endpoint boilerplate."""
    return create_access_token(
        {"user_id": test_admin_user.id, "username": test_admin_user.username, "role": test_admin_user.role}
    )
