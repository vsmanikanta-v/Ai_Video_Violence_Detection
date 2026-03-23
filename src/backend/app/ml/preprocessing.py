"""Video preprocessing: frame extraction and normalization for CNN-LSTM inference.

Extracts frames at a configurable FPS, resizes to model input size, and normalizes
pixel values. Deterministic: same video path produces same frame sequence. CPU-only.
"""

from pathlib import Path
from typing import TYPE_CHECKING

from app.config import settings

if TYPE_CHECKING:
    import numpy as np


def _get_cv2():
    """Lazy import of OpenCV. Returns None if not installed."""
    try:
        import cv2  # noqa: PLC0415

        return cv2
    except ImportError:
        return None


def extract_frames(
    video_path: str | Path,
    *,
    fps: float | None = None,
    max_frames: int | None = None,
) -> list["np.ndarray"]:
    """Extract frames from a video file at uniform time intervals.

    Args:
        video_path: Path to video file (e.g. MP4).
        fps: Target frames per second to sample. Default from settings.frame_extract_fps.
        max_frames: Maximum number of frames to return. Default from settings.max_frames.

    Returns:
        List of frames as BGR uint8 arrays (H, W, 3). Empty list on error or unsupported format.
    """
    cv2 = _get_cv2()
    if cv2 is None:
        return []
    video_path = Path(video_path)
    if not str(video_path).strip() or not video_path.exists():
        return []
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        return []
    try:
        target_fps = fps if fps is not None else getattr(settings, "frame_extract_fps", 2.0)
        max_n = max_frames if max_frames is not None else getattr(settings, "max_frames", 32)
        video_fps = cap.get(cv2.CAP_PROP_FPS) or 1.0
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
        if total_frames <= 0:
            return []
        # Deterministic: sample at fixed step so same video -> same indices
        step = max(1.0, video_fps / target_fps)
        indices = []
        i = 0.0
        while len(indices) < max_n and i < total_frames:
            indices.append(int(i))
            i += step
        frames = []
        for idx in indices:
            cap.set(cv2.CAP_PROP_POS_FRAMES, idx)
            ret, frame = cap.read()
            if not ret or frame is None:
                break
            frames.append(frame)
        return frames
    finally:
        cap.release()


def normalize_frames(
    frames: list["np.ndarray"],
    target_height: int | None = None,
    target_width: int | None = None,
) -> "np.ndarray | None":
    """Resize frames to target size and normalize to float32 [0, 1]. Convert BGR -> RGB.

    Returns array of shape (1, T, H, W, 3) for inference, or None if frames empty.
    """
    if not frames:
        return None
    cv2 = _get_cv2()
    if cv2 is None:
        return None
    import numpy as np  # noqa: PLC0415

    h = target_height if target_height is not None else getattr(settings, "model_input_size", 64)
    w = target_width if target_width is not None else getattr(settings, "model_input_size", 64)
    out = []
    for f in frames:
        resized = cv2.resize(f, (w, h), interpolation=cv2.INTER_LINEAR)
        rgb = cv2.cvtColor(resized, cv2.COLOR_BGR2RGB)
        out.append(rgb)
    arr = np.stack(out, axis=0).astype(np.float32) / 255.0
    return np.expand_dims(arr, axis=0)


def preprocess_video(
    video_path: str | Path,
    *,
    fps: float | None = None,
    max_frames: int | None = None,
    target_size: int | None = None,
) -> "np.ndarray | None":
    """Extract and normalize frames from a video for ML inference.

    Same video path and config produces the same output (deterministic).

    Args:
        video_path: Path to video file.
        fps: Override frame extraction FPS.
        max_frames: Override max frames.
        target_size: Override model input size (height and width).

    Returns:
        Array of shape (1, T, H, W, 3), float32 in [0, 1], or None on error.
    """
    frames = extract_frames(video_path, fps=fps, max_frames=max_frames)
    if not frames:
        return None
    size = target_size if target_size is not None else getattr(settings, "model_input_size", 64)
    return normalize_frames(frames, target_height=size, target_width=size)
