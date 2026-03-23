# Work Item WI-012: Phase 12 - Role-Based Access Control (RBAC)

## Status
- [ ] Not started
- [ ] In progress
- [ ] Blocked
- [ ] Done

## Goal

Implement role-based access control to restrict admin endpoints to authorized users.

## Scope

### 1. User Roles

| Role | Permissions |
|------|-------------|
| USER | Submit complaints, view own history |
| ADMIN | All USER permissions + view all complaints + statistics |

### 2. Endpoint Protection

| Endpoint | Required Role |
|----------|--------------|
| `/api/classify` | Public (or USER) |
| `/api/complaints/{id}` | USER (own) or ADMIN |
| `/api/admin/complaints` | ADMIN only |
| `/api/admin/statistics` | ADMIN only |

### 3. Implementation

- Role stored in user table
- Role included in JWT claims
- Decorator for role checking

## Acceptance Criteria

- Role enforcement at API layer (not UI only)
- Admin endpoints reject non-admin users
- Users can only access own data
- Clear 403 error for unauthorized access

## Role Decorator

```python
@admin_required
def get_all_complaints():
    # Only accessible to ADMIN role
    pass
```

## Error Response (403)

```json
{
  "error": "Forbidden",
  "message": "Admin access required",
  "status": 403
}
```

## Dependencies

- Requires WI-011 (JWT Authentication)

## Success Criteria

- Role enforcement works correctly
- Non-admin users cannot access admin endpoints
- Users can only see own complaints (unless admin)
