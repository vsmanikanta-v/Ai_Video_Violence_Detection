# AI Video Violence Detection System - Final Review Presentation

**Last reviewed:** March 31, 2026 — Aligned to the same review standard as `consumer-complaints-ml-genai-ntier/docs/reviews/31mar2026_FinalReview.md` (agenda, demo walkthrough, setup, tests, flows). Stack: FastAPI, React 19.2, PostgreSQL, CNN+LSTM inference, Google Gemini (`google.genai`) for explanations.

---

## Slide 1: Title Slide

**Title:** AI Video Violence Detection System  
**Subtitle:** Deep Learning-Based Violence Detection with GenAI Incident Explanations (N-Tier Architecture)

**Presented by:** Jyothi, Rishika, Sumasri and Vishnu  
**Date:** March 31, 2026

---

## Slide 2: Agenda

- Problem Statement
- Proposed Solution
- Key Features
- Technology Stack
- System Architecture
- Database Schema / ER Diagram
- Authentication Flow Diagram
- API (Swagger) Overview
- Environment Setup
- Podman & Containers
- PostgreSQL & VS Code Extension
- ML Model Training
- Backend Execution & Swagger UI
- Backend Unit Tests
- Frontend Execution & Landing Page
- Frontend Unit Tests
- User Flow
- Admin Flow
- Mock Mode (GenAI Optional)
- ML Pipeline & Workflow
- Explainable AI Integration
- Real-World Applications
- Expected Outcomes & Benefits
- Conclusion & Future Scope

---

## Slide 3: Problem Statement

**The Challenge in Video Surveillance & Review Workflows**

- **Manual monitoring limits:** Operators cannot continuously review many short clips; delayed detection and inconsistent review.
- **Alert fatigue:** Large volumes of footage make it hard to focus on high-risk segments.
- **Lack of explainability:** Raw scores or binary alerts lack context for trust and next steps.
- **Security & governance:** Video and findings need **JWT + RBAC**, audit trails, and controlled access—not ad hoc scripts.
- **Resource constraints:** Many DL demos assume **GPU**; this project targets **CPU-friendly inference** for academic and constrained environments.

---

## Slide 4: Proposed Solution

**Hybrid Deep Learning + GenAI with Enterprise N-Tier Design**

- **Spatial–temporal ML:** CNN + LSTM (or equivalent sequence model) for frame features and temporal patterns; **inference-only** in the app (training is offline).
- **GenAI incident explanations:** **Google Gemini** (`google.genai`) turns structured detection outputs (score, label, confidence, timestamps) into readable summaries—**not** raw video sent to the LLM.
- **N-Tier architecture:** Presentation (React) → Application (FastAPI) → ML preprocessing/inference → GenAI service module → PostgreSQL.
- **RBAC:** **USER** (upload, own history); **ADMIN** (stats, audit logs).
- **Traceability:** Videos, detection results, and audit events persisted for compliance-style review.

**How this differs from typical demos (summary)**

| Aspect | Typical demo | This project |
|:-------|:-------------|:-------------|
| Architecture | Script / notebook | N-Tier API + SPA |
| Explainability | Score only | GenAI narrative after detection |
| Hardware | GPU-assumed | CPU-oriented inference path |
| Security | Minimal | JWT, RBAC, audit logging |
| Processing | Live stream (often) | **Short pre-recorded clips** (project scope) |

---

## Slide 5: Key Features

- **Violence detection engine:** CNN–LSTM-style pipeline; outputs violence score, **VIOLENT / NON_VIOLENT**, and confidence tier (**HIGH / MEDIUM / LOW**).
- **Confidence & explainability:** Structured result + **Gemini**-generated incident summary (or **mock** text if no API key).
- **Video lifecycle:** Upload → analyze → history; metadata and file paths stored under configurable `UPLOAD_DIR`.
- **Admin visibility:** Aggregate stats and **paginated audit logs** (admin-only).
- **Secure authentication:** JWT access tokens; passwords hashed with **bcrypt** (12 rounds, `$2b$`). **No refresh-token flow** in this codebase—re-login after expiry.
- **Rate limiting:** Upload and analyze routes limited per IP (SlowAPI / limits configuration).
- **OpenAPI:** Swagger UI `/api/docs`, ReDoc `/redoc`, OpenAPI JSON `/openapi.json`, YAML `/api/openapi.yaml`.

---

## Slide 6: Technology Stack

| Layer | Technology |
|:------|:-----------|
| **Frontend** | React 19.2 (TypeScript), Vite, Tailwind CSS, Redux Toolkit |
| **Backend / API** | Python 3.12+, FastAPI, Pydantic Settings |
| **ML / Vision** | TensorFlow / Keras (inference), OpenCV (frames), NumPy |
| **Generative AI** | **Google Gemini** via **`google.genai`** (`GEMINI_API_KEY`; mock if unset) |
| **Database** | PostgreSQL 16 (see `infra/docker-compose.yml`) |
| **Data access** | psycopg2, parameterized SQL in services |
| **Security** | JWT (HS256), bcrypt (12 rounds), RBAC |
| **DevOps** | Docker Compose / Podman for DB, GitHub Actions (Python + frontend + docs) |

---

## Slide 7: System Architecture

**Five-layer N-Tier view**

1. **Presentation:** React SPA — landing, auth, upload, analysis, history, admin.
2. **Application:** FastAPI — routers (`auth`, `videos`, `detections`, `admin`, `health`), validation, orchestration.
3. **ML processing:** OpenCV preprocessing → Keras **`.keras`** model when `ML_MODEL_PATH` is set → otherwise **stub** inference path (safe defaults for dev).
4. **GenAI module:** `explanation_service.py` — builds prompts from detection DTOs; calls Gemini or returns mock explanation.
5. **Data:** PostgreSQL — users, videos, results, audit_logs.

![System Architecture](../diagrams/system-architecture.png)

*See:* `docs/diagrams/system-architecture.png`

---

## Slide 8: Database Schema / ER Diagram

**Core entities**

- **users:** `id`, `username`, `email`, `password_hash`, `role` (USER \| ADMIN), `created_at`.
- **videos:** `id`, `user_id` (FK), `file_path`, `filename`, `file_size`, `duration_seconds`, `video_format`, `uploaded_at`.
- **results:** `id`, `video_id` (FK), `violence_score`, `prediction`, `confidence_level`, `key_frame_timestamps`, `processing_time_seconds`, `genai_summary`, `created_at`.
- **audit_logs:** `id`, `user_id`, `action`, `entity_type`, `entity_id`, `request_context_id`, `details`, `created_at`.

![Database ER Diagram](../diagrams/database-erd.png)

*See:* `docs/diagrams/database-erd.png` · *SQL schema:* `infra/database/schema.sql`

---

## Slide 9: Authentication Flow Diagram

**Auth & authorization (as implemented)**

- **Register / Login:** `POST /api/auth/register`, `POST /api/auth/login` — password hashing via **bcrypt** (12 rounds); JWT **access** token returned (expiry from `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`, default 30).
- **Current user:** `GET /api/auth/me` — Bearer JWT required.
- **RBAC:** Video and detection routes scoped to **resource owner**; admin routes require **ADMIN** role.
- **No `/api/auth/refresh`:** Clients obtain a new token by **logging in again** after expiry (differs from consumer-complaints stack).

![Authentication Flow](../diagrams/auth-authorization-flow.png)

*See:* `docs/diagrams/auth-authorization-flow.png`

---

## Slide 10: API (Swagger) Overview

**Representative endpoints** (full table: `docs/reference/api-surface.md`)

| Purpose | Method | Path (examples) |
|:--------|:-------|:----------------|
| Health | GET | `/health` |
| API root | GET | `/` |
| OpenAPI | GET | `/api/openapi.yaml`, `/openapi.json` |
| Swagger UI | GET | `/api/docs` |
| ReDoc | GET | `/redoc` |
| Auth | POST / GET | `/api/auth/register`, `/api/auth/login`, `/api/auth/me`, `/api/auth/admin-check` |
| Videos | POST / GET | `/api/videos/upload`, `/api/videos/{id}/analyze`, `/api/videos/history`, `/api/videos/{id}` |
| Detections | GET | `/api/detections/result/{result_id}`, `/api/detections/video/{video_id}` |
| Admin | GET | `/api/admin/stats`, `/api/admin/audit-logs` |

*Live docs:* `http://localhost:8000/api/docs` (when backend is running on port 8000)

---

## Slide 11: Environment Setup

**Prerequisites:** Python 3.12+, Node.js 20+, `uv`, PostgreSQL (local or container), optional Gemini API key.

**Step 1 — Backend `.env`** (`src/backend/.env` — copy from `src/backend/.env.example`):

```env
JWT_SECRET_KEY=change-me-in-production
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_video_violence
CREATE_DEFAULT_USERS=true
DEFAULT_ADMIN_USERNAME=admin
DEFAULT_ADMIN_PASSWORD=Admin@123
DEFAULT_USER_USERNAME=user
DEFAULT_USER_PASSWORD=User@123
GEMINI_API_KEY=
GEMINI_MODEL=gemini-3-flash-preview
UPLOAD_DIR=uploads
MAX_UPLOAD_SIZE_MB=2
# Optional: ML_MODEL_PATH=C:\path\to\model.keras
```

**Step 2 — Frontend `.env`** (`src/frontend/.env`, optional):

```env
# Dev often uses Vite proxy; set if calling API directly:
# VITE_API_URL=http://localhost:8000
```

**Step 3 — Infra `.env`** (`infra/.env` — copy from `infra/.env.example`):

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=ai_video_violence
```

*Canonical setup:* `docs/03_setup.md`

---

## Slide 12: Podman & Containers

**Start PostgreSQL** (from `infra/`):

```bash
cd infra
docker compose up -d
```

**Podman (alternative):**

```bash
cd infra
podman-compose up -d
```

**Verify:**

```bash
docker compose ps
# or: podman ps
```

**Stop:**

```bash
docker compose down
```

**Key facts**

- Image: **postgres:16-alpine**; container name: **`ai_video_violence_postgres`**
- Port: **5432** (host)
- Init script: `infra/database/schema.sql` mounted for first-time DB creation
- Volume: **`postgres_data`** (named volume `ai_video_violence_data`)

*(Screen print: terminal showing `docker compose up -d` and healthy postgres)*

---

## Slide 13: PostgreSQL & VS Code Extension

**Recommended extension:** PostgreSQL (e.g. **PostgreSQL** by Weijan Chen — ID `cweijan.vscode-postgresql-client2`)

**Connection**

| Field | Value |
|:------|:------|
| Host | `localhost` |
| Port | `5432` |
| Database | `ai_video_violence` |
| Username | `postgres` |
| Password | `postgres` (or your `infra/.env` values) |

**Tables to inspect**

- `users`, `videos`, `results`, `audit_logs`

*(Screen print: extension tree showing the four tables)*

---

## Slide 14: ML Model Training

**Important:** The **running application does not train** the CNN–LSTM. Training is an **offline** step (separate scripts, coursework, or lab environment). The backend **loads** a saved Keras model when configured.

**At runtime**

1. Set **`ML_MODEL_PATH`** in `src/backend/.env` to a **`.keras`** (or compatible) file produced by your training pipeline.
2. If unset or file missing, the service uses a **stub** inference path so APIs and UI still work for demos.

**Typical offline flow (conceptual)**

1. Curate labeled short videos / frames; define CNN + LSTM (or equivalent) in TensorFlow/Keras.
2. Train with your split and metrics; export **saved model**.
3. Place artifact on disk; point `ML_MODEL_PATH` at it; restart backend.

*Code reference:* `src/backend/app/ml/inference.py`, `preprocessing.py`

*(Screen print: optional — training notebook or `ML_MODEL_PATH` set in `.env`)*

---

## Slide 15: Backend Execution & Swagger UI

**From repository root**

```bash
uv sync --extra dev
cd src/backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Health check**

```bash
curl http://localhost:8000/health
```

**Swagger UI:** `http://localhost:8000/api/docs`

**Swagger highlights**

- Bearer auth — paste JWT from login to try protected routes
- Try `POST /api/auth/login`, then `POST /api/videos/upload` / `.../analyze` with a small test clip

*(Screen print: Swagger UI showing auth and video endpoints)*

---

## Slide 16: Backend Unit Tests

**Run tests** (`src/backend`):

```bash
cd src/backend
uv run pytest tests/ -v --cov=app --cov-report=term-missing
```

**Results summary (typical CI / local)**

| Metric | Value |
|:-------|:------|
| Tests collected | **68** |
| Framework | pytest |
| Focus areas | auth, videos, detections, admin, ML inference/preprocess stubs, explanation service, rate limits, validators |

**Representative test modules**

| File | Focus |
|:-----|:------|
| `test_auth.py` | Register, login, JWT, `/me` |
| `test_videos_api.py` | Upload, analyze, history |
| `test_detections_api.py` | Result retrieval |
| `test_explanation_service.py` | Gemini + mock explanation paths |
| `test_ml_inference.py` / `test_ml_preprocessing.py` | ML helpers |
| `test_admin_api.py` | Stats and audit logs |

*(Screen print: `pytest -v` showing 68 passed)*

---

## Slide 17: Frontend Execution & Landing Page

```bash
cd src/frontend
npm install
npm run dev
```

**URL:** `http://localhost:5173` (Vite default)

**Landing / app**

- Marketing / hero → **Register** / **Login**
- After login: **upload**, **analyze**, **history**, **admin** (role-based)

**Default demo users** (when `CREATE_DEFAULT_USERS=true` in backend `.env`)

| Role | Username | Password |
|:-----|:---------|:---------|
| USER | `user` | `User@123` |
| ADMIN | `admin` | `Admin@123` |

*(Screen print: landing page and login)*

---

## Slide 18: Frontend Unit Tests

```bash
cd src/frontend
npm test
```

**Results summary**

| Metric | Value |
|:-------|:------|
| Framework | Vitest + React Testing Library |
| Tests | **24** (`it(...)` across Vitest test files; run `npm test` to confirm) |
| Examples | `PrivateRoute`, `AdminRoute`, `ErrorBoundary`, Redux slices, API client |

```bash
npx tsc --noEmit
npm run lint
```

*(Screen print: Vitest output — all tests passed)*

---

## Slide 19: User Flow

**End-to-end USER journey**

1. **Open** `http://localhost:5173` → **Register** or **Login** (`user` / `User@123`).
2. **Upload** a short clip (within size / type rules).
3. **Analyze** — backend runs preprocessing + inference (+ GenAI summary); result stored.
4. **Review result** — violence score, label, confidence, explanation text, timestamps.
5. **History** — list own videos and past results.

*(Screen prints: Upload → Analyze → Result → History)*

---

## Slide 20: Admin Flow

**End-to-end ADMIN journey**

1. **Login** as `admin` / `Admin@123`.
2. **Admin dashboard** — aggregate **stats** (users, videos, results, audit volume).
3. **Audit logs** — paginated list of actions (minimal PII; usernames where relevant).
4. **RBAC** — USER JWT must **not** access admin APIs (expect **403**).

*(Screen prints: Admin stats → Audit log table)*

---

## Slide 21: Mock Mode (GenAI Optional)

**Full stack works without Gemini**

- Leave **`GEMINI_API_KEY`** empty in `src/backend/.env`.
- `explanation_service.py` returns a **safe mock** explanation string; detection and persistence still run.

**Benefit:** Demos and CI do not require a paid key; behavior of REST + UI + DB unchanged except LLM text quality.

*(Screen print: result page with mock explanation paragraph)*

---

## Slide 22: ML Pipeline & Workflow

**End-to-end video analysis path**

1. **Upload** — multipart upload; file stored under `UPLOAD_DIR`; row in `videos`.
2. **Preprocessing** — OpenCV frame extract (FPS / max frames from settings); resize (e.g. 64×64); normalize for model input.
3. **Inference** — Keras model predicts score / class; map to confidence tier; optional timing metrics.
4. **GenAI** — Structured prompt from scores + timestamps → Gemini (or mock).
5. **Persist** — `results` row + **audit_log** entry; JSON response to client.

---

## Slide 23: Explainable AI Integration

**Why it matters**

- Operators need **context**, not only a number.
- Supports trust, review, and incident documentation.

**How it works here**

- **Input to Gemini:** Violence score, **VIOLENT/NON_VIOLENT**, confidence tier, optional key-frame times — **not** raw pixels.
- **Output:** Short incident-style narrative for security / compliance-style review.
- **Prompting:** Project-specific templates in code (see `explanation_service.py`).

---

## Slide 24: Real-World Applications

- **Campus & education:** Review recorded clips for altercations; audit trail for processes.
- **Public venues & transit:** Post-event review of submitted footage (project scope: **short files**, not live CCTV).
- **Retail & corporate security:** Incident documentation and handoff.
- **Healthcare / corrections:** Workflow-dependent; always subject to policy and law — system is a **technical demo**, not certified surveillance.

---

## Slide 25: Expected Outcomes & Benefits

- **Faster triage** of short clips vs fully manual viewing.
- **Consistent structured output** (score + label + confidence + text).
- **Auditability** via DB and admin views.
- **Teaches N-Tier integration** of CV, API design, auth, and GenAI **post-processing**.
- **CPU-friendly** positioning for labs without GPU farms.

---

## Slide 26: Conclusion & Future Scope

**Conclusion**

- Delivers a **full-stack**, **JWT-secured** pipeline from upload to **CNN–LSTM-style** inference to **Gemini** explanations.
- **N-Tier** boundaries match professional practice; OpenAPI-first API.
- **Mock GenAI** enables inclusive demos.

**Future scope**

- **Live / streaming** ingest (RTSP, HLS) — out of current scope.
- **Finer-grained classes** (e.g. weapon vs shove) with retraining.
- **Edge deployment** (TensorFlow Lite, ONNX) for on-device inference.
- **Active learning** from analyst feedback.
- **Rich analytics** dashboards (trends, false-positive review queues).

---

## Appendix: Research & positioning (optional slide)

This project is **architecture- and engineering-driven** (N-Tier, secure API, explainability) rather than a single-paper reproduction. It combines ideas from **video understanding (CNN, LSTM, spatial–temporal models)**, **XAI / GenAI for operators**, and **enterprise-style** auth and persistence—integrated into one deployable teaching / demo system.
