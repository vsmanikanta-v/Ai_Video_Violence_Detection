"""Unit tests for app.utils.validators."""

from app.utils.validators import validate_email, validate_password


def test_validate_email_valid():
    """Accept valid-looking emails."""
    assert validate_email("user@example.com") is True
    assert validate_email("a+b@x.co") is True


def test_validate_email_invalid():
    """Reject invalid emails."""
    assert validate_email("") is False
    assert validate_email("notanemail") is False
    assert validate_email("@nodomain.com") is False
    assert validate_email("spaces in@name.com") is False


def test_validate_password_ok():
    """Accept password in length range."""
    ok, msg = validate_password("eightchr")  # 8 chars minimum
    assert ok is True
    assert msg == ""


def test_validate_password_too_short():
    """Reject too short password."""
    ok, msg = validate_password("short")
    assert ok is False
    assert "8" in msg


def test_validate_password_too_long():
    """Reject too long password."""
    ok, msg = validate_password("a" * 101)
    assert ok is False
    assert "100" in msg
