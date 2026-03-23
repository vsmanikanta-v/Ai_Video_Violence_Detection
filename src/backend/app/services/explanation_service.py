"""GenAI incident explanation service for video violence detection.

Uses Google Gemini to generate human-readable incident reports from detection
results (violence score, confidence, timestamps). When GEMINI_API_KEY is not
set, returns safe mock explanations. All prompts are project-specific (zero-copy).
"""

import logging
from dataclasses import dataclass

from app.config import settings

logger = logging.getLogger(__name__)

# Maximum length for normalized explanation text (chars)
MAX_EXPLANATION_LENGTH = 2000

# Cached Gemini client instance; initialized on first use (per process)
_genai_client = None
_genai_missing_warned = False


@dataclass
class DetectionInput:
    """Validated input for incident explanation.

    violence_score: 0.0–1.0; clamped if out of range.
    prediction: VIOLENT | NON_VIOLENT.
    confidence_level: HIGH | MEDIUM | LOW; invalid values default to LOW.
    key_frame_timestamps: optional list of seconds; default [].
    processing_time_seconds: optional float; default None.
    """

    violence_score: float
    prediction: str
    confidence_level: str
    key_frame_timestamps: list[int]
    processing_time_seconds: float | None


def _validate_and_normalize(
    violence_score: float,
    prediction: str,
    confidence_level: str,
    key_frame_timestamps: list[int] | None = None,
    processing_time_seconds: float | None = None,
) -> DetectionInput:
    """Validate and apply safe defaults. Returns DetectionInput."""
    score = max(0.0, min(1.0, float(violence_score)))
    pred = str(prediction).strip().upper() if prediction else "NON_VIOLENT"
    if pred not in ("VIOLENT", "NON_VIOLENT"):
        pred = "NON_VIOLENT"
    conf = str(confidence_level).strip().upper() if confidence_level else "LOW"
    if conf not in ("HIGH", "MEDIUM", "LOW"):
        conf = "LOW"
    timestamps = list(key_frame_timestamps) if key_frame_timestamps is not None else []
    proc_time = float(processing_time_seconds) if processing_time_seconds is not None else None
    return DetectionInput(
        violence_score=score,
        prediction=pred,
        confidence_level=conf,
        key_frame_timestamps=timestamps,
        processing_time_seconds=proc_time,
    )


def _template_kind(d: DetectionInput) -> str:
    """Return template kind: high_violence, medium_violence, low_violence, non_violent."""
    if d.prediction == "NON_VIOLENT":
        return "non_violent"
    if d.confidence_level == "HIGH":
        return "high_violence"
    if d.confidence_level == "MEDIUM":
        return "medium_violence"
    return "low_violence"


def _build_prompt(d: DetectionInput) -> str:
    """Build project-specific prompt for security analyst incident report.

    Role: security analyst. Integrates score, timestamps, confidence, processing time.
    Template kind drives requested tone (high/medium/low violence vs non-violent).
    """
    kind = _template_kind(d)
    ts_str = ", ".join(str(t) for t in d.key_frame_timestamps[:20]) if d.key_frame_timestamps else "None"
    proc_str = f"{d.processing_time_seconds:.1f}s" if d.processing_time_seconds is not None else "N/A"

    role = (
        "You are a security analyst assistant. Produce a short, professional "
        "incident report for a video violence detection system. Be factual and concise."
    )
    data_block = (
        f"Detection result:\n"
        f"- Violence score: {d.violence_score:.2f} (0.0 = none, 1.0 = maximum)\n"
        f"- Prediction: {d.prediction}\n"
        f"- Confidence level: {d.confidence_level}\n"
        f"- Key frame timestamps (seconds): {ts_str}\n"
        f"- Processing time: {proc_str}\n"
    )
    if kind == "non_violent":
        instruction = (
            "The video was classified as NON_VIOLENT. Write a brief confirmation "
            "sentence (one or two sentences) suitable for an incident log: no violence detected."
        )
    elif kind == "high_violence":
        instruction = (
            "The video was classified as VIOLENT with HIGH confidence. Write a short "
            "incident report (2–4 sentences): summary, key timestamps if any, and recommended follow-up."
        )
    elif kind == "medium_violence":
        instruction = (
            "The video was classified as VIOLENT with MEDIUM confidence. Write a short "
            "incident note (1–3 sentences): summary and that manual review may be advised."
        )
    else:
        instruction = (
            "The video was classified as VIOLENT with LOW confidence. Write a single "
            "sentence noting possible violence and that verification is recommended."
        )

    return f"{role}\n\n{data_block}\nTask: {instruction}\n\nOutput only the report text, no preamble."


def _normalize_output(raw: str) -> str:
    """Normalize model output: strip, truncate to safe length."""
    if not raw or not isinstance(raw, str):
        return ""
    text = raw.strip()
    if len(text) > MAX_EXPLANATION_LENGTH:
        text = text[: MAX_EXPLANATION_LENGTH - 3] + "..."
    return text


def _mock_explanation(d: DetectionInput) -> str:
    """Return a safe mock explanation when Gemini is unavailable."""
    kind = _template_kind(d)
    if kind == "non_violent":
        return "No violence detected in this video. (Mock explanation — set GEMINI_API_KEY for GenAI.)"
    if kind == "high_violence":
        return (
            f"High-confidence violence detected (score {d.violence_score:.2f}). "
            "Review recommended. (Mock explanation — set GEMINI_API_KEY for GenAI.)"
        )
    if kind == "medium_violence":
        return (
            f"Medium-confidence violence detected (score {d.violence_score:.2f}). "
            "Manual review advised. (Mock explanation — set GEMINI_API_KEY for GenAI.)"
        )
    return (
        f"Low-confidence possible violence (score {d.violence_score:.2f}). "
        "Verification recommended. (Mock explanation — set GEMINI_API_KEY for GenAI.)"
    )


def generate_incident_explanation(
    violence_score: float,
    prediction: str,
    confidence_level: str,
    key_frame_timestamps: list[int] | None = None,
    processing_time_seconds: float | None = None,
) -> str:
    """Generate a human-readable incident explanation from detection results.

    Uses Gemini when GEMINI_API_KEY is set; otherwise returns a mock explanation.
    Failures (timeout, API error) return a safe, user-friendly fallback; no secrets are logged.

    Returns:
        Non-empty string suitable for storage in results.genai_summary.
    """
    global _genai_client, _genai_missing_warned

    d = _validate_and_normalize(
        violence_score=violence_score,
        prediction=prediction,
        confidence_level=confidence_level,
        key_frame_timestamps=key_frame_timestamps,
        processing_time_seconds=processing_time_seconds,
    )

    if not settings.gemini_api_key or not settings.gemini_api_key.strip():
        if not _genai_missing_warned:
            logger.warning("GEMINI_API_KEY not set; explanation service using mock response")
            _genai_missing_warned = True
        return _mock_explanation(d)

    try:
        if _genai_client is None:
            from google import genai  # noqa: PLC0415

            _genai_client = genai.Client(api_key=settings.gemini_api_key)
        prompt = _build_prompt(d)
        response = _genai_client.models.generate_content(model=settings.gemini_model, contents=prompt)
        if response and response.text:
            return _normalize_output(response.text)
        return _mock_explanation(d)
    except Exception as e:
        # Log without secrets (no API key or response content)
        logger.warning("GenAI explanation failed: %s", type(e).__name__, exc_info=False)
        return (
            f"Incident explanation could not be generated ({d.prediction}, {d.confidence_level}). "
            "Please try again or contact support."
        )
