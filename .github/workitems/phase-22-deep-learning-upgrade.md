# Work Item WI-022: Phase 22 - Deep Learning Upgrade (Future)

## Status
- [ ] Not started
- [ ] In progress
- [ ] Blocked
- [ ] Done

## Goal

Upgrade classification model from Logistic Regression to BERT/RoBERTa for improved accuracy.

## Scope

### 1. Model Selection

- Evaluate BERT, RoBERTa, DistilBERT
- Consider inference speed vs accuracy
- GPU requirements

### 2. Training Pipeline

- Fine-tuning on complaint dataset
- Transfer learning approach
- Model evaluation metrics

### 3. Inference Optimization

- Model quantization
- ONNX export (optional)
- Batch inference support

## Trade-offs

| Model | Accuracy | Speed | GPU Required |
|-------|----------|-------|--------------|
| Logistic Regression | 85% | <10ms | No |
| DistilBERT | 92% | 50ms | Optional |
| BERT-base | 94% | 100ms | Recommended |
| RoBERTa | 95% | 100ms | Recommended |

## Acceptance Criteria

- Model accuracy > 90%
- Inference time acceptable for production
- Graceful fallback to simple model
- Training reproducible

## Technical Constraints

- HuggingFace Transformers
- PyTorch backend
- CPU inference must work (slower)

## Out of Scope

- Custom model architecture
- Distributed training

## Success Criteria

- Accuracy improvement measurable
- Production-ready inference
- Clear upgrade path
