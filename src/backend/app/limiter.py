"""Rate limiter instance for the application.

Uses slowapi with in-memory storage. Disabled when RATELIMIT_ENABLED=false (e.g. tests).
"""

from app.config import settings
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.ratelimit_default] if settings.ratelimit_enabled else [],
    enabled=settings.ratelimit_enabled,
)
