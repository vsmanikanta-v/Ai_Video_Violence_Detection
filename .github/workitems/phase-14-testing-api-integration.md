# Work Item WI-014: Phase 14 - API Integration Tests

## Status
- [ ] Not started
- [ ] In progress
- [ ] Blocked
- [ ] Done

## Goal

Create integration tests for API endpoints using Flask's test client.

## Scope

### 1. Health & Info Tests

- Health endpoint returns 200
- Info endpoint returns metadata

### 2. Classification Tests

- POST /api/classify with valid input
- POST /api/classify with missing text
- Response format validation

### 3. Explanation Tests

- GET /api/explanation/{id} returns stored data
- 404 for non-existent ID

### 4. Auth Tests (when implemented)

- Login returns token
- Protected endpoints reject without token
- Token validation works

## Test Cases

```python
# test_api.py
def test_health_endpoint(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json['status'] == 'healthy'

def test_classify_valid_input(client):
    response = client.post('/api/classify', json={
        'complaint_text': 'I was charged twice'
    })
    assert response.status_code == 200
    assert 'category' in response.json
    assert 'confidence' in response.json

def test_classify_missing_text(client):
    response = client.post('/api/classify', json={})
    assert response.status_code == 400
```

## Acceptance Criteria

- All endpoints have test coverage
- Error scenarios tested
- Response format validated
- Tests use in-memory database

## Technical Constraints

- Use pytest with Flask test client
- Mock GenAI API calls
- Use test database (SQLite)

## Files Created

- `src/backend/tests/test_api.py`
- `src/backend/tests/conftest.py` (fixtures)

## Success Criteria

- All API tests pass
- Tests run independently
- No real database/API calls
