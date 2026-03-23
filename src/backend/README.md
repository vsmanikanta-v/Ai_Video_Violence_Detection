# AI Video Violence Detection - Backend

FastAPI backend for the AI Video Violence Detection N-Tier application. Fully implemented: health, OpenAPI docs, JWT-based auth (RBAC), video upload/analyze/history, detection retrieval, admin stats and audit logs, rate limiting (SlowAPI), ML inference (CNN-LSTM stub; real inference when `ML_MODEL_PATH` is set), and GenAI incident explanations via Google Gemini.

## 🎯 Endpoints Implemented

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | API metadata and links |
| GET | `/health` | Health check |
| GET | `/api/openapi.yaml` | OpenAPI 3.1 specification (YAML) |
| POST | `/api/auth/register` | Register new user (role: USER only) |
| POST | `/api/auth/login` | Login; returns JWT access token |
| GET | `/api/auth/me` | Current user (JWT protected) |
| GET | `/api/auth/admin-check` | Admin role check (ADMIN only) |
| POST | `/api/videos/upload` | Upload video file (rate limited) |
| POST | `/api/videos/{video_id}/analyze` | Run violence detection + GenAI explanation |
| GET | `/api/videos/history` | Current user's video history |
| GET | `/api/videos/{video_id}` | Video metadata and results |
| GET | `/api/detections/result/{result_id}` | Detection by result ID |
| GET | `/api/detections/video/{video_id}` | Detections for a video |
| GET | `/api/admin/stats` | Aggregate counts (ADMIN only) |
| GET | `/api/admin/audit-logs` | Audit log entries, paginated (ADMIN only) |

## 📁 Project Structure

```text
src/backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app entry point
│   ├── config.py                    # Configuration (pydantic-settings)
│   ├── db.py                        # Database connection (psycopg2)
│   ├── deps.py                      # Shared dependencies (require_admin)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── auth.py                  # User, auth request/response models
│   │   ├── health.py                # Health response models
│   │   └── video.py                 # Video, Result, history models
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                  # /api/auth/* endpoints
│   │   ├── health.py                # /health endpoint
│   │   ├── videos.py                # /api/videos/* endpoints
│   │   ├── detections.py            # /api/detections/* endpoints
│   │   └── admin.py                 # /api/admin/* endpoints (ADMIN only)
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py          # Authentication business logic
│   │   ├── video_service.py         # Video and result persistence
│   │   ├── admin_service.py         # Admin stats and audit log queries
│   │   ├── audit_service.py         # Audit log writes
│   │   └── explanation_service.py   # GenAI incident explanation (Gemini)
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── jwt_handler.py           # JWT token creation/validation
│   │   ├── password.py              # Password hashing (bcrypt $2b$12$)
│   │   ├── validators.py            # Email/password validation
│   │   ├── request_helpers.py       # Request ID extraction
│   │   └── audit_helpers.py         # Audit log wrapper
│   └── ml/
│       ├── __init__.py
│       ├── inference.py             # CNN-LSTM inference pipeline
│       ├── preprocessing.py         # Video frame extraction/normalization
│       └── train.py                 # Offline CNN-LSTM training script
├── data/
│   ├── violent/                     # Violent MP4 clips (training data)
│   └── non-violent/                 # Non-violent MP4 clips (training data)
├── models/
│   └── violence_model.keras         # Trained CNN-LSTM model
├── tests/
│   ├── __init__.py
│   ├── conftest.py                  # Pytest fixtures (tokens, mocks)
│   ├── helpers.py                   # Shared test utilities
│   ├── test_auth.py                 # Authentication endpoint tests
│   ├── test_admin_api.py            # Admin API (403/200) tests
│   ├── test_health.py               # Health endpoint tests
│   ├── test_main.py                 # Root and OpenAPI YAML tests
│   ├── test_videos_api.py           # Video upload/analyze/history tests
│   ├── test_detections_api.py       # Detection result endpoint tests
│   ├── test_explanation_service.py  # GenAI explanation service tests
│   ├── test_ml_inference.py         # ML inference pipeline tests
│   ├── test_ml_preprocessing.py     # Video preprocessing tests
│   ├── test_ratelimit.py            # Rate limiting (429) tests
│   └── test_utils_validators.py     # Email/password validator tests
├── uploads/                         # Uploaded video storage (runtime)
└── .env.example                     # Environment variables template
```

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
# Navigate to project root
cd D:\SrivariHSSPL-2026\ai-video-violence-detection

# Install all dependencies (production + dev)
uv sync --all-extras --link-mode=copy
```

### 2. Configure Environment

See [Environment Configuration](#-environment-configuration) below. Quick step:

```powershell
cd src\backend
Copy-Item .env.example .env
# Edit .env: set JWT_SECRET_KEY, DATABASE_URL, and optionally GEMINI_API_KEY
notepad .env
```

### 3. Start Server

```powershell
# From src/backend directory
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API Root**: <http://localhost:8000/>
- **Health Check**: <http://localhost:8000/health>
- **Swagger UI**: <http://localhost:8000/api/docs>
- **ReDoc**: <http://localhost:8000/redoc>
- **OpenAPI YAML**: <http://localhost:8000/api/openapi.yaml>

## 🔧 Environment Configuration

This project uses two `.env.example` files for different setup scenarios. Copy the relevant example to `.env` and fill in values; never commit `.env` (it is in `.gitignore`).

### 1. infra/.env.example (for Docker Compose)

| Location             | Purpose                                            | When to use                                                                 |
| -------------------- | -------------------------------------------------- | --------------------------------------------------------------------------- |
| `infra/.env.example` | PostgreSQL container credentials for Docker Compose | When you run the database with `docker compose up -d` from the `infra/` directory |

**Setup:**

```powershell
# From repo root
Copy-Item infra\.env.example infra\.env
# Optional: edit infra/.env to set POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
```

**Variables:**

- `POSTGRES_USER` — Database username (default: postgres)
- `POSTGRES_PASSWORD` — Database password (default: postgres)
- `POSTGRES_DB` — Database name (default: ai_video_violence)

The backend connects to this database using `DATABASE_URL` in **backend** `.env` (see below). Keep credentials in sync: if you change `infra/.env`, set the same user/password in `src/backend/.env` in the connection string.

### 2. src/backend/.env.example (for Backend / Direct Execution)

| Location                  | Purpose                                              | When to use                                                                        |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------------------------- |
| `src/backend/.env.example` | FastAPI app, JWT, database connection, GenAI (Gemini) | When you run the backend (e.g. `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`) |

**Setup:**

```powershell
cd src\backend
Copy-Item .env.example .env
# Edit .env: set JWT_SECRET_KEY (required), DATABASE_URL, and optionally GEMINI_API_KEY
```

**Variables (see also `app/config.py`):**

| Variable                          | Required | Description                                                       |
| --------------------------------- | -------- | ----------------------------------------------------------------- |
| `JWT_SECRET_KEY`                  | Yes      | Secret for JWT token signing; use a long random string in production |
| `JWT_ALGORITHM`                   | No       | Default: HS256                                                    |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | No       | Default: 30                                                        |
| `DATABASE_URL`                   | Yes      | PostgreSQL connection string, e.g. `postgresql://...@localhost:5432/ai_video_violence` |
| `CREATE_DEFAULT_USERS`          | No       | If true, create default admin/user on startup (dev only); default: false |
| `DEFAULT_ADMIN_*` / `DEFAULT_USER_*` | No  | Used when CREATE_DEFAULT_USERS is true                            |
| `GEMINI_API_KEY`                | No       | Gemini API key for incident explanations; omit for mock mode      |
| `GEMINI_MODEL`                  | No       | Model name (default `gemini-3-flash-preview`)                     |
| `UPLOAD_DIR`                    | No       | Directory for uploaded videos; default: uploads                   |
| `MAX_UPLOAD_SIZE_MB`            | No       | Max upload size in MB; default: 10                                |
| `RATELIMIT_ENABLED`             | No       | Enable rate limiting; default: true (set false in tests)           |
| `RATELIMIT_DEFAULT`             | No       | Global limit per IP; default: 50 per hour                          |
| `RATELIMIT_VIDEO_UPLOAD`        | No       | Limit for upload endpoint; default: 5 per minute                 |
| `RATELIMIT_VIDEO_ANALYSIS`      | No       | Limit for analyze endpoint; default: 10 per minute                 |

### Quick setup by scenario

#### Scenario 1: Docker Compose for database (recommended)

1. Copy `infra/.env.example` to `infra/.env` (optional; defaults work).
2. From `infra/`, run `docker compose up -d`.
3. Copy `src/backend/.env.example` to `src/backend/.env`.
4. Set `DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_video_violence` (or match `infra/.env` if you changed it).
5. Set `JWT_SECRET_KEY` to a random secret; optionally set `GEMINI_API_KEY`.
6. Run the backend from `src/backend/`.

#### Scenario 2: Local PostgreSQL (no Docker)

1. Create database `ai_video_violence` and apply `infra/database/schema.sql`.
2. Copy `src/backend/.env.example` to `src/backend/.env`.
3. Set `DATABASE_URL` to your local connection string (user, password, host, port, db name).
4. Set `JWT_SECRET_KEY` and optionally `GEMINI_API_KEY`.

### Security notes

- Do not commit `.env` files; they are listed in `.gitignore`.
- Generate a strong `JWT_SECRET_KEY` for production (e.g. `python -c "import secrets; print(secrets.token_urlsafe(32))"`).
- Keep `GEMINI_API_KEY` and database credentials confidential.
- Use different secrets for development and production.

## 🧪 Testing

Install dependencies from repo root (`uv sync --extra dev`), then run tests (`uv run pytest tests/` from this directory or `uv run pytest src/backend/tests/` from repo root):

```powershell
# From src/backend
uv run pytest tests/ -v
```

With coverage:

```powershell
uv run pytest tests/ --cov=app --cov-report=term-missing -v
```

**Tip:** Run backend tests (and frontend tests) after every phase to stay on track. See the root [README Testing section](../../README.md#testing).

## 🔍 Code Quality

All code passes linting and formatting checks:

```powershell
# Format code with black
black app/ tests/

# Sort imports with isort
isort app/ tests/

# Check code style with flake8
flake8 app/ tests/ --max-line-length=120 --extend-ignore=E203,W503
```

## 📝 API Documentation

### Root Endpoint

```powershell
# Using Invoke-RestMethod (recommended for PowerShell)
Invoke-RestMethod -Uri "http://localhost:8000/" | ConvertTo-Json

# Or using curl (if installed)
curl http://localhost:8000/
```

Response:

```json
{
  "status": "ok",
  "message": "AI Video Violence Detection API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "openapi": "/api/openapi.yaml",
    "swagger": "/api/docs",
    "redoc": "/redoc"
  }
}
```

### Health Check

```powershell
# Using Invoke-RestMethod
Invoke-RestMethod -Uri "http://localhost:8000/health" | ConvertTo-Json

# Or using curl
curl http://localhost:8000/health
```

Response:

```json
{
  "status": "healthy",
  "message": "All systems operational",
  "timestamp": "2026-02-12T18:10:59.488115"
}
```

### User Registration

```powershell
# Using Invoke-RestMethod (recommended)
$body = @{
    username = "john_doe"
    email = "john.doe@company.com"
    password = "SecurePass123!"
    role = "USER"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/register" `
  -Method Post `
  -Body $body `
  -ContentType "application/json" | ConvertTo-Json

# Or using curl
curl -X POST http://localhost:8000/api/auth/register `
  -H "Content-Type: application/json" `
  -d '{"username":"john_doe","email":"john.doe@company.com","password":"SecurePass123!","role":"USER"}'
```

Response (201 Created):

```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john.doe@company.com",
    "role": "USER",
    "created_at": "2026-02-12T10:00:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### User Login

```powershell
# Using Invoke-RestMethod
$loginBody = @{
    username = "john_doe"
    password = "SecurePass123!"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login" `
  -Method Post `
  -Body $loginBody `
  -ContentType "application/json"

# Save the token for later use
$token = $response.access_token
$response | ConvertTo-Json

# Or using curl
curl -X POST http://localhost:8000/api/auth/login `
  -H "Content-Type: application/json" `
  -d '{"username":"john_doe","password":"SecurePass123!"}'
```

Response (200 OK):

```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john.doe@company.com",
    "role": "USER",
    "created_at": "2026-02-12T10:00:00Z"
  },
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Get Current User

```powershell
# Using Invoke-RestMethod (use $token from login)
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/me" `
  -Headers $headers | ConvertTo-Json

# Or using curl
curl http://localhost:8000/api/auth/me `
  -H "Authorization: Bearer <YOUR_JWT_TOKEN>"
```

Response (200 OK):

```json
{
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john.doe@company.com",
    "role": "USER",
    "created_at": "2026-02-12T10:00:00Z"
  }
}
```

## 🔒 Security Features

- ✅ Passwords hashed with bcrypt (12 rounds)
- ✅ JWT tokens signed with secret from environment variable
- ✅ Protected endpoints validate JWT tokens
- ✅ No secrets hardcoded in code
- ✅ Input validation with Pydantic
- ✅ CORS middleware configured for frontend integration

## 🔧 Technology Stack

- **Python**: 3.12+
- **FastAPI**: 0.110.0
- **Pydantic**: 2.6.1
- **python-jose**: 3.3.0 (JWT)
- **passlib**: removed; passwords now hashed with **bcrypt** directly (12 rounds, `$2b$`)
- **psycopg2-binary**: 2.9.10 (PostgreSQL driver)
- **PyYAML**: 6.0.2 (OpenAPI YAML export)

## 📚 Environment Variables

Required environment variables (see `.env.example`):

- `JWT_SECRET_KEY` - Secret key for JWT token signing (REQUIRED)
- `JWT_ALGORITHM` - Algorithm for JWT encoding (default: HS256)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` - Token expiration in minutes (default: 30)
- `DATABASE_URL` - PostgreSQL connection string (REQUIRED)
- `ML_MODEL_PATH` - Optional path to CNN-LSTM Keras model file; if unset or file missing, stub inference is used
- `INFERENCE_BATCH_SIZE` - Batch size for model.predict (default: 16)
- `FRAME_EXTRACT_FPS` - FPS for frame extraction from video (default: 2.0)
- `MODEL_INPUT_SIZE` - Height/width for normalized frames (default: 64)
- `MAX_FRAMES` - Maximum frames to extract per video (default: 32)

### GenAI incident explanation

Detection results include a human-readable **incident explanation** (`genai_summary`) generated from the ML outcome (score, confidence, timestamps). The explanation is **persisted** in `results.genai_summary` and returned in:

- `POST /api/videos/{video_id}/analyze` (response.result.genai_summary)
- `GET /api/detections/result/{result_id}` and `GET /api/detections/video/{video_id}`

**Fallback behaviour:** If `GEMINI_API_KEY` is unset or the GenAI API fails (timeout, error), the service returns a safe, user-friendly message (e.g. mock explanation or "Explanation could not be generated...") and **never raises**. The detection flow (ML result + DB persist) always completes; only the explanation text varies. Access control is unchanged: explanations are only returned for results whose video belongs to the current user.

## 🎯 Success Criteria Met

- ✅ All 15 endpoints implemented and tested (68 pytest tests pass)
- ✅ OpenAPI 3.1 specification at `/api/openapi.yaml`
- ✅ Interactive Swagger UI at `/api/docs`
- ✅ JWT authentication and RBAC working
- ✅ Zero linting errors (black, isort, flake8)
- ✅ Comprehensive Pydantic validation
- ✅ Production-ready error handling
- ✅ Rate limiting (SlowAPI) on upload and analyze endpoints
- ✅ ML inference pipeline (CNN-LSTM; stub or real via `ML_MODEL_PATH`)
- ✅ GenAI incident explanations (Gemini; mock fallback when key absent)

## 📄 License

MIT License - See LICENSE file for details
