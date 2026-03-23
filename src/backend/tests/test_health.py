"""Tests for health check endpoint."""

from datetime import datetime

from fastapi import status


def test_health_check(test_client):
    """Health check returns 200, correct values, valid ISO timestamp, and string types."""
    response = test_client.get("/health")

    assert response.status_code == status.HTTP_200_OK
    assert response.headers.get("content-type", "").startswith("application/json")

    data = response.json()
    assert data["status"] == "healthy"
    assert data["message"] == "All systems operational"
    assert "timestamp" in data
    assert isinstance(data["status"], str)
    assert isinstance(data["message"], str)
    assert isinstance(data["timestamp"], str)
    # Verify timestamp is valid ISO 8601
    datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00"))
