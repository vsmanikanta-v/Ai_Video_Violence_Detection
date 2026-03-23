"""Inference-only ML pipeline for violence probability from frame sequences.

Loads a pre-trained Keras/TensorFlow model from a configurable path and produces
violence probability (0.0–1.0). No training; CPU-only. When no model path is set
or the model file is missing, callers should use a stub.
"""

import logging
import time
from pathlib import Path
from threading import Lock
from typing import Any

from app.config import settings

logger = logging.getLogger(__name__)

# Lazy import so the app loads without TensorFlow when ML_MODEL_PATH is unset
_keras: Any = None

_lock = Lock()
_model: Any = None
_load_attempted = False


def _get_keras():
    """Lazy import of Keras. Returns None if not installed."""
    global _keras
    if _keras is not None:
        return _keras
    try:
        import keras  # noqa: PLC0415

        _keras = keras
        return _keras
    except ImportError:
        return None


class ModelNotFoundError(FileNotFoundError):
    """Raised when ML_MODEL_PATH is set but the model file does not exist."""

    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(
            f"ML model file not found: {path}. "
            "Set ML_MODEL_PATH to a valid Keras saved model (.keras) or leave unset to use stub."
        )


def _load_model_once() -> bool:
    """Load model from settings.ml_model_path if set. Thread-safe. Returns True if model loaded."""
    global _model, _load_attempted
    path = settings.ml_model_path
    if not path or not str(path).strip():
        return False
    path = Path(path).resolve()
    with _lock:
        if _model is not None:
            return True
        if _load_attempted:
            return False
        _load_attempted = True
        if not path.exists():
            raise ModelNotFoundError(str(path))
        keras = _get_keras()
        if keras is None:
            raise ImportError("TensorFlow/Keras is required for ML inference. Install with: pip install tensorflow")
        _model = keras.models.load_model(str(path), compile=False)
        return True


def score_to_prediction(score: float) -> str:
    """Map violence score to VIOLENT or NON_VIOLENT."""
    return "VIOLENT" if score >= 0.5 else "NON_VIOLENT"


def score_to_confidence(score: float) -> str:
    """Map violence score to HIGH, MEDIUM, or LOW confidence."""
    if score >= 0.8 or score <= 0.2:
        return "HIGH"
    if score >= 0.6 or score <= 0.4:
        return "MEDIUM"
    return "LOW"


def run_inference(  # noqa: C901
    frames: Any = None,
) -> tuple[float, str, str, list[int], float] | None:
    """Run model inference on a frame sequence.

    Args:
        frames: Frame sequence as numpy array of shape (batch, ...) or (batch, T, H, W, C).
                If None or model not configured, returns None (caller should use stub).

    Returns:
        (violence_score, prediction, confidence_level, key_frame_timestamps, processing_time_sec)
        or None if no model loaded or frames is None.
    """
    if frames is None:
        return None
    try:
        loaded = _load_model_once()
    except (ModelNotFoundError, ImportError):
        return None
    if not loaded or _model is None:
        return None
    keras = _get_keras()
    if keras is None:
        return None
    import numpy as np  # noqa: PLC0415

    if not hasattr(frames, "shape"):
        frames = np.asarray(frames)
    batch_size = getattr(settings, "inference_batch_size", 16) or 16
    start = time.perf_counter()
    try:
        preds = _model.predict(frames, batch_size=batch_size, verbose=0)
    except Exception as e:
        logger.error("Model inference failed: %s", e)
        return None
    elapsed = time.perf_counter() - start
    # preds may be (N,) or (N, 1) or (N, T); take scalar clip score
    preds = np.asarray(preds)
    if preds.size == 0:
        return None
    score = float(np.clip(preds.flat[-1], 0.0, 1.0))
    if preds.ndim >= 2 and preds.shape[0] > 1:
        score = float(np.clip(preds.mean(), 0.0, 1.0))
    prediction = score_to_prediction(score)
    confidence = score_to_confidence(score)
    return (score, prediction, confidence, [], elapsed)
