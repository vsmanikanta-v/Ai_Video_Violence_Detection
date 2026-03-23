# AI Video Violence Detection — Frontend

React 19.2 + TypeScript + Vite + Tailwind CSS + Redux Toolkit + React Router.

## Setup

```bash
npm install
```

## Develop

```bash
npm run dev
```

Runs at <http://localhost:5173>. API requests to `/api` are proxied to the FastAPI backend (default <http://localhost:8000>).

## Build

```bash
npm run build
```

## Test

```bash
npm run test
```

Runs Vitest (24 unit tests across 6 files: authSlice, videosSlice, API client, PrivateRoute, AdminRoute, ErrorBoundary). For watch mode: `npm run test:watch`.

**Tip:** Run frontend and backend tests after every phase; see the root [README Testing section](../../README.md#testing).

## Environment

- `VITE_API_URL` — Base URL for API (default: empty; use relative paths with Vite proxy in dev).

## Pages and flow

- **Landing** (`/`) — Public landing page (hero, features, tech stack, CTA). Unauthenticated: standalone header + content; authenticated: same content inside Layout. Flow aligned with Gen AI Email and Consumer Complaints.
- **Login** (`/login`) / **Register** (`/register`) — Standalone auth pages with minimal header (app name + link to Register/Login).
- **Upload** (`/upload`) — Video upload with progress; auto-runs analysis and navigates to results.
- **Results** (`/results`) — Latest detection result (score, prediction, GenAI explanation).
- **History** (`/history`) — User's videos and their analysis results.
- **Admin** (`/admin`) — Admin dashboard (audit logs, activity metrics).

**Components:** Layout, PrivateRoute, AdminRoute, VideoUpload, SkipNavigation (skip-to-main-content), ErrorBoundary (runtime error fallback).
