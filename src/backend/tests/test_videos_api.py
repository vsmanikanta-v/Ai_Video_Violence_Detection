"""API tests for video upload, analyze, and history.

Mocks DB and ML/GenAI; uses FastAPI dependency_overrides for get_current_user_id.
"""

import tempfile
from datetime import datetime
from io import BytesIO
from unittest.mock import patch

from fastapi import HTTPException, status
from tests.helpers import override_get_current_user_id


def test_upload_requires_auth(test_client):
    """Upload without token returns 401."""
    response = test_client.post("/api/videos/upload", files={"file": ("test.mp4", BytesIO(b"x"), "video/mp4")})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_upload_success(test_client, test_user):
    """Upload with valid token and file returns 201 and video metadata."""
    with override_get_current_user_id(test_user.id):
        with tempfile.TemporaryDirectory() as upload_dir:
            with patch("app.routers.videos.settings") as m_settings:
                m_settings.upload_dir = upload_dir
                m_settings.max_upload_size_mb = 100
                with patch("app.routers.videos.create_video") as m_create:
                    with patch("app.routers.videos.create_audit_log"):
                        m_create.return_value = {
                            "id": 1,
                            "user_id": test_user.id,
                            "filename": "test.mp4",
                            "file_path": "/tmp/1_abc.mp4",
                            "file_size": 1,
                            "duration_seconds": None,
                            "video_format": "MP4",
                            "uploaded_at": datetime(2026, 3, 14, 12, 0, 0),
                        }
                        response = test_client.post(
                            "/api/videos/upload",
                            files={"file": ("test.mp4", BytesIO(b"x"), "video/mp4")},
                            headers={"Authorization": "Bearer fake-token-for-test"},
                        )
                        assert response.status_code == status.HTTP_201_CREATED
                        data = response.json()
                        assert "video" in data
                        assert data["video"]["filename"] == "test.mp4"
                        assert data["video"]["id"] == 1


def test_analyze_requires_auth(test_client):
    """Analyze without token returns 401."""
    response = test_client.post("/api/videos/1/analyze")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_analyze_success(test_client, test_user):
    """Analyze with valid token returns 200 and result with GenAI summary."""
    with override_get_current_user_id(test_user.id):
        with patch("app.routers.videos.analyze_video") as m_analyze:
            m_analyze.return_value = {
                "id": 1,
                "video_id": 1,
                "violence_score": 0.0,
                "prediction": "NON_VIOLENT",
                "confidence_level": "LOW",
                "key_frame_timestamps": [],
                "processing_time_seconds": 0.1,
                "genai_summary": "No violence detected.",
                "created_at": "2026-03-14T12:00:00",
            }
            response = test_client.post(
                "/api/videos/1/analyze",
                headers={"Authorization": "Bearer fake-token-for-test"},
            )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "result" in data
    assert data["result"]["prediction"] == "NON_VIOLENT"
    assert "genai_summary" in data["result"]


def test_analyze_404(test_client, test_user):
    """Analyze for non-existent or wrong-user video returns 404."""
    with override_get_current_user_id(test_user.id):
        with patch("app.routers.videos.analyze_video") as m_analyze:
            m_analyze.side_effect = HTTPException(status_code=404, detail="Video not found")
            response = test_client.post(
                "/api/videos/999/analyze",
                headers={"Authorization": "Bearer fake-token-for-test"},
            )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_history_requires_auth(test_client):
    """History without token returns 401."""
    response = test_client.get("/api/videos/history")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_history_success(test_client, test_user):
    """History with valid token returns 200 and user-scoped list."""
    with override_get_current_user_id(test_user.id):
        with patch("app.routers.videos.list_videos_by_user") as m_list:
            with patch("app.routers.videos.list_results_by_video_id") as m_results:
                m_list.return_value = [
                    {
                        "id": 1,
                        "user_id": test_user.id,
                        "filename": "a.mp4",
                        "file_path": "/x/a.mp4",
                        "file_size": 100,
                        "duration_seconds": None,
                        "video_format": "MP4",
                        "uploaded_at": datetime(2026, 3, 14, 12, 0, 0),
                    }
                ]
                m_results.return_value = []
                response = test_client.get(
                    "/api/videos/history",
                    headers={"Authorization": "Bearer fake-token-for-test"},
                )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["video"]["filename"] == "a.mp4"
    assert data[0]["results"] == []


def test_get_video_404(test_client, test_user):
    """Get video that does not exist or not owned returns 404."""
    with override_get_current_user_id(test_user.id):
        with patch("app.routers.videos.get_video_by_id", return_value=None):
            response = test_client.get(
                "/api/videos/999",
                headers={"Authorization": "Bearer fake-token-for-test"},
            )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_analyze_persists_genai_explanation(test_user):
    """Phase 23: analyze_video calls GenAI explanation and persists it in create_result."""
    from app.services import video_service

    fake_explanation = "Incident explanation from GenAI (or fallback)."
    with patch.object(video_service, "get_video_by_id") as m_get_video:
        with patch.object(video_service, "preprocess_video", return_value=None):
            with patch.object(video_service, "run_inference", return_value=None):
                with patch.object(
                    video_service,
                    "generate_incident_explanation",
                    return_value=fake_explanation,
                ) as m_genai:
                    with patch.object(video_service, "create_result") as m_create:
                        with patch.object(video_service, "log_action"):
                            m_get_video.return_value = {"id": 1, "user_id": test_user.id, "file_path": "/tmp/x.mp4"}
                            m_create.return_value = {
                                "id": 1,
                                "video_id": 1,
                                "violence_score": 0.0,
                                "prediction": "NON_VIOLENT",
                                "confidence_level": "LOW",
                                "key_frame_timestamps": [],
                                "processing_time_seconds": 0.1,
                                "genai_summary": fake_explanation,
                                "created_at": datetime(2026, 3, 14, 12, 0, 0),
                            }
                            result = video_service.analyze_video(
                                video_id=1,
                                user_id=test_user.id,
                            )
    m_genai.assert_called_once()
    m_create.assert_called_once()
    call_kwargs = m_create.call_args[1]
    assert call_kwargs.get("genai_summary") == fake_explanation
    assert result.get("genai_summary") == fake_explanation
