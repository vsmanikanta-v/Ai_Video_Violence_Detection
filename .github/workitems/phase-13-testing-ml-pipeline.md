# Work Item WI-013: Phase 13 - ML Pipeline Unit Tests

## Status
- [ ] Not started
- [ ] In progress
- [ ] Blocked
- [ ] Done

## Goal

Create comprehensive unit tests for the ML pipeline components (preprocessing, vectorization, prediction).

## Scope

### 1. Preprocessing Tests

- Text cleaning edge cases
- Empty string handling
- Unicode character handling
- Determinism verification

### 2. Vectorization Tests

- TF-IDF transform consistency
- Feature dimension verification
- Unknown words handling

### 3. Predictor Tests

- Model loading
- Prediction accuracy
- Confidence score range
- Category mapping

## Test Cases

```python
# test_preprocessing.py
def test_lowercase_conversion():
    assert preprocess("HELLO") == "hello"

def test_special_chars_removed():
    assert preprocess("hello!!!") == "hello"

def test_deterministic_output():
    text = "Test input"
    assert preprocess(text) == preprocess(text)

# test_predictor.py
def test_model_loads():
    classifier = ComplaintClassifier()
    assert classifier.model is not None

def test_prediction_returns_category():
    result = classifier.predict("billing issue")
    assert result["category"] in VALID_CATEGORIES

def test_confidence_in_range():
    result = classifier.predict("some complaint")
    assert 0.0 <= result["confidence"] <= 1.0
```

## Acceptance Criteria

- Test coverage > 80% for ML modules
- All edge cases covered
- Tests run in < 30 seconds
- No external dependencies (mock APIs)

## Technical Constraints

- Use pytest framework
- Mock external services
- Fixed random seeds for reproducibility

## Files Created

- `src/backend/tests/test_preprocessing.py`
- `src/backend/tests/test_predictor.py`
- `src/backend/tests/test_training.py`

## Success Criteria

- All tests pass
- Coverage report shows > 80%
- Tests are deterministic
