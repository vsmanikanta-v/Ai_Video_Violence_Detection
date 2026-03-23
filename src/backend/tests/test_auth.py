"""Tests for authentication endpoints and RBAC."""

from unittest.mock import MagicMock, patch

from fastapi import status
from fastapi.exceptions import HTTPException


def test_register_success(test_client, test_user):
    """Test successful user registration.

    Args:
        test_client: FastAPI test client fixture
        test_user: Test user fixture
    """
    with patch("app.routers.auth.register_user", new=MagicMock(return_value=test_user)):
        response = test_client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "SecurePass123!",
                "role": "USER",
            },
        )

        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert "token_type" in data
        assert data["user"]["username"] == "testuser"
        assert data["token_type"] == "bearer"


def test_register_validation_error(test_client):
    """Test registration with invalid data.

    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.post(
        "/api/auth/register", json={"username": "ab", "email": "invalid-email", "password": "short"}
    )

    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_register_duplicate_returns_409_generic_message(test_client):
    """Test registration with duplicate username/email returns 409 and generic message (no enumeration)."""
    with patch(
        "app.routers.auth.register_user",
        new=MagicMock(side_effect=HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")),
    ):
        response = test_client.post(
            "/api/auth/register",
            json={
                "username": "existing",
                "email": "existing@example.com",
                "password": "SecurePass123!",
                "role": "USER",
            },
        )
    assert response.status_code == status.HTTP_409_CONFLICT
    data = response.json()
    assert data.get("detail") == "User already exists"


def test_login_success(test_client, test_user):
    """Test successful user login.

    Args:
        test_client: FastAPI test client fixture
        test_user: Test user fixture
    """
    with patch("app.routers.auth.authenticate_user", new=MagicMock(return_value=test_user)):
        response = test_client.post("/api/auth/login", json={"username": "testuser", "password": "SecurePass123!"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "user" in data
        assert "access_token" in data
        assert "token_type" in data
        assert data["user"]["username"] == "testuser"
        assert data["token_type"] == "bearer"


def test_login_invalid_credentials(test_client):
    """Test login with invalid credentials.

    Args:
        test_client: FastAPI test client fixture
    """
    with patch("app.routers.auth.authenticate_user", new=MagicMock(return_value=None)):
        response = test_client.post("/api/auth/login", json={"username": "testuser", "password": "WrongPassword"})

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        data = response.json()
        assert "detail" in data


def test_get_current_user_success(test_client, test_user):
    """Test getting current user with valid token.

    Args:
        test_client: FastAPI test client fixture
        test_user: Test user fixture
    """
    # First register/login to get token
    with patch("app.routers.auth.register_user", new=MagicMock(return_value=test_user)):
        register_response = test_client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "SecurePass123!",
                "role": "USER",
            },
        )
        token = register_response.json()["access_token"]

    # Then try to get current user
    with patch("app.routers.auth.get_user_by_id", new=MagicMock(return_value=test_user)):
        response = test_client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "user" in data
        assert data["user"]["username"] == "testuser"


def test_get_current_user_no_token(test_client):
    """Test getting current user without token.

    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/api/auth/me")

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_current_user_invalid_token(test_client):
    """Test getting current user with invalid token.

    Args:
        test_client: FastAPI test client fixture
    """
    response = test_client.get("/api/auth/me", headers={"Authorization": "Bearer invalid_token"})

    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_check_returns_403_for_user(test_client, test_user):
    """Test admin-only endpoint returns 403 for non-admin (USER role)."""
    with patch("app.routers.auth.register_user", new=MagicMock(return_value=test_user)):
        reg = test_client.post(
            "/api/auth/register",
            json={
                "username": "testuser",
                "email": "test@example.com",
                "password": "SecurePass123!",
                "role": "USER",
            },
        )
    token = reg.json()["access_token"]
    with patch("app.deps.get_user_by_id", new=MagicMock(return_value=test_user)):
        response = test_client.get("/api/auth/admin-check", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in response.json()


def test_admin_check_returns_200_for_admin(test_client, test_admin_user, admin_token):
    """Test admin-only endpoint returns 200 for ADMIN role."""
    with patch("app.deps.get_user_by_id", new=MagicMock(return_value=test_admin_user)):
        response = test_client.get("/api/auth/admin-check", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data.get("message") == "Admin access granted"
    assert "user_id" in data
