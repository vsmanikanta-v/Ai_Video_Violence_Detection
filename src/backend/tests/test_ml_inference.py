"""Tests for ML inference module."""

from unittest.mock import MagicMock, patch

import numpy as np
from app.ml.inference import ModelNotFoundError, run_inference, score_to_confidence, score_to_prediction


def test_score_to_prediction():
    """Prediction is VIOLENT for score >= 0.5, else NON_VIOLENT."""
    assert score_to_prediction(0.0) == "NON_VIOLENT"
    assert score_to_prediction(0.49) == "NON_VIOLENT"
    assert score_to_prediction(0.5) == "VIOLENT"
    assert score_to_prediction(1.0) == "VIOLENT"


def test_score_to_confidence():
    """Confidence levels derived from score thresholds."""
    assert score_to_confidence(0.1) == "HIGH"
    assert score_to_confidence(0.9) == "HIGH"
    assert score_to_confidence(0.5) == "LOW"
    assert score_to_confidence(0.65) == "MEDIUM"
    assert score_to_confidence(0.35) == "MEDIUM"


def test_run_inference_returns_none_when_frames_none():
    """When frames is None, run_inference returns None (caller uses stub)."""
    assert run_inference(None) is None


def test_run_inference_returns_none_when_model_not_configured():
    """When ML_MODEL_PATH is not set, run_inference returns None."""
    with patch("app.ml.inference.settings") as m:
        m.ml_model_path = None
        m.inference_batch_size = 16
        # Reset module state so we don't use a previously loaded model
        import app.ml.inference as mod  # noqa: PLC0415

        mod._model = None
        mod._load_attempted = False
        assert run_inference(np.zeros((1, 2, 2, 2, 3))) is None


def test_run_inference_returns_none_when_model_file_missing():
    """When ML_MODEL_PATH is set but file missing, run_inference returns None (graceful)."""
    import app.ml.inference as mod  # noqa: PLC0415

    mod._model = None
    mod._load_attempted = False
    with patch("app.ml.inference.settings") as m:
        m.ml_model_path = "/nonexistent/path/model.keras"
        m.inference_batch_size = 16
        result = run_inference(np.zeros((1, 2, 2, 2, 3)))
    assert result is None


def test_run_inference_output_shape_and_range_when_mock_model():
    """With a mocked model, run_inference returns (score, pred, conf, timestamps, time) with score in [0,1]."""
    import app.ml.inference as mod  # noqa: PLC0415

    mock = MagicMock()
    mock.predict.return_value = np.array([[0.75]])
    mod._model = mock
    mod._load_attempted = True
    with patch("app.ml.inference.settings") as m:
        m.ml_model_path = "."  # non-empty so _load_model_once returns True (model already set)
        m.inference_batch_size = 16
        with patch.object(mod, "_get_keras", return_value=object()):  # truthy so we don't return None
            result = run_inference(np.zeros((1, 5, 64, 64, 3)))
    try:
        assert result is not None
        score, prediction, confidence, timestamps, proc_time = result
        assert 0.0 <= score <= 1.0
        assert prediction in ("VIOLENT", "NON_VIOLENT")
        assert confidence in ("HIGH", "MEDIUM", "LOW")
        assert isinstance(timestamps, list)
        assert proc_time >= 0
    finally:
        mod._model = None
        mod._load_attempted = False


def test_model_not_found_error_message():
    """ModelNotFoundError has a clear message with the path."""
    err = ModelNotFoundError("/path/to/missing.keras")
    assert "/path/to/missing.keras" in str(err)
    assert "ML_MODEL_PATH" in str(err)
