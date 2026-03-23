# Work Item WI-006: Phase 6 - GenAI Integration (Google Gemini)

## Status
- [x] Done
- [ ] Not started
- [ ] In progress
- [ ] Blocked

## Goal

Integrate Google Gemini API to generate human-readable explanations for ML classification decisions.

## Core Principle

- GenAI is for **explanation only** — it never changes the ML classification
- The ML model remains the source of truth for predictions
- GenAI adds transparency and explainability

## Scope

### 1. Gemini Client

- Initialize Google Generative AI client
- Configure API key from environment
- Handle rate limits and errors

### 2. Explanation Service

- Accept complaint text + predicted category
- Generate natural language explanation
- Return formatted explanation string

### 3. Error Handling

- Graceful degradation if API unavailable
- Fallback message for API failures
- Logging for debugging

## Acceptance Criteria

- Gemini API calls succeed with valid key
- Explanations are relevant to the complaint
- Service handles API errors gracefully
- Explanations stored in database

## Technical Constraints

- Requires `GEMINI_API_KEY` environment variable
- Respect API rate limits
- Keep prompts concise to minimize token usage

## Files Created

- `src/backend/genai/explanation.py`

## API Interface

```python
from genai.explanation import ExplanationService

service = ExplanationService()
explanation = service.generate_explanation(
    complaint_text="I was charged twice for the same item",
    predicted_category="Billing Issue",
    confidence=0.91
)

# Output: "The complaint is classified as Billing Issue because 
#          it mentions duplicate charges..."
```

## Environment Setup

```powershell
$env:GEMINI_API_KEY = "your-api-key-here"
```

## Success Criteria

- Explanations are factual and grounded
- No hallucinations about complaint content
- Response time < 3 seconds
- Graceful fallback on API failure
