# Database - AI Video Violence Detection System

This directory contains the PostgreSQL database schema for the AI Video Violence Detection System.

## 📁 Contents

- `schema.sql` - Complete PostgreSQL schema definition with tables, indexes, and comments

## 🗄️ Database Schema

### Tables

1. **users** - User accounts and authentication
2. **videos** - Uploaded video metadata and file information
3. **results** - Violence detection results and GenAI-generated incident explanations
4. **audit_logs** - System activity tracking and audit trail

### Entity Relationships

```
users (1) ─────< (N) videos
videos (1) ─────< (N) results
users (1) ─────< (N) audit_logs
```

### Key Features

- **Cascade Delete**: When a user is deleted, all their videos and results are automatically removed
- **Audit Preservation**: Audit logs are preserved even if the associated user is deleted (SET NULL)
- **Optimized Indexes**: Composite indexes for efficient query patterns
- **Timestamp Tracking**: All tables include created_at timestamps
- **Confidence Levels**: Results table includes confidence categorization (HIGH, MEDIUM, LOW)

## 🚀 Setup Instructions

### Prerequisites

- PostgreSQL 16 or higher installed and running
- Database admin credentials

### Option 1: Using Docker Compose (recommended)

From the repo root or `infra/` directory:

```powershell
# From repo root
docker compose -f infra/docker-compose.yml up -d

# Schema is applied automatically via /docker-entrypoint-initdb.d/01_schema.sql
# Connection: postgresql://postgres:postgres@localhost:5432/ai_video_violence
```

### Option 2: Using psql (command line)

```bash
# Create the database
psql -U postgres -c "CREATE DATABASE ai_video_violence;"

# Apply the schema (from infra/database or repo root)
psql -U postgres -d ai_video_violence -f schema.sql
```

### Option 3: Using pgAdmin (GUI)

1. Open pgAdmin
2. Right-click on "Databases" → "Create" → "Database..."
3. Name: `ai_video_violence`
4. Click "Save"
5. Right-click on the new database → "Query Tool"
6. Open `schema.sql` and execute

### Verification

After applying the schema, verify the tables were created:

```sql
-- List all tables
SELECT tablename FROM pg_tables WHERE schemaname = 'public';

-- Count rows in each table (should be 0 for new database)
SELECT COUNT(*) FROM users;
SELECT COUNT(*) FROM videos;
SELECT COUNT(*) FROM results;
SELECT COUNT(*) FROM audit_logs;
```

## 📊 Schema Details

### Users Table

| Column        | Type          | Constraints                  |
|---------------|---------------|------------------------------|
| id            | SERIAL        | PRIMARY KEY                  |
| username      | VARCHAR(50)   | UNIQUE, NOT NULL, INDEXED     |
| email         | VARCHAR(255)  | UNIQUE, NOT NULL, INDEXED    |
| password_hash | VARCHAR(255)  | NOT NULL                     |
| role          | VARCHAR(50)   | NOT NULL, DEFAULT 'USER'     |
| created_at    | TIMESTAMP     | NOT NULL, DEFAULT NOW()      |

### Videos Table

| Column          | Type          | Constraints                  |
|-----------------|---------------|------------------------------|
| id              | SERIAL        | PRIMARY KEY                  |
| user_id         | INTEGER       | FK(users.id), NOT NULL       |
| file_path       | TEXT          | NOT NULL                     |
| filename        | VARCHAR(500)  | NOT NULL                     |
| file_size       | BIGINT        | NULLABLE                     |
| duration_seconds| INTEGER       | NULLABLE                     |
| video_format    | VARCHAR(50)   | NULLABLE                     |
| uploaded_at     | TIMESTAMP     | NOT NULL, DEFAULT NOW()      |

**Indexes:**
- `idx_videos_user_id` on (user_id)
- `idx_videos_uploaded_at` on (uploaded_at DESC)
- `idx_videos_user_uploaded` on (user_id, uploaded_at DESC) [composite]

### Results Table

| Column                | Type          | Constraints                  |
|-----------------------|---------------|------------------------------|
| id                    | SERIAL        | PRIMARY KEY                  |
| video_id              | INTEGER       | FK(videos.id), NOT NULL      |
| violence_score        | FLOAT         | NOT NULL, CHECK (0.0-1.0)   |
| prediction            | VARCHAR(50)   | NOT NULL, CHECK (VIOLENT/NON_VIOLENT) |
| confidence_level      | VARCHAR(50)   | NOT NULL, CHECK (HIGH/MEDIUM/LOW) |
| key_frame_timestamps  | INTEGER[]     | NULLABLE                     |
| processing_time_seconds | FLOAT      | NULLABLE                     |
| genai_summary         | TEXT          | NULLABLE                     |
| created_at            | TIMESTAMP     | NOT NULL, DEFAULT NOW()      |

**Indexes:**
- `idx_results_video_id` on (video_id)
- `idx_results_prediction` on (prediction)
- `idx_results_confidence_level` on (confidence_level)
- `idx_results_created_at` on (created_at DESC)
- `idx_results_video_created` on (video_id, created_at DESC) [composite]
- `idx_results_violence_score` on (violence_score DESC)

### Audit Logs Table

| Column            | Type          | Constraints                  |
|-------------------|---------------|------------------------------|
| id                | SERIAL        | PRIMARY KEY                  |
| user_id           | INTEGER       | FK(users.id), NULLABLE       |
| action            | VARCHAR(100)  | NOT NULL                     |
| entity_type       | VARCHAR(50)   | NULLABLE                     |
| entity_id         | INTEGER       | NULLABLE                     |
| request_context_id| VARCHAR(100)  | NULLABLE, INDEXED            |
| details           | TEXT          | NULLABLE                     |
| created_at        | TIMESTAMP     | NOT NULL, DEFAULT NOW()      |

**Indexes:**
- `idx_audit_logs_user_id` on (user_id)
- `idx_audit_logs_created_at` on (created_at DESC)
- `idx_audit_logs_user_created` on (user_id, created_at DESC) [composite]
- `idx_audit_logs_action_created` on (action, created_at DESC) [composite]
- `idx_audit_logs_request_context` on (request_context_id)

## 🔍 Common Queries

### User Video History

```sql
-- Get all videos for a specific user, newest first
SELECT * FROM videos 
WHERE user_id = 1 
ORDER BY uploaded_at DESC;
```

### Video Detection Results

```sql
-- Get detection results for a specific video
SELECT * FROM results 
WHERE video_id = 1 
ORDER BY created_at DESC;
```

### High Confidence Violent Detections (Admin)

```sql
-- Get all high-confidence violent detections across all users
SELECT r.*, v.filename, v.uploaded_at, u.email
FROM results r
JOIN videos v ON r.video_id = v.id
JOIN users u ON v.user_id = u.id
WHERE r.prediction = 'VIOLENT' 
  AND r.confidence_level = 'HIGH'
ORDER BY r.created_at DESC;
```

### User Audit Trail

```sql
-- Get audit logs for a specific user
SELECT * FROM audit_logs 
WHERE user_id = 1 
ORDER BY created_at DESC;
```

### Request Correlation

```sql
-- Get all audit logs for a specific request
SELECT * FROM audit_logs 
WHERE request_context_id = 'req-12345'
ORDER BY created_at ASC;
```

## 🔐 Security Notes

- **Never store plain text passwords** - always use hashed passwords
- **Use environment variables** for database connection strings
- **Grant minimum privileges** to application database users
- **Regular backups** are essential for production environments
- **Audit logs** should be write-only for application users
- **Video file paths** should be secured and not directly accessible via web

## 🧪 Testing

To test the schema with sample data, see the commented section at the end of `schema.sql`.

## 📚 Integration

The FastAPI backend uses **parameterized SQL** (psycopg2) for data access; Pydantic models in `src/backend/app/models/` align with this schema. Any schema change should be reflected in the backend layer and docs.

## 🔄 Schema / migration strategy (FastAPI)

- **Baseline:** This `schema.sql` is the single source of truth for the initial schema. Apply it via Docker Compose (automatic on first run) or manually with `psql -f schema.sql`.
- **Data access:** Backend uses raw SQL with parameterized queries (no ORM); connection string from `DATABASE_URL` env.
- **Future migrations:** For schema versioning and upgrades, consider **Alembic** (e.g. `alembic init` in backend, revision from this baseline). This file remains the reference for the initial state.

## 🤝 Contributing

When proposing schema changes:
1. Update `schema.sql`
2. Update backend data access and Pydantic models in `src/backend/app/` as needed
3. Document the change in this README and `docs/11_database_schema.md`
4. Test with PostgreSQL (and test fixtures where applicable)

## 📄 License

See the main repository [LICENSE](../../LICENSE) file.
