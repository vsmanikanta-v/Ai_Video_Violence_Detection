# Setup Guide: AI Video Violence Detection System

**Project:** AI Video Violence Detection System  
**Purpose:** Complete installation and configuration guide  
**For Usage Instructions:** See [Usage Guide](04_usage.md)

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installation](#installation)
3. [Database Setup](#database-setup)
4. [Configuration](#configuration)
5. [ML Model Training](#ml-model-training)
6. [Running the Application](#running-the-application)
7. [Troubleshooting](#troubleshooting)
8. [Testing](#testing)

---

## Prerequisites

Before setting up the system, ensure you have the following installed:

- **Python 3.12+** for backend (pinned via `.python-version`)
- **Node.js 20+** for frontend
- **PostgreSQL 16** - Choose one:
  - Docker & Docker Compose (recommended for development)
  - Local PostgreSQL installation
- **CPU-only machine** (no GPU required - inference-only execution)
- **Google Gemini API key** (for incident explanation generation; optional for dev with mock)
- **TensorFlow** and **OpenCV** (for ML inference)

---

## Installation

### Backend Setup

**Virtual environment location:** The Python virtual environment (`.venv`) is at the **repository root**. Run `uv sync` from the repo root to create or update it. Do not create a venv inside `src/backend`.

You have two options for setting up the Python backend:

#### Option 1: Using `uv` (Recommended - Faster)

Dependencies are in `pyproject.toml` at the repo root. Use `uv sync` from the repository root:

```powershell
# Install uv first (one-time setup)
# Windows (PowerShell):
irm https://astral.sh/uv/install.ps1 | iex
# Linux/macOS:
curl -LsSf https://astral.sh/uv/install.sh | sh

# From repository root: install all dependencies (runtime + dev tools)
uv sync --extra dev

# Activate virtual environment (created at .venv in repo root)
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Windows CMD:
.venv\Scripts\activate
# Linux/Mac:
source .venv/bin/activate
```

#### Option 2: Using pip (fallback)

If you cannot use `uv`, create a venv at repo root and install from an exported lockfile (e.g. `uv pip compile pyproject.toml -o requirements.txt` then `pip install -r requirements.txt`). **Recommended:** use Option 1 (`uv sync --extra dev`) so `pyproject.toml` is the single source of truth.

**Key Dependencies:**

- FastAPI, Pydantic, python-jose (JWT)
- TensorFlow (for CNN-LSTM inference)
- OpenCV (for video processing)
- NumPy, Pillow (for image processing)
- Google Gemini SDK (`google-genai`) for incident explanations

### Frontend Setup

```powershell
# Navigate to frontend directory
cd src/frontend

# Install dependencies
npm install

# Verify installation
npm run build
```

---

## Database Setup

You have two options for setting up PostgreSQL:

### Option 1: Using Docker Compose (Recommended)

Docker Compose provides a consistent local development environment. The schema (`infra/database/schema.sql`) is applied automatically when the database is created (mounted as init script).

```powershell
# 1. Copy the environment file (optional; defaults work)
# From repo root:
cp infra/.env.example infra/.env
# (Optional) Edit infra/.env to customize: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)

# 2. Navigate to infra directory
cd infra

# 3. Start PostgreSQL service (schema runs on first start)
docker compose up -d

# 4. Check service health
docker compose ps

# 5. View logs (optional)
docker compose logs postgres
```

#### Managing the Docker Compose Environment

```powershell
# Navigate to infra directory
cd infra

# Stop services
docker compose down

# Stop and remove data (WARNING: destroys all data)
docker compose down -v

# View service status
docker compose ps

# Access PostgreSQL CLI (optional)
docker compose exec postgres psql -U postgres -d ai_video_violence
```

#### Connect Backend to Docker Compose PostgreSQL

Set `DATABASE_URL` in `src/backend/.env` to match the container credentials (see `infra/.env.example` for Docker Compose variables):

```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/ai_video_violence
```

Use the same username/password as in `infra/.env` if you customized them. Data persists in the `postgres_data` volume across `docker compose down` and `up`.

**Reference:** Port mapping is **5432:5432** (host:container). Volume name: **postgres_data**. Commands: `docker compose up -d` (start), `docker compose ps` (health), `docker compose down` (stop; use `down -v` to remove the volume and data).

### Option 2: Using Local PostgreSQL Installation

If you prefer a local PostgreSQL installation:

```sql
-- Create database
CREATE DATABASE ai_video_violence;

-- Run schema migration
psql -U postgres -d ai_video_violence -f infra/database/schema.sql
```

---

## Configuration

The backend is FastAPI; the authoritative list of environment variables is in the [Backend README — Environment Configuration](../src/backend/README.md#-environment-configuration).

### Backend Configuration

Copy the backend environment template and set required values:

```powershell
cd src\backend
Copy-Item .env.example .env
# Edit .env: set JWT_SECRET_KEY (required), DATABASE_URL, and optionally GEMINI_API_KEY
```

**Required:** `JWT_SECRET_KEY`, `DATABASE_URL`. **Optional:** `GEMINI_API_KEY` (Gemini for incident explanations; omit for mock), default users and upload settings.

For the full variable list and the two `.env.example` files (Docker Compose vs backend), see [Backend README — Environment Configuration](../src/backend/README.md#-environment-configuration).

### Frontend Configuration

Optional: create a `.env` in `src/frontend/` if you need to override the API base URL (e.g. for production). In development, the Vite proxy uses relative paths; `VITE_API_URL` can be left unset or set to the backend URL (e.g. `http://localhost:8000`).

---

## ML Model Training

The backend supports two modes:

| Mode | When | Result |
|:-----|:-----|:-------|
| **Stub** | `ML_MODEL_PATH` unset or file missing | Always returns `NON_VIOLENT / 0.0 / LOW` — safe for dev and CI |
| **Real inference** | `ML_MODEL_PATH` points to a valid `.keras` file | CNN-LSTM model scores each video |

Training is an **offline step** — the running application never trains; it only loads an already-saved model.

### Step 1 — Prepare training data

Create two directories and populate them with labeled short video clips (`.mp4`, `.avi`, `.mov`):

```
src/backend/data/
  violent/          ← violent video clips (minimum 3 recommended)
  non-violent/      ← non-violent video clips (minimum 3 recommended)
```

> Both directories are in `.gitignore` — video files will not be committed.

### Step 2 — Run the training script

From the repository root:

```powershell
uv run python src/backend/app/ml/train.py `
  --violent-dir     src/backend/data/violent `
  --non-violent-dir src/backend/data/non-violent `
  --output          src/backend/models/violence_model.keras `
  --epochs          50
```

**Options:**

| Argument | Default | Description |
|:---------|:--------|:------------|
| `--violent-dir` | required | Directory of violent video clips |
| `--non-violent-dir` | required | Directory of non-violent video clips |
| `--output` | `src/backend/models/violence_model.keras` | Output `.keras` model path |
| `--epochs` | `20` | Training epochs — use `50` for small datasets (< 10 videos) |
| `--frames` | `16` | Frames sampled per video during training |
| `--img-size` | `64` | Frame height/width in pixels |

**Expected output:**

```
============================================================
CNN-LSTM Violence Detection — Training
============================================================
  Frames per video : 16
  Frame size       : 64x64
  Epochs           : 50

Step 1/3 — Loading dataset...
  VIOLENT: found 3 video(s)
    [ok] violent_1.mp4
    [ok] violent_2.mp4
    [ok] violent_3.mp4
  NON_VIOLENT: found 3 video(s)
    [ok] non-violent_1.mp4
    ...

Step 2/3 — Building model...
Step 3/3 — Training (50 epochs, batch=4, val_split=0.0, class_weights=...)...
Epoch 1/50 ...
...
Training complete in 30.2s

Model saved: D:\...\src\backend\models\violence_model.keras

Next steps:
  1. Add to src/backend/.env:
       ML_MODEL_PATH=models/violence_model.keras
  2. Restart the backend — inference will use the real model.
```

**Training time (CPU):** ~5–30 minutes depending on number of videos and epochs.

### Step 3 — Set ML_MODEL_PATH in .env

Add the following line to `src/backend/.env`:

```env
ML_MODEL_PATH=models/violence_model.keras
```

> The path is relative to `src/backend/` — matching where uvicorn runs from.

### Step 4 — Restart the backend

Stop and fully restart the backend (hot reload does **not** pick up `.env` changes):

```powershell
# Ctrl+C to stop, then:
cd src/backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Step 5 — Verify real inference is active

Upload and analyze a video in the UI. Confirm:

| Signal | Stub (not loaded) | Real model (loaded) |
|:-------|:-----------------|:--------------------|
| Processing time | `0.10s` | `0.5s – 3s` |
| Violence score | Always `0.0` | Varies per video |
| Prediction | Always `NON_VIOLENT` | `VIOLENT` or `NON_VIOLENT` |

### Model architecture

```
Input:  (None, 64, 64, 3)         — variable frame sequence, RGB float32 [0,1]
TimeDistributed Conv2D(16, 3×3)   — per-frame spatial features
TimeDistributed MaxPool2D(2×2)
TimeDistributed Conv2D(32, 3×3)
TimeDistributed MaxPool2D(2×2)
TimeDistributed GlobalAveragePooling2D  → (None, T, 32)
LSTM(64, dropout=0.3)             — temporal pattern across frames
Dense(1, sigmoid)                 → violence probability [0, 1]
```

The `None` time dimension means the model accepts any number of frames — training with 16 frames and inferring with 32 (from `MAX_FRAMES` in config) both work correctly.

### Notes

- **Small datasets (< 10 videos):** Training automatically disables the validation split and applies class weights to ensure both classes are learned equally. Accuracy on training data should reach 1.0 by epoch 30–50.
- **Larger datasets:** For production-quality models, consider the RWF-2000 or RLVS public datasets (~200–2000 labeled clips per class). Retrain with the same script — no code changes needed.
- **The trained model is gitignored** (`src/backend/models/` is in `.gitignore`). Store `.keras` files in artifact storage for team sharing.

---

## Running the Application

### Start Backend Server

```powershell
# Navigate to backend directory
cd src/backend

# Start FastAPI server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run on `http://localhost:8000`

### Start Frontend Development Server

```powershell
# Navigate to frontend directory
cd src/frontend

# Start Vite development server
npm run dev
```

Frontend will run on `http://localhost:5173` (or similar port - check console output)

### Access the Application

1. Open your browser and navigate to the frontend URL (e.g., `http://localhost:5173`)
2. You should see the **landing page** (hero, features, tech stack)
3. Use **Log in** or **Register** in the header to authenticate
4. After signing in, use **Upload** to submit a video for violence detection analysis

---

## Troubleshooting

### Docker Compose and PostgreSQL container

**Port 5432 already in use**

- Another PostgreSQL (or service) is using port 5432. Options:
  - Stop the other service, or
  - Change the host port in `infra/docker-compose.yml` (e.g. `"5433:5432"`) and use `DATABASE_URL=postgresql://postgres:postgres@localhost:5433/ai_video_violence` in the backend.

**Docker daemon not running**

- Start Docker Desktop (or the Docker service) and wait until it is ready. Then run `docker compose up -d` again from the `infra/` directory.

**Permission or access errors (Windows)**

- Run your terminal as Administrator if you see permission errors.
- Ensure the `infra/` path has no special characters or very long paths that can cause volume mount issues.
- If the container exits immediately, run `docker compose logs postgres` from `infra/` to see the error.

### Issue: Backend Won't Start

**Symptoms:** Error when running `uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

**Solutions:**

1. **Check virtual environment is activated:**

   ```powershell
   .venv\Scripts\Activate.ps1
   ```

2. **Verify database connection:**
   - If using Docker Compose: Run `docker compose ps` (from infra/ directory)
   - If using local PostgreSQL: Ensure PostgreSQL service is running
   - Check `DATABASE_URL` in `src/backend/.env` file
   - Verify database exists: `psql -U postgres -d ai_video_violence`

3. **Check ML model path:**
   - Ensure `ML_MODEL_PATH` points to a valid offline-trained model file (e.g. `src/backend/models/violence_model.keras`)
   - Verify model file exists and is accessible

4. **Check API key:**
   - Ensure `GEMINI_API_KEY` is set in `.env` if using live GenAI
   - Verify the key is valid and active

5. **Check dependencies:**
   ```powershell
   uv sync --extra dev
   ```

### Issue: Frontend Can't Connect to Backend

**Symptoms:** API calls failing, CORS errors, network errors

**Solutions:**

1. **Verify backend is running** on `http://localhost:8000`
2. **Check `VITE_API_URL`** in frontend `.env`
3. **Verify CORS is enabled** in FastAPI backend
4. **Check firewall settings** that might block localhost connections

### Issue: Video Upload Fails

**Symptoms:** Video upload errors, file size errors

**Solutions:**

1. **Check file size limits** in backend configuration
2. **Verify video format** is supported (MP4, AVI, MOV)
3. **Check video duration** is within limits (typically 30-60 seconds)
4. **Verify file permissions** for upload directory

### Issue: ML Inference Errors

**Symptoms:** Detection fails, model loading errors

**Solutions:**

1. **Verify model path** is correct in `.env`
2. **Check model file** exists and is valid
3. **Verify TensorFlow installation:**
   ```powershell
   uv run python -c "import tensorflow as tf; print(tf.__version__)"
   ```
4. **Check OpenCV installation:**
   ```powershell
   uv run python -c "import cv2; print(cv2.__version__)"
   ```

### Issue: GenAI Explanation Generation Fails

**Symptoms:** Incident explanations not generated, API errors

**Solutions:**

1. **Verify `GEMINI_API_KEY`** is correct and active (if using Gemini for explanations)
2. **Check API quota/limits** in GenAI provider console
3. **Review error messages** in backend logs
4. **Ensure internet connection** is stable

---

## Testing

### Backend Testing

**Run backend tests:**

```powershell
# Navigate to backend directory
cd src/backend

# Run all tests
uv run pytest tests/

# Run with verbose output
uv run pytest -v tests/

# Run specific test file
uv run pytest tests/test_videos_api.py
```

**Run with coverage:**

```powershell
# Generate coverage report
uv run pytest --cov=app --cov-report=html tests/

# View HTML coverage report
# Open htmlcov/index.html in your browser
```

**Available Test Files:**

- `test_auth.py` - Authentication endpoint tests
- `test_videos_api.py` - Video upload and management tests
- `test_detections_api.py` - Detection endpoint tests
- `test_ml_inference.py` - ML inference tests
- `test_ml_preprocessing.py` - ML preprocessing tests
- `test_admin_api.py` - Admin endpoint tests
- `test_health.py` - Health endpoint tests

**Before pushing to `main` (or your CI branch):** Run the full backend test suite from `src/backend` so CI passes:

```powershell
cd src/backend
uv run pytest tests/ --cov=app -v
```

### Frontend Testing

**Run frontend tests:**

```powershell
# Navigate to frontend directory
cd src/frontend

# Run tests
npm test

# Run with coverage
npm test -- --coverage

# Run in watch mode
npm test -- --watch
```

### Integration Testing

Test the full stack:

1. Start Docker Compose PostgreSQL (if using)
2. Start backend server
3. Start frontend dev server
4. Run end-to-end tests (if configured)

**Manual Integration Test:**

1. Navigate to frontend URL (landing page)
2. Register a new user (or use Log in if already registered)
3. Sign in with credentials
4. Upload a test video
5. Wait for detection results
6. View incident explanation
7. Test admin features (if admin user)

---

## Repository checks (optional)

- **Zero-copy:** All code and docs must be original and project-specific. Optional: run `.\tools\psscripts\Verify-ZeroCopy.ps1 -AllowMissingSourceMaterial` from repo root.

---

## Next Steps

Once setup is complete:

1. **Read the [Usage Guide](04_usage.md)** to learn how to use the application
2. **Review [Technical Documentation](05_technical.md)** for implementation details
3. **Check [Architecture Plan](06_architecture_plan.md)** for system architecture
4. **Explore the codebase** in `src/backend/` and `src/frontend/`

---

## Additional Resources

- [Main README](../README.md) - Project overview
- [Requirements Specification](02_requirements.md) - System requirements
- [Usage Guide](04_usage.md) - How to use the application
- [Technical Documentation](05_technical.md) - Technical details
- [Repository Structure](08_repository_structure.md) - Complete structure guide
- [Database Schema](11_database_schema.md) - Database documentation

---

**Document Version:** 1.1
**Last Updated:** March 21, 2026
**Status:** Complete
