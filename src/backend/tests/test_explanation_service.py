"""Unit tests for GenAI incident explanation service.

Mocks Gemini API; verifies mock mode, success path, and safe fallback on failure.
"""

from unittest.mock import MagicMock, patch

from app.services.explanation_service import (
    DetectionInput,
    _build_prompt,
    _mock_explanation,
    _normalize_output,
    _template_kind,
    _validate_and_normalize,
    generate_incident_explanation,
)


def test_validate_and_normalize_clamps_score():
    """Violence score is clamped to 0.0–1.0."""
    d = _validate_and_normalize(1.5, "VIOLENT", "HIGH")
    assert d.violence_score == 1.0
    d = _validate_and_normalize(-0.1, "NON_VIOLENT", "LOW")
    assert d.violence_score == 0.0


def test_validate_and_normalize_prediction_defaults():
    """Invalid prediction defaults to NON_VIOLENT."""
    d = _validate_and_normalize(0.5, "unknown", "MEDIUM")
    assert d.prediction == "NON_VIOLENT"
    d = _validate_and_normalize(0.5, "VIOLENT", "HIGH")
    assert d.prediction == "VIOLENT"


def test_validate_and_normalize_confidence_defaults():
    """Invalid confidence_level defaults to LOW."""
    d = _validate_and_normalize(0.5, "VIOLENT", "INVALID")
    assert d.confidence_level == "LOW"


def test_template_kind():
    """Template kind matches prediction and confidence."""
    assert _template_kind(DetectionInput(0.1, "NON_VIOLENT", "LOW", [], None)) == "non_violent"
    assert _template_kind(DetectionInput(0.9, "VIOLENT", "HIGH", [], None)) == "high_violence"
    assert _template_kind(DetectionInput(0.65, "VIOLENT", "MEDIUM", [], None)) == "medium_violence"
    assert _template_kind(DetectionInput(0.4, "VIOLENT", "LOW", [], None)) == "low_violence"


def test_build_prompt_includes_data():
    """Prompt contains score, prediction, confidence, timestamps."""
    d = DetectionInput(0.87, "VIOLENT", "HIGH", [12, 18], 3.5)
    prompt = _build_prompt(d)
    assert "0.87" in prompt
    assert "VIOLENT" in prompt
    assert "HIGH" in prompt
    assert "12" in prompt and "18" in prompt
    assert "3.5" in prompt
    assert "security analyst" in prompt.lower()


def test_normalize_output_strips_and_truncates():
    """Output is stripped and truncated to max length."""
    assert _normalize_output("  short  ") == "short"
    long_str = "x" * 2500
    out = _normalize_output(long_str)
    assert len(out) == 2000
    assert out.endswith("...")


def test_mock_explanation_non_violent():
    """Mock explanation for non-violent is non-empty and mentions no violence."""
    d = DetectionInput(0.1, "NON_VIOLENT", "LOW", [], None)
    text = _mock_explanation(d)
    assert text
    assert "violence" in text.lower() or "no " in text.lower() or "mock" in text.lower()


def test_mock_explanation_high_violence():
    """Mock explanation for high violence includes score."""
    d = DetectionInput(0.9, "VIOLENT", "HIGH", [], None)
    text = _mock_explanation(d)
    assert "0.90" in text or "0.9" in text
    assert "High" in text or "high" in text or "mock" in text.lower()


def test_generate_incident_explanation_mock_mode():
    """Without API key, generate_incident_explanation returns mock text."""
    with patch("app.services.explanation_service.settings") as m:
        m.gemini_api_key = None
        m.gemini_model = "gemini-3-flash-preview"
        out = generate_incident_explanation(0.2, "NON_VIOLENT", "LOW")
    assert out
    assert "mock" in out.lower() or "GEMINI" in out


def test_generate_incident_explanation_empty_key_uses_mock():
    """Empty API key is treated as mock mode."""
    with patch("app.services.explanation_service.settings") as m:
        m.gemini_api_key = "   "
        m.gemini_model = "gemini-3-flash-preview"
        out = generate_incident_explanation(0.8, "VIOLENT", "HIGH")
    assert out
    assert "mock" in out.lower() or "GEMINI" in out or "High-confidence" in out


def test_generate_incident_explanation_success_returns_normalized():
    """With API key and valid client, returns normalized text from the response."""
    fake_response = MagicMock()
    fake_response.text = "Summary: Violent content detected. Review recommended."

    mock_client = MagicMock()
    mock_client.models.generate_content.return_value = fake_response

    with patch("app.services.explanation_service.settings") as m:
        m.gemini_api_key = "test-key"
        m.gemini_model = "gemini-3-flash-preview"
        with patch("app.services.explanation_service._genai_client", mock_client):
            out = generate_incident_explanation(0.87, "VIOLENT", "HIGH")
    assert out
    assert "Summary" in out or "Violent" in out or "Review" in out


def test_generate_incident_explanation_api_error_returns_safe_message():
    """When Gemini raises, return safe user-friendly message."""
    mock_client = MagicMock()
    mock_client.models.generate_content.side_effect = RuntimeError("API error")
    with patch("app.services.explanation_service.settings") as m:
        m.gemini_api_key = "test-key"
        m.gemini_model = "gemini-3-flash-preview"
        with patch("app.services.explanation_service._genai_client", mock_client):
            out = generate_incident_explanation(0.5, "VIOLENT", "MEDIUM")
    assert out
    assert "could not be generated" in out or "try again" in out or "support" in out
    assert "API error" not in out


def test_generate_incident_explanation_valid_inputs_produce_output():
    """Valid inputs always produce non-empty output (mock or real)."""
    with patch("app.services.explanation_service.settings") as m:
        m.gemini_api_key = None
        m.gemini_model = "gemini-3-flash-preview"
        for pred, conf in [("VIOLENT", "HIGH"), ("VIOLENT", "LOW"), ("NON_VIOLENT", "LOW")]:
            out = generate_incident_explanation(0.5, pred, conf)
            assert out, f"Empty output for prediction={pred} confidence={conf}"
