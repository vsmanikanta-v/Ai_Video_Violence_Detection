# AI Video Violence Detection System - Presentation Outline

**Last reviewed:** March 16, 2026 — API slide updated: video, detections, and admin endpoints are implemented; paths aligned with `docs/reference/api-surface.md`. React 19.2.

---

## Slide 1: Title Slide

**Title:** AI Video Violence Detection System
**Subtitle:** Deep Learning-Based Violence Detection with GenAI Incident Explanations

**Presented by:** Jyothi, Rishika, Sumasri and Vishnu
**Date:** March 13, 2026

---

## Slide 2: Agenda

* Problem Statement
* Proposed Solution
* How This Differs from Existing Solutions
* Real-Time Applications
* Research Background
* Key Features
* Technology Stack
* System Architecture
* Database Schema / ER Diagram
* Authentication Flow Diagram
* API (Swagger) Overview
* Methodology: Video Analysis Workflow
* AI Integration Strategy
* Conclusion & Future Scope

---

## Slide 3: Problem Statement

### The Challenge in Video Surveillance Security

* **Manual Monitoring Limitations**
  Human operators cannot continuously monitor multiple video feeds, leading to delayed incident detection.

* **Alert Fatigue**
  Security personnel face overwhelming volumes of surveillance footage, making it difficult to identify critical events.

* **Lack of Explainability**
  Traditional detection systems provide binary alerts without context, reducing trust and actionable insights.

* **Security Concerns**
  Many solutions lack enterprise-grade authentication and access control for sensitive video data.

* **Resource Constraints**
  Real-time GPU-dependent systems limit accessibility in academic and resource-constrained environments.

---

## Slide 4: Proposed Solution

### Hybrid AI with N-Tier Enterprise Architecture

* **Spatial-Temporal Deep Learning**
  CNN + LSTM architecture for spatial features (frames) and temporal patterns (motion); inference-only, CPU-friendly.

* **GenAI-Powered Explanations**
  Human-readable incident reports from detection results for security personnel.

* **Enterprise Architecture**
  Built on a secure N-Tier architecture (Presentation, Application, ML Processing, GenAI Service, Data).

* **Role-Based Security**
  Strict access control for **Users** (upload, view results) and **Administrators** (monitoring, audit).

* **Full Traceability**
  All uploads, detection results, and system actions are logged for auditability.

---

## Slide 5: How This Differs from Existing Solutions

### Key Differentiators

| Aspect         | Existing Solutions          | This Project                         |
| -------------- | --------------------------- | ------------------------------------ |
| Architecture   | Black-box ML scripts        | N-Tier enterprise architecture       |
| Explainability | Binary alerts only          | GenAI incident explanations          |
| Hardware       | GPU-dependent               | CPU-optimized inference              |
| Security       | Basic or none               | JWT + RBAC + audit logging           |
| Processing     | Real-time streaming         | Offline short-video analysis          |
| Traceability   | No logging                  | Full video/result history & audit     |

### Unique Innovations

1. **Enterprise-Grade Security**
   JWT authentication, RBAC, and comprehensive audit logging.

2. **Hybrid Deep Learning + GenAI**
   CNN-LSTM for detection; GenAI for human-readable incident reports.

3. **N-Tier Architecture**
   Five-layer design suitable for real enterprise deployment.

4. **Explainable AI**
   Security personnel receive actionable context (timestamps, confidence, summary).

5. **Video & Result Management**
   Complete history of videos and detection results with audit trail.

6. **Academic + Practical Balance**
   Architecturally sound system with real-world applicability.

---

## Slide 6: Real-Time Applications

This system can be used in multiple real-world environments:

#### Campus & Education

* Automated monitoring of campus surveillance for fights or bullying
* Evidence and audit trail for disciplinary processes

#### Public Safety & Municipal

* Surveillance for public disturbances, assaults, or violent incidents
* Faster incident response with contextual alerts

#### Retail & Loss Prevention

* Store safety and loss-prevention monitoring
* Employee and customer safety

#### Transportation Hubs

* Violence detection in airports, stations, and terminals
* Passenger and staff safety

#### Healthcare & Corrections

* Patient and staff safety in hospitals and psychiatric facilities
* Inmate behavior monitoring and early incident detection

#### Security Operations

* Centralized audit of detections and GenAI explanations
* Compliance and forensic analysis

---

## Slide 7: Research Background

This project is **architecture-driven rather than paper-replication based**.

The system design draws inspiration from established concepts in:

* **Deep Learning for Video Understanding** (CNN, LSTM, spatial-temporal models)
* **Explainable AI and GenAI for Security**
* **Enterprise N-Tier Software Architecture**
* **Secure API Design using JWT Authentication**

Instead of replicating a single research paper, the project integrates **multiple modern software engineering and AI concepts** to build a practical, explainable violence-detection solution.

---

## Slide 8: Key Features

* **Violence Detection Engine**
  CNN-LSTM model identifies violent activities in video clips; outputs violence score and classification (VIOLENT / NON_VIOLENT).

* **Confidence & Explainability**
  Confidence levels (HIGH / MEDIUM / LOW); GenAI-generated incident summaries with timestamps and context.

* **Role-Based Access Control (RBAC)**

  **Users**

  * Upload videos
  * View own detection results and history

  **Admins**

  * System summary and monitoring
  * View audit logs

* **Video & Result History**
  Persists uploaded videos and detection results for future reference and audit.

* **Secure Authentication**
  JWT-based stateless authentication with bcrypt password hashing.

---

## Slide 9: Technology Stack

### Frontend

* React 19.2 (TypeScript)
* Redux Toolkit (state management)
* Tailwind CSS
* Vite (build tool)
* Video upload interface, detection results, history, admin dashboard

### Backend

* FastAPI (Python 3.12)
* REST API Architecture
* psycopg2 (direct parameterized SQL)

### ML & AI

* TensorFlow / Keras (CNN + LSTM)
* OpenCV (video preprocessing, frame extraction)
* GenAI API (**Google Gemini** — `google-genai`, `GEMINI_API_KEY`; mock if unset)

### Data & Security

* PostgreSQL (Users, Videos, Results, Audit Logs)
* JSON Web Token (JWT) Security
* Bcrypt password hashing

---

## Slide 10: System Architecture

### N-Tier Enterprise Architecture

1️⃣ **Presentation Layer**

* React Single Page Application
* Video upload, detection results, history, admin dashboard

2️⃣ **Application Layer**

* FastAPI REST API
* Authentication, video service, detection service, audit logging

3️⃣ **ML Processing Layer**

* Frame extraction and preprocessing
* CNN-LSTM inference and violence scoring

4️⃣ **GenAI Service Layer**

* Incident explanation generation from detection results
* Prompt construction and report formatting

5️⃣ **Data Layer**

* PostgreSQL database
* Stores Users, Videos, Results, and Audit Logs

---

## Slide 11: Database Schema / ER Diagram

### Database Schema & Entity Relationships

The system uses a **PostgreSQL relational database** to store application data.

#### Core Tables

#### Users

* id (Primary Key)
* username (Unique)
* email (Unique)
* password_hash (bcrypt)
* role (USER or ADMIN)
* created_at

#### Videos

* id (Primary Key)
* user_id (Foreign Key)
* file_path, filename, file_size, duration_seconds, video_format
* uploaded_at

#### Results

* id (Primary Key)
* video_id (Foreign Key)
* violence_score, prediction (VIOLENT / NON_VIOLENT), confidence_level
* key_frame_timestamps, processing_time_seconds, genai_summary
* created_at

#### Audit Logs

* id (Primary Key)
* user_id (Foreign Key)
* action, entity_type, entity_id, details
* created_at

#### Key Design Principles

* Foreign key constraints ensure **data integrity**
* Role-based ownership of videos and results
* Complete **audit trail of system activities**

---

## Slide 12: Authentication Flow Diagram

### Authentication & Authorization Workflow

The system implements **JWT-based stateless authentication**.

#### Authentication Steps

1️⃣ User enters **username and password** (registration also requires email)

2️⃣ Backend validates credentials using **bcrypt**

3️⃣ If valid, backend generates **JWT access token**

4️⃣ Token is returned to the client

5️⃣ Client includes token in the **Authorization header**

```
Authorization: Bearer <JWT>
```

6️⃣ Backend validates the token for every request

7️⃣ **Role-Based Access Control** determines permissions

#### Permissions

**User**

* Upload videos
* View own results and history

**Admin**

* System summary and monitoring
* View audit logs

#### Security Features

* Stateless authentication
* Secure password hashing (bcrypt)
* Token expiration
* Protected API endpoints

---

## Slide 13: API (Swagger) Overview

### REST API & Swagger Documentation

The backend exposes a **RESTful API** implemented using **FastAPI**.

API endpoints are documented with **Swagger UI** at `/api/docs`, **ReDoc** at `/redoc`, **OpenAPI JSON** at `/openapi.json`, and **OpenAPI YAML** at `/api/openapi.yaml` when the backend is running. See also `docs/reference/api-surface.md`.

#### System

```
GET  /                         API root and metadata
GET  /health                   Health check
GET  /api/openapi.yaml         OpenAPI specification (YAML)
```

#### Authentication

```
POST /api/auth/register       Register (username, email, password, role: USER only)
POST /api/auth/login          Login (username, password)
GET  /api/auth/me              Current user (requires JWT)
GET  /api/auth/admin-check     Admin role verification (requires JWT)
```

#### Videos (implemented)

```
POST /api/videos/upload           Upload video (multipart/form-data; requires JWT; rate limited)
POST /api/videos/{video_id}/analyze  Run violence detection on uploaded video
GET  /api/videos/history             List current user's videos
GET  /api/videos/{video_id}        Get video metadata and results (user must own video)
```

#### Detections (implemented)

```
GET  /api/detections/result/{result_id}  Get detection by result ID (user must own video)
GET  /api/detections/video/{video_id}     List detections for a video (user must own video)
```

#### Admin (implemented)

```
GET  /api/admin/stats          Aggregate counts (users, videos, results, audit logs) — Admin only
GET  /api/admin/audit-logs     List audit log entries (paginated; limit, offset) — Admin only
```

#### Benefits of Swagger / OpenAPI

* Interactive API testing
* Automatic API documentation
* Clear contract between frontend and backend

---

## Slide 14: Methodology – Video Analysis Workflow

### How the System Works

1️⃣ **Video Upload**

User uploads a short video clip (e.g. 30–60 seconds) via the React interface.

2️⃣ **Preprocessing**

Frame extraction (OpenCV), resizing (64×64), normalization.

3️⃣ **ML Inference**

CNN extracts spatial features; LSTM analyzes temporal sequence; model outputs violence score (0.0–1.0) and classification.

4️⃣ **GenAI Explanation**

Detection result (score, timestamps, confidence) is sent to GenAI to generate a human-readable incident summary.

5️⃣ **Persistence & Response**

Result and GenAI summary are stored in **PostgreSQL**; full response returned to the user with audit log entry.

---

## Slide 15: AI Integration Strategy

### Leveraging Deep Learning + GenAI

#### CNN-LSTM Pipeline

* **CNN:** Spatial feature extraction from video frames (64×64×3).
* **LSTM:** Temporal pattern recognition over frame sequences.
* **Output:** Violence probability (0.0–1.0), classification, confidence level.
* **Inference-only:** Custom CNN-LSTM model; supports local training via `train.py`; CPU-optimized.

#### GenAI for Explanations

* **Input:** Detection result (score, prediction, confidence, key-frame timestamps).
* **Output:** Professional incident report for security personnel.
* **Design:** GenAI does not process raw video; only structured detection data—reduces cost and improves clarity.

#### Safety & Validation

* Input validation on upload (file type, size)
* Structured prompts for factual, professional incident reports
* Audit logging of all analyses and explanations

---

## Slide 16: Conclusion & Future Scope

### Conclusion

* Automates violence detection in surveillance-style video clips using CNN-LSTM.
* Demonstrates secure integration of **deep learning and GenAI in an enterprise system**.
* Explainable outputs (confidence + GenAI summary) support trust and actionable response.
* N-Tier architecture provides a scalable foundation for security and monitoring tools.

### Future Scope

* **Real-Time Processing** — Integration with live streams (e.g. RTSP / HLS).
* **Multi-Class Detection** — Detect specific violence types (assault, weapon use, etc.).
* **Edge Deployment** — Optimize for edge devices (e.g. Raspberry Pi, Jetson).
* **Active Learning** — Feedback from security personnel to improve model accuracy.
* **Dashboard Analytics** — Incident trends, detection patterns, and performance metrics.
