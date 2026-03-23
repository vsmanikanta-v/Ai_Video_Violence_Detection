"""Validation helpers for email and password.

Reusable checks for auth and registration; aligns with Pydantic models
(RegisterRequest) where used. Kept in utils for reuse and testability.
"""

import re

# Simple email pattern (aligned with common usage; for strict validation use pydantic EmailStr)
EMAIL_RE = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

PASSWORD_MIN_LEN = 8
PASSWORD_MAX_LEN = 100


def validate_email(email: str) -> bool:
    """Return True if email looks valid.

    Args:
        email: Email string to check.

    Returns:
        True if format is valid.
    """
    if not email or not isinstance(email, str):
        return False
    return bool(EMAIL_RE.fullmatch(email.strip()))


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password length and basic rules.

    Args:
        password: Plain text password.

    Returns:
        (True, "") if valid; (False, "error message") otherwise.
    """
    if not isinstance(password, str):
        return False, "Password must be a string"
    if len(password) < PASSWORD_MIN_LEN:
        return False, f"Password must be at least {PASSWORD_MIN_LEN} characters"
    if len(password) > PASSWORD_MAX_LEN:
        return False, f"Password must be at most {PASSWORD_MAX_LEN} characters"
    return True, ""
