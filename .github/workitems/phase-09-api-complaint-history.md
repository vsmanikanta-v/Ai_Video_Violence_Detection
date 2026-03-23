# Work Item WI-009: Phase 9 - Complaint History Endpoint

## Status
- [ ] Not started
- [ ] In progress
- [ ] Blocked
- [ ] Done

## Goal

Implement the `GET /api/complaints/{id}` endpoint to retrieve individual complaint details with classification results.

## Scope

### 1. Endpoint Implementation

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/complaints/{id}` | Get complaint by ID |

### 2. Response Data

- Original complaint text
- Classification result (category, confidence)
- AI explanation
- Timestamps (created, classified)

### 3. Error Handling

- 404 if complaint not found
- Proper JSON error format

## Acceptance Criteria

- Endpoint returns complete complaint data
- Joins data from complaints, classifications, explanations tables
- Proper 404 handling for non-existent IDs
- Response matches documented format

## API Response Format

```json
{
  "id": 123,
  "complaint_text": "I was charged twice...",
  "category": "Billing Issue",
  "confidence": 0.91,
  "explanation": "The complaint mentions duplicate charges...",
  "created_at": "2026-01-16T14:30:00Z",
  "classified_at": "2026-01-16T14:30:02Z"
}
```

## Technical Notes

- Use SQLAlchemy joins for efficient query
- Consider pagination for user's complaint history
- May need authentication for user-specific data

## Files Modified

- `src/backend/app.py` - Add route
- Create complaint retrieval service

## Success Criteria

- Single complaint retrieval works
- All related data included
- Performance acceptable (<200ms)
