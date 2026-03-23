# Work Item WI-005: Phase 5 - ML Inference Service

## Status
- [x] Done
- [ ] Not started
- [ ] In progress
- [ ] Blocked

## Goal

Implement an inference service that loads the trained model and predicts complaint categories with confidence scores.

## Scope

### 1. Predictor Module

- Load serialized model and vectorizer
- Preprocess input text
- Return prediction with confidence score

### 2. Inference API

- Single prediction for one complaint
- Batch prediction support (optional)
- Error handling for model loading failures

### 3. Confidence Scoring

- Return probability estimates
- Map to confidence levels (HIGH/MEDIUM/LOW)

## Acceptance Criteria

- Model loads successfully at startup
- Predictions are deterministic
- Confidence scores range 0.0-1.0
- Graceful error handling if model missing

## Technical Constraints

- Inference must be fast (<100ms per prediction)
- No retraining during inference
- Thread-safe for concurrent requests

## Files Created

- `src/backend/ml/predictor.py`

## API Interface

```python
from ml.predictor import ComplaintClassifier

classifier = ComplaintClassifier()
result = classifier.predict("I was charged twice")

# Result:
# {
#     "category": "Billing Issue",
#     "confidence": 0.91,
#     "all_probabilities": {...}
# }
```

## Complaint Categories

1. Billing Issue
2. Service Quality
3. Delivery Problem
4. Product Defect
5. Account Issue
6. Fraud/Security

## Success Criteria

- Predictions match expected categories
- Response time < 100ms
- Confidence accurately reflects certainty
