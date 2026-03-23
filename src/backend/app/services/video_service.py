"""Video and detection result persistence.

Handles video metadata, detection results, and user-scoped history.
ML inference uses app.ml.inference when a model is configured; otherwise stub.
GenAI explanation is generated via app.services.explanation_service.
"""

import logging

import psycopg2
from app.db import get_db_connection
from app.ml.inference import run_inference
from app.ml.preprocessing import preprocess_video
from app.services.audit_service import log_action
from app.services.explanation_service import generate_incident_explanation
from fastapi import HTTPException, status

logger = logging.getLogger(__name__)

# Allowed video extensions for upload validation
ALLOWED_VIDEO_EXTENSIONS = frozenset({".mp4", ".avi", ".webm", ".mov", ".mkv"})

_VIDEO_COLUMNS = "id, user_id, filename, file_path, file_size, duration_seconds, video_format, uploaded_at"
_RESULT_COLUMNS = (
    "id, video_id, violence_score, prediction, confidence_level, "
    "key_frame_timestamps, processing_time_seconds, genai_summary, created_at"
)


def _row_to_video(row: tuple) -> dict:
    """Convert videos table row to dict for VideoOut."""
    return {
        "id": row[0],
        "user_id": row[1],
        "filename": row[2],
        "file_path": row[3],
        "file_size": row[4],
        "duration_seconds": row[5],
        "video_format": row[6],
        "uploaded_at": row[7],
    }


def _row_to_result(row: tuple) -> dict:
    """Convert results table row to dict for ResultOut."""
    return {
        "id": row[0],
        "video_id": row[1],
        "violence_score": row[2],
        "prediction": row[3],
        "confidence_level": row[4],
        "key_frame_timestamps": list(row[5] or []),
        "processing_time_seconds": row[6],
        "genai_summary": row[7],
        "created_at": row[8],
    }


def create_video(
    user_id: int,
    file_path: str,
    filename: str,
    file_size: int | None = None,
    duration_seconds: int | None = None,
    video_format: str | None = None,
) -> dict:
    """Insert a video record. Returns video dict (including id, uploaded_at)."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO videos (user_id, file_path, filename, file_size, duration_seconds, video_format)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id, user_id, filename, file_path, file_size, duration_seconds, video_format, uploaded_at
            """,
            (user_id, file_path, filename, file_size, duration_seconds, video_format),
        )
        row = cur.fetchone()
        conn.commit()
        return _row_to_video(row)
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error("Database error in create_video: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_video_by_id(video_id: int, user_id: int | None = None) -> dict | None:
    """Get video by id. If user_id is set, only return if video belongs to that user."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if user_id is not None:
            cur.execute(
                f"SELECT {_VIDEO_COLUMNS} FROM videos WHERE id = %s AND user_id = %s",
                (video_id, user_id),
            )
        else:
            cur.execute(
                f"SELECT {_VIDEO_COLUMNS} FROM videos WHERE id = %s",
                (video_id,),
            )
        row = cur.fetchone()
        return _row_to_video(row) if row else None
    except psycopg2.Error as e:
        logger.error("Database error: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def list_videos_by_user(user_id: int) -> list[dict]:
    """List videos for a user, newest first."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            f"SELECT {_VIDEO_COLUMNS} FROM videos WHERE user_id = %s ORDER BY uploaded_at DESC",
            (user_id,),
        )
        return [_row_to_video(r) for r in cur.fetchall()]
    except psycopg2.Error as e:
        logger.error("Database error: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def list_results_by_video_id(video_id: int) -> list[dict]:
    """List detection results for a video, newest first."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            f"SELECT {_RESULT_COLUMNS} FROM results WHERE video_id = %s ORDER BY created_at DESC",
            (video_id,),
        )
        return [_row_to_result(r) for r in cur.fetchall()]
    except psycopg2.Error as e:
        logger.error("Database error: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def get_result_by_id(result_id: int, user_id: int | None = None) -> dict | None:
    """Get a detection result by id. If user_id is set, only return if the result's video belongs to that user."""
    conn = None
    cur = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        if user_id is not None:
            cur.execute(
                """
                SELECT r.id, r.video_id, r.violence_score, r.prediction, r.confidence_level,
                       r.key_frame_timestamps, r.processing_time_seconds, r.genai_summary, r.created_at
                FROM results r
                JOIN videos v ON v.id = r.video_id
                WHERE r.id = %s AND v.user_id = %s
                """,
                (result_id, user_id),
            )
        else:
            cur.execute(
                f"SELECT {_RESULT_COLUMNS} FROM results WHERE id = %s",
                (result_id,),
            )
        row = cur.fetchone()
        return _row_to_result(row) if row else None
    except psycopg2.Error as e:
        logger.error("Database error: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def create_result(
    video_id: int,
    violence_score: float,
    prediction: str,
    confidence_level: str,
    key_frame_timestamps: list[int] | None = None,
    processing_time_seconds: float | None = None,
    genai_summary: str | None = None,
) -> dict:
    """Insert a detection result. Returns result dict."""
    conn = None
    cur = None
    try:
        ts = key_frame_timestamps or []
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO results (video_id, violence_score, prediction, confidence_level,
                                 key_frame_timestamps, processing_time_seconds, genai_summary)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id, video_id, violence_score, prediction, confidence_level,
                      key_frame_timestamps, processing_time_seconds, genai_summary, created_at
            """,
            (video_id, violence_score, prediction, confidence_level, ts, processing_time_seconds, genai_summary),
        )
        row = cur.fetchone()
        conn.commit()
        return _row_to_result(row)
    except psycopg2.Error as e:
        if conn:
            conn.rollback()
        logger.error("Database error: %s", e)
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Database error")
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


def run_inference_stub() -> tuple[float, str, str, list[int], float]:
    """Stub when no ML model is configured or inference returns None.

    Returns (score, prediction, confidence, timestamps, time_sec).
    """
    return 0.0, "NON_VIOLENT", "LOW", [], 0.1


def analyze_video(video_id: int, user_id: int, request_context_id: str | None = None) -> dict:
    """Run ML inference (or stub) + GenAI explanation, persist result, audit log. Returns result dict.

    Raises:
        HTTPException: 404 if video not found or not owned by user, 503 on DB error.
    """
    video = get_video_by_id(video_id, user_id=user_id)
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")

    # Extract and normalize frames for ML; if preprocessing fails or returns empty, use stub
    file_path = video.get("file_path")
    frames = preprocess_video(file_path) if file_path else None
    inference_result = run_inference(frames)
    if inference_result is None:
        score, prediction, confidence, timestamps, proc_time = run_inference_stub()
    else:
        score, prediction, confidence, timestamps, proc_time = inference_result
    genai_summary = generate_incident_explanation(
        violence_score=score,
        prediction=prediction,
        confidence_level=confidence,
        key_frame_timestamps=timestamps,
        processing_time_seconds=proc_time,
    )
    db_result = create_result(
        video_id=video_id,
        violence_score=score,
        prediction=prediction,
        confidence_level=confidence,
        key_frame_timestamps=timestamps,
        processing_time_seconds=proc_time,
        genai_summary=genai_summary,
    )
    log_action(
        user_id=user_id,
        action="video_analyzed",
        entity_type="result",
        entity_id=db_result["id"],
        request_context_id=request_context_id,
        details=f"video_id={video_id} prediction={prediction}",
    )
    return db_result


def video_out_from_dict(v: dict) -> dict:
    """Strip file_path from video dict for API response."""
    return {
        k: v[k]
        for k in ("id", "user_id", "filename", "file_size", "duration_seconds", "video_format", "uploaded_at")
        if k in v
    }
