"""Authentication service for user management.

Handles user registration, login, and profile retrieval.
Integrates with PostgreSQL database for user storage.
"""

import logging

import psycopg2
from app.db import get_db_connection
from app.models.auth import User
from app.utils.password import hash_password, verify_password
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)


def register_user(username: str, email: str, password: str, role: str) -> User:
    """Register a new user account.

    Args:
        username: Unique username
        email: Unique email address
        password: Plain text password (will be hashed)
        role: User role (USER or ADMIN)

    Returns:
        User object with created user information

    Raises:
        HTTPException: 409 if username or email already exists
        HTTPException: 503 if database operation fails
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Hash the password
        password_hash = hash_password(password)

        # Insert user into database
        cursor.execute(
            """
            INSERT INTO users (username, email, password_hash, role)
            VALUES (%s, %s, %s, %s)
            RETURNING id, username, email, role, created_at
            """,
            (username, email, password_hash, role),
        )

        user_data = cursor.fetchone()
        conn.commit()

        # Create User object
        user = User(
            id=user_data[0], username=user_data[1], email=user_data[2], role=user_data[3], created_at=user_data[4]
        )

        return user

    except psycopg2.errors.UniqueViolation:
        if conn:
            conn.rollback()
        # Generic message to prevent user enumeration (OWASP)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
            headers={"error_code": "USER_CONFLICT"},
        )
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error("Database error in register_user: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def authenticate_user(username: str, password: str) -> User | None:
    """Authenticate a user with username and password.

    Args:
        username: Username to authenticate
        password: Plain text password to verify

    Returns:
        User object if authentication successful, None otherwise

    Raises:
        HTTPException: 503 if database operation fails
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get user from database
        cursor.execute(
            """
            SELECT id, username, email, password_hash, role, created_at
            FROM users
            WHERE username = %s
            """,
            (username,),
        )

        user_data = cursor.fetchone()

        if user_data is None:
            return None

        # Verify password
        if not verify_password(password, user_data[3]):
            return None

        # Create User object
        user = User(
            id=user_data[0], username=user_data[1], email=user_data[2], role=user_data[4], created_at=user_data[5]
        )

        return user

    except psycopg2.Error as e:
        logger.error("Database error in authenticate_user: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_user_by_id(user_id: int) -> User | None:
    """Get user by ID.

    Args:
        user_id: User ID to retrieve

    Returns:
        User object if found, None otherwise

    Raises:
        HTTPException: 503 if database operation fails
    """
    conn = None
    cursor = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get user from database
        cursor.execute(
            """
            SELECT id, username, email, role, created_at
            FROM users
            WHERE id = %s
            """,
            (user_id,),
        )

        user_data = cursor.fetchone()

        if user_data is None:
            return None

        # Create User object
        user = User(
            id=user_data[0], username=user_data[1], email=user_data[2], role=user_data[3], created_at=user_data[4]
        )

        return user

    except psycopg2.Error as e:
        logger.error("Database error in get_user_by_id: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
