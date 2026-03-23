"""Request-level helpers (correlation ID, etc.)."""

from fastapi import Request


def get_request_id(request: Request) -> str | None:
    """Return optional correlation ID from request headers.

    Checks X-Request-ID and Request-Id. Used for audit and tracing.

    Args:
        request: FastAPI request.

    Returns:
        Header value or None if not set.
    """
    return request.headers.get("X-Request-ID") or request.headers.get("Request-Id")
