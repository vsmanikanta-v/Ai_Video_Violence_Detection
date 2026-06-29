# Repository Structure

**Project:** AI Video Violence Detection System  


---

## Overview

This document provides a comprehensive overview of the repository structure for the AI Video Violence Detection System. The project follows an N-Tier architecture with clear separation between frontend, backend, database, ML processing, and documentation layers.

---

## Complete Directory Structure

```text
ai-video-violence-detection/
├── .github/                    # GitHub configuration
│   ├── workflows/              # CI workflows (automated testing)
│   ├── ISSUE_TEMPLATE/         # Issue templates
│   ├── prompts/                # Prompt engineering guides
│   ├── workitems/              # Phase work items
│   └── copilot-instructions.md # GitHub Copilot instructions
│
├── .cursor/                    # Cursor IDE configuration
│   └── rules/                  # Cursor rules (.mdc files)
│       ├── 01_educational-content-rules.mdc
│       ├── 02_repository-structure.mdc
│       ├── 03_quality-assurance.mdc
│       ├── 04_markdown-standards.mdc
│       ├── 05_primary-directives.mdc
│       ├── 06_cross-domain-integration.mdc
│       └── 07_file-naming-conventions.mdc
│
├── infra/                      # Infrastructure configuration
│   ├── database/               # Database schema and migrations
│   │   ├── README.md           # Database setup instructions
│   │   └── schema.sql          # PostgreSQL schema definition
│   ├── docker-compose.yml      # Docker Compose configuration for PostgreSQL
│   └── .env.example            # Docker Compose environment variables template
│
├── src/
│   ├── frontend/               # React.js (Presentation Layer)
│   │   ├── src/
│   │   │   ├── api/            # API client
│   │   │   │   └── client.ts   # TypeScript API client with JWT handling
│   │   │   ├── components/     # Reusable React components
│   │   │   │   ├── AdminRoute.tsx  # Admin route protection
│   │   │   │   ├── Layout.tsx      # Main layout component
│   │   │   │   ├── PrivateRoute.tsx # Private route protection
│   │   │   │   └── VideoUpload.tsx  # Video upload component
│   │   │   ├── pages/          # Page components
│   │   │   │   ├── AdminDashboard.tsx
│   │   │   │   ├── DetectionResults.tsx
│   │   │   │   ├── History.tsx
│   │   │   │   ├── Login.tsx
│   │   │   │   ├── Register.tsx
│   │   │   │   └── VideoAnalysis.tsx
│   │   │   ├── store/          # Redux state management
│   │   │   │   ├── authSlice.ts    # Authentication state
│   │   │   │   ├── videosSlice.ts   # Videos state
│   │   │   │   ├── hooks.ts        # Typed Redux hooks
│   │   │   │   └── index.ts        # Store configuration
│   │   │   ├── types/          # TypeScript type definitions
│   │   │   │   └── index.ts        # Shared types and interfaces
│   │   │   ├── App.tsx         # Main application component
│   │   │   ├── main.tsx        # Application entry point
│   │   │   └── index.css       # Global styles
│   │   ├── public/             # Static assets
│   │   ├── dist/               # Build output (generated)
│   │   ├── eslint.config.js    # ESLint configuration
│   │   ├── index.html          # HTML entry point
│   │   ├── package.json        # Node.js dependencies
│   │   ├── package-lock.json   # Dependency lock file
│   │   ├── postcss.config.js   # PostCSS configuration
│   │   ├── tailwind.config.js  # Tailwind CSS configuration
│   │   ├── tsconfig.json       # TypeScript configuration
│   │   ├── vite.config.ts      # Vite build configuration
│   │   └── README.md           # Frontend documentation
│   │
│   └── backend/                # Flask REST API (Application Layer)
│       ├── models/             # SQLAlchemy database models
│       │   ├── __init__.py
│       │   ├── user.py         # User authentication model
│       │   ├── video.py        # Video storage model
│       │   ├── result.py       # Detection result model
│       │   └── audit_log.py    # Audit logging model
│       ├── routes/             # API endpoint handlers
│       │   ├── __init__.py
│       │   ├── auth.py         # Authentication endpoints
│       │   ├── videos.py       # Video upload endpoints
│       │   ├── detections.py  # Detection result endpoints
│       │   ├── admin.py        # Admin endpoints
│       │   └── README.md       # Routes documentation
│       ├── services/           # Business logic layer
│       │   ├── __init__.py
│       │   ├── genai_service.py        # GenAI API integration
│       │   ├── incident_explanation_engine.py # Incident explanation prompts
│       │   └── README.md       # Services documentation
│       ├── ml/                 # Machine Learning components
│       │   ├── __init__.py
│       │   ├── cnn_lstm_model.py  # CNN-LSTM model definition
│       │   ├── inference.py       # Inference pipeline
│       │   ├── preprocessing.py   # Video preprocessing utilities
│       │   └── README.md          # ML components documentation
│       ├── tests/              # Test suite
│       │   ├── __init__.py
│       │   ├── conftest.py     # Pytest configuration
│       │   ├── test_models.py  # Database model tests
│       │   ├── test_auth.py    # Authentication tests
│       │   ├── test_videos.py  # Video upload tests
│       │   ├── test_detections.py # Detection endpoint tests
│       │   └── test_ml.py      # ML inference tests
│       ├── utils/              # Utility functions
│       │   ├── __init__.py
│       │   ├── audit_helpers.py
│       │   ├── request_helpers.py
│       │   └── validators.py
│       ├── app.py              # Flask application factory
│       ├── config.py           # Configuration management
│       ├── db.py               # Database initialization
│       ├── pyproject.toml      # Python project configuration
│       ├── requirements.txt    # Python dependencies
│       └── README.md           # Backend documentation
│
├── docs/                       # Project documentation
│   ├── 01_abstract.md          # Project abstract
│   ├── 02_requirements.md      # Requirements specification
│   ├── 03_setup.md             # Setup guide (prerequisites, installation)
│   ├── 04_usage.md             # Usage guide (features, workflows)
│   ├── 05_technical.md         # Technical documentation
│   ├── 06_architecture_plan.md # Architecture planning
│   ├── 07_comparison.md        # Approach comparison
│   ├── 08_repository_structure.md # This file (repository structure)
│   ├── 09_authentication_authorization.md # Auth documentation
│   ├── 10_prompt_engineering_strategy.md # Prompt engineering
│   ├── 11_database_schema.md   # Database schema documentation
│   ├── diagrams/               # Architecture diagrams
│   │   ├── system-architecture.mmd
│   │   ├── system-architecture-simple.mmd
│   │   ├── mermaid-config.json
│   │   └── README.md
│   ├── images/                 # Documentation images
│   ├── masterplan.md           # Master plan document
│   ├── reference/               # Reference materials
│   └── reports/                # Project reports
│
├── tools/                      # Utility scripts and automation
│   └── psscripts/              # PowerShell scripts
│       ├── Compare-DocFiles.ps1
│       ├── Find-DuplicateContent.ps1
│       ├── Get-FileStats.ps1
│       ├── Get-MarkdownSummary.ps1
│       ├── Get-RepoStats.ps1
│       ├── Quick-HealthCheck.ps1
│       ├── RepoConfig.psd1
│       ├── Run-MarkdownLintAndLychee.ps1
│       ├── Test-ContentCompliance.ps1
│       ├── Validate-FileReferences.ps1
│       ├── Verify-ZeroCopy.ps1
│       ├── Run-AllPSScripts.ps1
│       └── README.md
│
├── .python-version             # Python version specification (3.9+)
├── CODE_OF_CONDUCT.md          # Code of conduct
├── CONTRIBUTING.md             # Contribution guidelines
├── LICENSE                     # MIT License
├── lychee.toml                 # Lychee link checker configuration
├── pyproject.toml              # Root Python project configuration
└── README.md                   # Main project README
```

---

## Layer Organization

### Presentation Layer (`src/frontend/`)

**Technology:** React.js, TypeScript, Redux Toolkit, Tailwind CSS, Vite

**Key Directories:**

- `src/api/` - API client with JWT token handling
- `src/components/` - Reusable UI components (Layout, Route guards, VideoUpload)
- `src/pages/` - Page-level components (Login, Register, VideoAnalysis, DetectionResults, History, Admin)
- `src/store/` - Redux state management (auth, videos)
- `src/types/` - TypeScript type definitions

**Key Files:**

- `src/App.tsx` - Main application with routing
- `src/main.tsx` - Application entry point
- `vite.config.ts` - Build configuration
- `tailwind.config.js` - CSS framework configuration

---

### Application Layer (`src/backend/`)

**Technology:** Flask, SQLAlchemy, Flask-JWT-Extended, TensorFlow, OpenCV

**Key Directories:**

- `models/` - Database models (User, Video, Result, AuditLog)
- `routes/` - API endpoints (auth, videos, detections, admin)
- `services/` - Business logic (GenAI service, incident explanation engine)
- `ml/` - Machine Learning components (CNN-LSTM model, inference pipeline)
- `tests/` - Comprehensive test suite

**Key Files:**

- `app.py` - Flask application factory
- `config.py` - Environment-based configuration
- `db.py` - Database initialization
- `requirements.txt` - Python dependencies

---

### Machine Learning Layer (`src/backend/ml/`)

**Technology:** TensorFlow/Keras, OpenCV, NumPy

**Key Components:**

- `cnn_lstm_model.py` - CNN-LSTM model architecture definition
- `inference.py` - Inference pipeline for violence detection
- `preprocessing.py` - Video frame extraction and normalization

**Key Features:**

- Inference-only execution (no training)
- CPU-optimized for student machines
- Frame extraction and sequence generation
- Violence probability scoring

---

### GenAI Service Layer (`src/backend/services/`)

**Technology:** Generative AI API (Google Gemini, OpenAI, etc.)

**Key Components:**

- `genai_service.py` - GenAI API client
- `incident_explanation_engine.py` - Prompt construction for incident explanations

**Key Features:**

- Post-processing layer (does not process raw video)
- Converts detection results to human-readable reports
- Structured prompt engineering
- Confidence-aware explanations

---

### Infrastructure Layer (`infra/`)

**Technology:** Docker Compose, PostgreSQL

**Key Files:**

- `docker-compose.yml` - Docker Compose configuration for PostgreSQL
- `.env.example` - Docker Compose environment variables template
- `database/schema.sql` - Complete database schema
- `database/README.md` - Database setup instructions

**Tables:**

- `users` - User accounts and authentication
- `videos` - Uploaded video metadata
- `results` - Detection results and GenAI summaries
- `audit_logs` - System audit trail

---

### Documentation Layer (`docs/`)

**Contents:**

- Project documentation (abstract, requirements, usage, technical)
- Architecture diagrams (Mermaid source files)
- Master plan and structure analysis

---

## Key Files Reference

### Configuration Files

- `.python-version` - Python version (3.9+)
- `pyproject.toml` - Root Python project config
- `src/backend/pyproject.toml` - Backend-specific config
- `src/frontend/package.json` - Frontend dependencies
- `src/backend/requirements.txt` - Backend dependencies
- `lychee.toml` - Link checker configuration

### Entry Points

- `src/frontend/src/main.tsx` - Frontend entry point
- `src/backend/app.py` - Backend entry point
- `infra/database/schema.sql` - Database initialization

### Documentation

- `README.md` - Main project documentation
- `docs/01_abstract.md` - Project abstract (single source of truth)
- `docs/02_requirements.md` - Requirements specification
- `docs/03_setup.md` - Setup and installation guide
- `docs/04_usage.md` - Usage guide and user workflows
- `docs/05_technical.md` - Technical implementation details
- `docs/06_architecture_plan.md` - Architecture planning and design
- `docs/08_repository_structure.md` - This file (repository structure)
- `docs/09_authentication_authorization.md` - Authentication and security
- `docs/10_prompt_engineering_strategy.md` - GenAI prompt engineering strategy
- `docs/11_database_schema.md` - Database schema documentation
- `docs/masterplan.md` - Original master plan (historical reference)
- `CONTRIBUTING.md` - Contribution guidelines
- `CODE_OF_CONDUCT.md` - Code of conduct
- `SECURITY.md` - Security policy

---

## N-Tier Architecture Mapping

| Layer | Directory | Technology |
|-------|-----------|------------|
| **Presentation** | `src/frontend/` | React.js + TypeScript |
| **Application** | `src/backend/` | Flask REST API |
| **ML Processing** | `src/backend/ml/` | TensorFlow, OpenCV |
| **GenAI Service** | `src/backend/services/` | Generative AI API |
| **Data** | `infra/database/` | PostgreSQL |
| **Infrastructure** | `infra/` | Docker Compose, Database Schema |

---

## File Naming Conventions

### Python Files (Backend)

- Snake_case: `cnn_lstm_model.py`, `incident_explanation_engine.py`
- Descriptive names: `video_service.py`, `auth_routes.py`

### TypeScript/React Files (Frontend)

- **Components**: PascalCase: `VideoUpload.tsx`, `DetectionResults.tsx`, `Login.tsx`
- **API Client**: camelCase: `client.ts`
- **Types**: PascalCase: `index.ts` (with interfaces/types)

### Documentation Files

- Numbered sequence: `01_abstract.md`, `02_requirements.md`
- Descriptive names: `masterplan.md`

---

## Development Workflow

### Adding New Features

1. **Frontend Feature:**
   - Add component in `src/frontend/src/components/` or `src/frontend/src/pages/`
   - Update types in `src/frontend/src/types/`
   - Update Redux store if needed in `src/frontend/src/store/`

2. **Backend Feature:**
   - Add route in `src/backend/routes/`
   - Add service logic in `src/backend/services/`
   - Update models in `src/backend/models/` if needed
   - Add tests in `src/backend/tests/`

3. **ML Component:**
   - Add ML logic in `src/backend/ml/`
   - Update inference pipeline if needed
   - Add tests for ML components

4. **Database Changes:**
   - Update `infra/database/schema.sql`
   - Create migration if using Flask-Migrate

---

## Testing Structure

### Backend Tests (`src/backend/tests/`)

- `test_models.py` - Database model tests
- `test_auth.py` - Authentication tests
- `test_videos.py` - Video upload tests
- `test_detections.py` - Detection endpoint tests
- `test_ml.py` - ML inference tests
- `conftest.py` - Pytest configuration and fixtures

**Run tests:**
```powershell
cd src/backend
pytest tests/
```

### Frontend Tests

TypeScript compilation and ESLint validation ensure type safety and code quality.

---

## Build and Deployment

### Frontend Build

```powershell
cd src/frontend
npm run build  # Outputs to src/frontend/dist/
```

### Backend Deployment

- Flask application runs from `src/backend/app.py`
- Uses environment variables for configuration
- Database migrations via Flask-Migrate (if configured)

### Infrastructure

- Docker Compose configuration in `infra/docker-compose.yml`
- Environment variables template in `infra/.env.example`
- Database schema in `infra/database/schema.sql`
- Run Docker Compose from `infra/` directory or use `-f infra/docker-compose.yml` from root

---

## Related Documentation

- [Requirements Specification](02_requirements.md) - System requirements
- [Setup Guide](03_setup.md) - Installation and configuration
- [Usage Guide](04_usage.md) - How to use the application
- [Technical Documentation](05_technical.md) - Technical implementation details
- [Architecture Plan](06_architecture_plan.md) - Detailed architecture documentation
- [Authentication & Authorization](09_authentication_authorization.md) - Security implementation
- [Prompt Engineering Strategy](10_prompt_engineering_strategy.md) - GenAI prompt design
- [Database Schema](11_database_schema.md) - Database structure and design

---