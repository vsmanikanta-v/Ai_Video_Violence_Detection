# Work Item WI-007: Phase 7 - Core API Endpoints

## Status
- [x] Done
- [ ] Not started
- [ ] In progress
- [ ] Blocked

## Goal

Implement the core REST API endpoints for health checks, complaint classification, and explanation retrieval.

## Scope

### 1. Public Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | System health check |
| GET | `/api/info` | API metadata |

### 2. Classification Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/complaints` | Submit complaint |
| POST | `/api/classify` | Classify & explain |

### 3. Explanation Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/explanation/{id}` | Get stored explanation |

## Acceptance Criteria

- All endpoints return valid JSON
- Error responses follow consistent format
- Classification returns category + confidence + explanation
- Database persistence works correctly

## Technical Constraints

- RESTful design principles
- JSON request/response format
- Proper HTTP status codes

## API Response Format

### Success (POST /api/classify)

```json
{
  "complaint_id": 123,
  "category": "Billing Issue",
  "confidence": 0.91,
  "explanation": "The complaint mentions duplicate charges..."
}
```

### Error

```json
{
  "error": "Invalid input",
  "message": "complaint_text is required",
  "status": 400
}
```

## Files Modified

- `src/backend/app.py` - Route registration
- Create route handlers

## Success Criteria

- All endpoints accessible and functional
- Responses match documented format
- Database records created correctly
- Health check validates all components
