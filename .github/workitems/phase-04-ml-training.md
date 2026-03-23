# Work Item WI-004: Phase 4 - ML Model Training Pipeline

## Status
- [x] Done
- [ ] Not started
- [ ] In progress
- [ ] Blocked

## Goal

Implement an offline training pipeline that produces a serialized ML model for complaint classification.

## Scope

### 1. Training Pipeline

- Load and preprocess training dataset
- TF-IDF vectorization
- Train classifier (Logistic Regression / SVM)
- Evaluate model performance
- Serialize model artifacts

### 2. Model Artifacts

- `complaint_classifier.pkl` - Trained model
- `tfidf_vectorizer.pkl` - Fitted vectorizer
- Model metadata (version, accuracy, training date)

### 3. Training Script

- Command-line executable
- Configurable hyperparameters
- Reproducible with fixed random seed

## Acceptance Criteria

- Training completes without errors
- Model achieves >85% accuracy on test set
- Artifacts saved to `models/` directory
- Training is reproducible (same data → same model)

## Technical Constraints

- Scikit-learn for ML
- Fixed random_state for reproducibility
- No GPU required

## Files Created

- `src/backend/ml/train_model.py`
- `src/backend/models/complaint_classifier.pkl`
- `src/backend/models/tfidf_vectorizer.pkl`

## Training Command

```powershell
cd src/backend
python ml/train_model.py
# Output: Model saved to models/complaint_classifier.pkl
```

## Model Metrics Target

| Metric | Target |
|--------|--------|
| Accuracy | >85% |
| Precision | >80% |
| Recall | >80% |
| F1-Score | >80% |

## Success Criteria

- Model file created and loadable
- Classification report shows acceptable metrics
- Same training run produces identical model
