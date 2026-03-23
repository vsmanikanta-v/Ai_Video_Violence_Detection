"""Pydantic models for video upload, analysis, and history API."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class VideoOut(BaseModel):
    """Video metadata for API responses (no sensitive path details)."""

    id: int = Field(..., description="Video ID")
    user_id: int = Field(..., description="Owner user ID")
    filename: str = Field(..., description="Original filename")
    file_size: int | None = Field(None, description="File size in bytes")
    duration_seconds: int | None = Field(None, description="Duration in seconds")
    video_format: str | None = Field(None, description="Format (e.g. MP4)")
    uploaded_at: datetime = Field(..., description="Upload timestamp")


class ResultOut(BaseModel):
    """Detection result for API responses."""

    id: int = Field(..., description="Result ID")
    video_id: int = Field(..., description="Video ID")
    violence_score: float = Field(..., ge=0.0, le=1.0, description="Violence probability 0–1")
    prediction: Literal["VIOLENT", "NON_VIOLENT"] = Field(..., description="VIOLENT or NON_VIOLENT")
    confidence_level: Literal["HIGH", "MEDIUM", "LOW"] = Field(..., description="HIGH, MEDIUM, or LOW")
    key_frame_timestamps: list[int] = Field(default_factory=list, description="Timestamps in seconds")
    processing_time_seconds: float | None = Field(None, description="Inference time")
    genai_summary: str | None = Field(None, description="Incident explanation")
    created_at: datetime = Field(..., description="Result timestamp")
    status: Literal["pending", "complete", "failed"] = Field(
        default="complete",
        description="Detection status: complete (sync), pending/failed (if async added later)",
    )


class VideoWithResultsOut(BaseModel):
    """Video with its detection results for history."""

    video: VideoOut = Field(..., description="Video metadata")
    results: list[ResultOut] = Field(default_factory=list, description="Detection results (newest first)")


class UploadResponse(BaseModel):
    """Response after successful video upload."""

    video: VideoOut = Field(..., description="Created video")
    message: str = Field(default="Video uploaded successfully", description="Status message")


class AnalyzeResponse(BaseModel):
    """Response after video analysis (ML + GenAI)."""

    result: ResultOut = Field(..., description="Detection result with GenAI summary")
    message: str = Field(default="Analysis complete", description="Status message")
