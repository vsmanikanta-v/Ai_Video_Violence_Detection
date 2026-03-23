"""Tests for video preprocessing: frame extraction and normalization."""

import tempfile
from pathlib import Path

import pytest
from app.ml.preprocessing import extract_frames, normalize_frames, preprocess_video


def test_extract_frames_nonexistent_path_returns_empty():
    """Non-existent video path returns empty list."""
    result = extract_frames(Path("/nonexistent/video.mp4"))
    assert result == []


def test_extract_frames_empty_path_returns_empty():
    """Empty path or missing file returns empty list."""
    result = extract_frames("")
    assert result == []


def test_normalize_frames_empty_list_returns_none():
    """Empty frame list returns None."""
    assert normalize_frames([]) is None


def test_normalize_frames_shape_and_range():
    """normalize_frames returns (1, T, H, W, 3), float32, values in [0, 1]."""
    import numpy as np

    # Two fake BGR frames 100x100
    frames = [
        np.ones((100, 100, 3), dtype=np.uint8) * 128,
        np.zeros((100, 100, 3), dtype=np.uint8),
    ]
    out = normalize_frames(frames, target_height=64, target_width=64)
    assert out is not None
    assert out.ndim == 5
    assert out.shape[0] == 1
    assert out.shape[1] == 2  # T
    assert out.shape[2] == 64
    assert out.shape[3] == 64
    assert out.shape[4] == 3
    assert out.dtype == np.float32
    assert float(out.min()) >= 0.0 and float(out.max()) <= 1.0


def test_preprocess_video_nonexistent_returns_none():
    """preprocess_video with non-existent path returns None."""
    assert preprocess_video("/nonexistent/video.mp4") is None


@pytest.fixture
def minimal_video_path():
    """Create a minimal valid video file and return its path."""
    import os

    try:
        import cv2  # noqa: PLC0415
        import numpy as np  # noqa: PLC0415
    except ImportError:
        pytest.skip("opencv-python-headless required for this test")
    fd, path = tempfile.mkstemp(suffix=".mp4")
    os.close(fd)
    try:
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(path, fourcc, 2.0, (32, 32))
        for _ in range(10):
            out.write(np.zeros((32, 32, 3), dtype=np.uint8))
        out.release()
        yield path
    finally:
        Path(path).unlink(missing_ok=True)


def test_preprocess_video_shape_and_deterministic(minimal_video_path):
    """Same video produces same preprocessed output; shape (1, T, H, W, 3)."""
    import numpy as np

    out1 = preprocess_video(minimal_video_path, target_size=64)
    out2 = preprocess_video(minimal_video_path, target_size=64)
    assert out1 is not None and out2 is not None
    assert out1.shape == out2.shape
    assert out1.ndim == 5 and out1.shape[0] == 1 and out1.shape[4] == 3
    assert out1.dtype == np.float32
    np.testing.assert_allclose(out1, out2, err_msg="Preprocessing should be deterministic")
