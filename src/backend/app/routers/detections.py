"""Detection results API.

GET detection by result_id or by video_id. All endpoints require authentication
and return only results for videos owned by the current user.
"""

from typing import Annotated

from app.models.video import ResultOut
from app.services.video_service import get_result_by_id, get_video_by_id, list_results_by_video_id
from app.utils.jwt_handler import get_current_user_id
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api/detections", tags=["Detections"])


@router.get(
    "/result/{result_id}",
    response_model=ResultOut,
    summary="Get detection by result ID",
    description="Return a single detection result. Only if the result's video belongs to the current user.",
    responses={
        200: {"description": "Detection result"},
        401: {"description": "Not authenticated"},
        404: {"description": "Result not found or access denied"},
    },
)
async def get_detection_by_result_id(
    result_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> ResultOut:
    """Get detection result by id (user must own the video)."""
    result = get_result_by_id(result_id, user_id=user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Detection result not found or access denied",
        )
    return ResultOut(**result)


@router.get(
    "/video/{video_id}",
    response_model=list[ResultOut],
    summary="List detections for a video",
    description="Return all detection results for a video. Only if the video belongs to the current user.",
    responses={
        200: {"description": "List of detection results (newest first)"},
        401: {"description": "Not authenticated"},
        404: {"description": "Video not found or access denied"},
    },
)
async def list_detections_by_video_id(
    video_id: int,
    user_id: Annotated[int, Depends(get_current_user_id)],
) -> list[ResultOut]:
    """List detection results for a video (user must own the video)."""
    video = get_video_by_id(video_id, user_id=user_id)
    if not video:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Video not found or access denied",
        )
    results = list_results_by_video_id(video_id)
    return [ResultOut(**r) for r in results]
