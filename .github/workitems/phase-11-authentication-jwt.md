# Work Item WI-011: Phase 11 - JWT Authentication

## Status
- [ ] Not started
- [ ] In progress
- [ ] Blocked
- [ ] Done

## Goal

Implement JWT-based authentication for securing API endpoints.

## Scope

### 1. Auth Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | User registration |
| POST | `/api/auth/login` | User login (returns JWT) |
| POST | `/api/auth/refresh` | Refresh access token |

### 2. JWT Implementation

- Use `flask-jwt-extended`
- Access token expiration (24 hours)
- Refresh token support
- Secure secret key from environment

### 3. Password Security

- Bcrypt hashing with salt
- Password strength validation
- Never store plain-text passwords

## Acceptance Criteria

- Registration creates user with hashed password
- Login returns valid JWT token
- Protected endpoints reject invalid tokens
- Token expiration works correctly

## API Response - Login

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "Bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "username": "john_doe",
    "role": "USER"
  }
}
```

## Technical Constraints

- JWT secret from `JWT_SECRET_KEY` env var
- Tokens signed with HS256 algorithm
- No sensitive data in token payload

## Configuration

```powershell
$env:JWT_SECRET_KEY = "your-secure-random-key"
```

## Files Modified

- `src/backend/app.py` - JWT configuration
- Create auth routes and services

## Success Criteria

- Secure password storage
- Token generation works
- Token validation works
- Refresh flow works
