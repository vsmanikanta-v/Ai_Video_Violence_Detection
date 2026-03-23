"""Video upload, analysis, and history API.

All endpoints require authentication. History is scoped to the current user.
"""

import logging
import uuid
from pathlib import Path
from typing import Annotated

from app.config import settings
from app.limiter import limiter
from app.models.video import AnalyzeResponse, ResultOut, UploadResponse, VideoOut, VideoWithResultsOut
from app.services.video_service import (
    ALLOWED_VIDEO_EXTENSIONS,
    analyze_video,
    create_video,
    get_video_by_id,
    list_results_by_video_id,
    list_videos_by_user,
    video_out_from_dict,
)
from app.utils.audit_helpers import create_audit_log
from app.utils.jwt_handler import get_current_user_id
from app.utils.request_helpers import get_request_id
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/videos", tags=["Videos"])

MAX_BYTES = settings.max_upload_size_mb * 1024 * 1024


def _safe_save_path(upload_dir: str, user_id: int, original_filename: str) -> tuple[Path, str]:
    """Build a safe file path and stored filename (no path traversal)."""
    ext = Path(original_filename).suffix.lower()
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        ext = ".mp4"
    name = f"{user_id}_{uuid.uuid4().hex[:12]}{ext}"
    path = Path(upload_dir) / name
    return path, name


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload video",
    description=(
        "Upload a video file. Authenticated user only. "
        "File size and format validated. Rate limit: 5 per minute per IP."
    ),
    responses={
        201: {"description": "Video uploaded"},
        400: {"description": "Invalid file type or size"},
        401: {"description": "Not authenticated"},
        429: {"description": "Rate limit exceeded"},
    },
)
@limiter.limit(settings.ratelimit_video_upload)
async def upload_video(
    request: Request,
    user_id: Annotated[int, Depends(get_current_user_id)],
    file: UploadFile = File(...),
) -> UploadResponse:
    """Upload a video; store metadata in DB and audit log."""
    if not file.filename or not file.filename.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Missing filename")
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid file type. Allowed: {', '.join(sorted(ALLOWED_VIDEO_EXTENSIONS))}",
        )

    upload_dir = settings.upload_dir
    Path(upload_dir).mkdir(parents=True, exist_ok=True)
    save_path, stored_name = _safe_save_path(upload_dir, user_id, file.filename)

    size = 0
    try:
        with open(save_path, "wb") as f:
            while chunk := await file.read(1024 * 1024):
                size += len(chunk)
                if size > MAX_BYTES:
                    save_path.unlink(missing_ok=True)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"File too large. Max {settings.max_upload_size_mb} MB",
                    )
                f.write(chunk)
    except HTTPException:
        raise
    except Exception as e:
        logger.error("Video upload I/O error for user %s: %s", user_id, e)
        save_path.unlink(missing_ok=True)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Upload failed")

    file_path_str = str(save_path.resolve())
    video = create_video(
        user_id=user_id,
        file_path=file_path_str,
        filename=file.filename,
        file_size=size,
        duration_seconds=None,
        video_format=ext.lstrip(".").upper(),
    )
    create_audit_log(
        user_id=user_id,
        action="video_uploaded",
        entity_type="video",
        entity_id=video["id"],
        request_context_id=get_request_id(request),
        details=f"filename={file.filename} size={size}",
    )
    out = VideoOut(**video_out_from_dict(video))
    return UploadResponse(video=out, message="Video uploaded successfully")


@router.post(
    "/{video_id}/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze video",
    description=(
        "Run violence detection (ML stub) and GenAI explanation. "
        "Video must belong to current user. Rate limit: 10 per minute per IP."
    ),
    responses={
        200: {"description": "Analysis complete"},
        401: {"description": "Not authenticated"},
        404: {"description": "Video not found"},
        429: {"description": "Rate limit exceeded"},
    },
)
@limiter.limit(settings.ratelimit_video_analysis)
async def analyze_video_endpoint(
    request: Request,
    video_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> AnalyzeResponse:
    """Trigger analysis for a video owned by the current user."""
    result = analyze_video(
        video_id=video_id,
        user_id=user_id,
        request_context_id=get_request_id(request),
    )
    out = ResultOut(**result)
    return AnalyzeResponse(result=out, message="Analysis complete")


@router.get(
    "/history",
    response_model=list[VideoWithResultsOut],
    summary="Analysis history",
    description="List current user's videos with their detection results (newest first).",
    responses={200: {"description": "List of videos with results"}, 401: {"description": "Not authenticated"}},
)
async def get_history(user_id: Annotated[int, Depends(get_current_user_id)]) -> list[VideoWithResultsOut]:
    """Return user-scoped history: each video with its results."""
    videos = list_videos_by_user(user_id)
    result = []
    for v in videos:
        video_out = VideoOut(**video_out_from_dict(v))
        results = list_results_by_video_id(v["id"])
        result.append(VideoWithResultsOut(video=video_out, results=[ResultOut(**r) for r in results]))
    return result


@router.get(
    "/{video_id}",
    response_model=VideoOut,
    summary="Get video",
    description="Get a video by ID. Only owned by current user.",
    responses={
        200: {"description": "Video metadata"},
        401: {"description": "Not authenticated"},
        404: {"description": "Not found"},
    },
)
async def get_video(
    video_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> VideoOut:
    """Return video metadata if it belongs to the current user."""
    video = get_video_by_id(video_id, user_id=user_id)
    if not video:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Video not found")
    return VideoOut(**video_out_from_dict(video))
