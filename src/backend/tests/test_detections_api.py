"""API tests for detection results endpoints.

GET /api/detections/result/{result_id} and GET /api/detections/video/{video_id}.
Uses dependency override for get_current_user_id.
"""

from datetime import datetime
from unittest.mock import patch

from fastapi import status
from tests.helpers import override_get_current_user_id


def test_get_detection_by_result_id_requires_auth(test_client):
    """GET /api/detections/result/1 without token returns 401."""
    response = test_client.get("/api/detections/result/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_get_detection_by_result_id_success(test_client, test_user):
    """GET /api/detections/result/{id} with valid token and owned result returns 200 and result."""
    with override_get_current_user_id(test_user.id):
        with patch("app.routers.detections.get_result_by_id") as m_get:
            m_get.return_value = {
                "id": 10,
                "video_id": 1,
                "violence_score": 0.2,
                "prediction": "NON_VIOLENT",
                "confidence_level": "LOW",
                "key_frame_timestamps": [],
                "processing_time_seconds": 0.5,
                "genai_summary": "No violence detected.",
                "created_at": datetime(2026, 3, 14, 12, 0, 0),
            }
            response = test_client.get(
                "/api/detections/result/10",
                headers={"Authorization": "Bearer fake-token-for-test"},
            )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == 10
    assert data["video_id"] == 1
    assert data["prediction"] == "NON_VIOLENT"
    assert data["status"] == "complete"


def test_get_detection_by_result_id_404(test_client, test_user):
    """GET /api/detections/result/{id} when result not found or not owned returns 404."""
    with override_get_current_user_id(test_user.id):
        with patch("app.routers.detections.get_result_by_id", return_value=None):
            response = test_client.get(
                "/api/detections/result/999",
                headers={"Authorization": "Bearer fake-token-for-test"},
            )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_list_detections_by_video_id_requires_auth(test_client):
    """GET /api/detections/video/1 without token returns 401."""
    response = test_client.get("/api/detections/video/1")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_list_detections_by_video_id_success(test_client, test_user):
    """GET /api/detections/video/{id} with valid token and owned video returns 200 and list."""
    with override_get_current_user_id(test_user.id):
        with patch("app.routers.detections.get_video_by_id") as m_video:
            with patch("app.routers.detections.list_results_by_video_id") as m_list:
                m_video.return_value = {"id": 1, "user_id": test_user.id}
                m_list.return_value = [
                    {
                        "id": 1,
                        "video_id": 1,
                        "violence_score": 0.0,
                        "prediction": "NON_VIOLENT",
                        "confidence_level": "LOW",
                        "key_frame_timestamps": [],
                        "processing_time_seconds": 0.1,
                        "genai_summary": "No violence.",
                        "created_at": datetime(2026, 3, 14, 12, 0, 0),
                    }
                ]
                response = test_client.get(
                    "/api/detections/video/1",
                    headers={"Authorization": "Bearer fake-token-for-test"},
                )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["video_id"] == 1
    assert data[0]["status"] == "complete"


def test_list_detections_by_video_id_404(test_client, test_user):
    """GET /api/detections/video/{id} when video not found or not owned returns 404."""
    with override_get_current_user_id(test_user.id):
        with patch("app.routers.detections.get_video_by_id", return_value=None):
            response = test_client.get(
                "/api/detections/video/999",
                headers={"Authorization": "Bearer fake-token-for-test"},
            )
    assert response.status_code == status.HTTP_404_NOT_FOUND
