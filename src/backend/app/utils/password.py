"""Password hashing utilities using bcrypt.

Provides secure password hashing and verification using bcrypt directly,
with 12 rounds for adequate security without excessive latency.
"""

import bcrypt


def hash_password(password: str) -> str:
    """Hash a plain text password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string

    Example:
        >>> hashed = hash_password("SecurePass123!")
        >>> hashed.startswith("$2b$")
        True
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=12)).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password from database

    Returns:
        True if password matches, False otherwise

    Example:
        >>> hashed = hash_password("SecurePass123!")
        >>> verify_password("SecurePass123!", hashed)
        True
        >>> verify_password("WrongPassword", hashed)
        False
    """
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())
