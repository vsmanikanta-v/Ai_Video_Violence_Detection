# Work Item WI-002: Phase 2 - Database Setup

## Status
- [x] Done
- [ ] Not started
- [ ] In progress
- [ ] Blocked

## Goal

Set up PostgreSQL database with SQLAlchemy ORM for persistent storage of complaints, classifications, and explanations.

## Scope

### 1. Database Schema

Create tables for:
- `users` - User accounts and roles
- `complaints` - Raw complaint text submissions
- `classification_results` - ML predictions with confidence scores
- `ai_explanations` - GenAI-generated explanations

### 2. SQLAlchemy Models

- Create ORM models in `src/backend/database/`
- Define relationships between tables
- Add indexes for performance

### 3. Infrastructure

- Docker Compose for PostgreSQL
- Schema initialization script
- Connection pooling configuration

## Acceptance Criteria

- PostgreSQL container starts via `docker compose up`
- SQLAlchemy models map to database tables
- Foreign key relationships work correctly
- Database queries return expected results

## Technical Constraints

- PostgreSQL 13+
- SQLAlchemy 2.x
- Schema must support audit trail

## Files Created

- `src/backend/database/db.py`
- `infra/docker-compose.yml`
- `infra/database/schema.sql`

## Schema Overview

```sql
-- Core tables
users (id, username, role, created_at)
complaints (id, user_id, complaint_text, created_at)
classification_results (id, complaint_id, category, confidence, created_at)
ai_explanations (id, complaint_id, explanation, created_at)
```

## Success Criteria

- All tables created successfully
- ORM operations (CRUD) work
- Relationships enforced at database level
