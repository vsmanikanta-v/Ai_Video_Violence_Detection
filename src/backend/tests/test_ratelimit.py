"""Tests for rate limiting (slowapi).

Rate limiting is disabled in the main app during tests (RATELIMIT_ENABLED=false in conftest).
These tests verify that:
  1. The real app's limiter is correctly wired to app.state.
  2. The RateLimitExceeded exception handler is registered.
  3. A locally-constructed rate-limited endpoint can actually return 429 when exceeded.
"""

import os

from app.main import app as main_app
from fastapi import FastAPI, Request
from fastapi.testclient import TestClient
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address


def test_main_app_has_limiter_on_state():
    """The real app attaches a SlowAPI Limiter instance to app.state.limiter."""
    assert hasattr(main_app.state, "limiter"), "app.state.limiter not set"
    assert isinstance(main_app.state.limiter, Limiter)


def test_main_app_limiter_uses_remote_address():
    """The real app's limiter uses get_remote_address as key function."""
    assert main_app.state.limiter._key_func is get_remote_address


def test_main_app_has_rate_limit_exceeded_handler():
    """The real app registers a handler for RateLimitExceeded."""
    assert (
        RateLimitExceeded in main_app.exception_handlers
    ), "RateLimitExceeded handler not registered in app.exception_handlers"


def test_rate_limited_endpoint_returns_429_when_exceeded():
    """A rate-limited endpoint returns 429 after the limit is exceeded.

    Uses a fixed key_func (not get_remote_address) because TestClient does not expose
    request.client.host reliably; the fixed key guarantees all requests share one counter.

    Temporarily sets RATELIMIT_ENABLED=true because SlowAPI's Limiter reads the env var
    at construction time via get_app_config, overriding the enabled=True parameter.
    """
    old_val = os.environ.get("RATELIMIT_ENABLED")
    os.environ["RATELIMIT_ENABLED"] = "true"
    try:
        limiter = Limiter(key_func=lambda request: "test_ip", default_limits=[])
        test_app = FastAPI()
        test_app.state.limiter = limiter
        test_app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

        @test_app.get("/limited")
        @limiter.limit("2 per minute")
        async def limited_endpoint(request: Request):
            return {"ok": True}

        client = TestClient(test_app, raise_server_exceptions=False)
        assert client.get("/limited").status_code == 200
        assert client.get("/limited").status_code == 200
        assert client.get("/limited").status_code == 429
    finally:
        if old_val is None:
            os.environ.pop("RATELIMIT_ENABLED", None)
        else:
            os.environ["RATELIMIT_ENABLED"] = old_val
