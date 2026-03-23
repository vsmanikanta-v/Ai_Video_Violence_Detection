"""Tests for admin-only API routes.

Non-admin users must receive 403; admin users receive 200 and data.
"""

from unittest.mock import MagicMock, patch

from fastapi import status


def test_admin_stats_requires_auth(test_client):
    """GET /api/admin/stats without token returns 401."""
    response = test_client.get("/api/admin/stats")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_admin_stats_returns_403_for_user(test_client, test_user, user_token):
    """GET /api/admin/stats with USER role returns 403."""
    with patch("app.deps.get_user_by_id", new=MagicMock(return_value=test_user)):
        response = test_client.get("/api/admin/stats", headers={"Authorization": f"Bearer {user_token}"})
    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert "detail" in response.json()


def test_admin_stats_returns_200_for_admin(test_client, test_admin_user, admin_token):
    """GET /api/admin/stats with ADMIN role returns 200 and metrics."""
    with patch("app.deps.get_user_by_id", new=MagicMock(return_value=test_admin_user)):
        with patch("app.routers.admin.get_admin_stats") as m_stats:
            m_stats.return_value = {
                "total_users": 2,
                "total_videos": 5,
                "total_results": 3,
                "total_audit_logs": 10,
            }
            response = test_client.get("/api/admin/stats", headers={"Authorization": f"Bearer {admin_token}"})
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_users"] == 2
    assert data["total_videos"] == 5
    assert data["total_results"] == 3
    assert data["total_audit_logs"] == 10


def test_admin_audit_logs_returns_403_for_user(test_client, test_user, user_token):
    """GET /api/admin/audit-logs with USER role returns 403."""
    with patch("app.deps.get_user_by_id", new=MagicMock(return_value=test_user)):
        response = test_client.get(
            "/api/admin/audit-logs?limit=10&offset=0",
            headers={"Authorization": f"Bearer {user_token}"},
        )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_admin_audit_logs_returns_200_for_admin(test_client, test_admin_user, admin_token):
    """GET /api/admin/audit-logs with ADMIN role returns 200 and list."""
    with patch("app.deps.get_user_by_id", new=MagicMock(return_value=test_admin_user)):
        with patch("app.routers.admin.get_audit_logs") as m_logs:
            m_logs.return_value = [
                {
                    "id": 1,
                    "user_id": 1,
                    "username": "admin",
                    "action": "video_uploaded",
                    "entity_type": "video",
                    "entity_id": 1,
                    "request_context_id": None,
                    "details": "filename=test.mp4",
                    "created_at": "2026-03-14T12:00:00",
                }
            ]
            response = test_client.get(
                "/api/admin/audit-logs?limit=10&offset=0",
                headers={"Authorization": f"Bearer {admin_token}"},
            )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["action"] == "video_uploaded"
    assert data[0]["username"] == "admin"
