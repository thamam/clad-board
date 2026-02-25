# Tasks: bot-monitoring-dashboard

## Phase 1: Project scaffolding

- [x] 1.1 Initialize project structure: `backend/`, `frontend/`, `sidecar/` directories with placeholder files
- [x] 1.2 Create backend `requirements.txt` (fastapi, uvicorn, sqlmodel, bcrypt)
- [x] 1.3 Create frontend with Vite + React + Tailwind (`npm create vite`, install tailwind, react-router, react-query)
- [x] 1.4 Create sidecar `requirements.txt` (watchfiles, httpx)
- [x] 1.5 Create `docker-compose.yml` with backend, frontend-build, and Caddy services
- [x] 1.6 Create `Caddyfile.snippet` for `dashboard.neuronbox.ai` route

## Phase 2: Backend — data layer

- [x] 2.1 Create `models.py` with SQLModel models: Bot, Event, TokenAggregate
- [x] 2.2 Create `database.py` with SQLite engine, session dependency, table init (WAL mode)
- [x] 2.3 Create `auth.py` with Basic Auth dependency and token validation helper

## Phase 3: Backend — API routes

- [x] 3.1 Create `routes/register.py` — `POST /api/register` (admin-only, generates UUID + hashed token, returns bot_id + raw token)
- [x] 3.2 Create `routes/ingest.py` — `POST /api/ingest` (token auth, accepts single or batch events, stores to DB, updates aggregates)
- [x] 3.3 Create `routes/bots.py` — `GET /api/bots` (list all bots with status) and `GET /api/bots/:id` (full detail with metrics)
- [x] 3.4 Create `aggregation.py` — token usage aggregation logic (all-time from aggregates table, 24h and MTD computed from events)
- [x] 3.5 Create `main.py` — FastAPI app, include routers, CORS middleware, static file serving, startup DB init

## Phase 4: Sidecar

- [x] 4.1 Create `sidecar/main.py` — config from env vars, validation, graceful startup/shutdown
- [x] 4.2 Implement log tailing (file-based with watchfiles, stdout mode)
- [x] 4.3 Implement JSON parsing with schema validation (skip non-JSON, warn on missing fields)
- [x] 4.4 Implement event forwarding with retry logic (exponential backoff, 1000-event buffer cap)
- [x] 4.5 Create `sidecar/Dockerfile` — minimal Python image, copy code, set entrypoint

## Phase 5: Frontend — core pages

- [x] 5.1 Create `src/api.js` — API client with React Query hooks, Basic Auth header injection, polling config
- [x] 5.2 Create `src/components/StatusBadge.jsx` — green/yellow/red indicator based on status
- [x] 5.3 Create `src/components/BotCard.jsx` — card showing name, class, status, last heartbeat, message count, error count
- [x] 5.4 Create `src/pages/Overview.jsx` — bot grid layout, empty state, auto-polling
- [x] 5.5 Create `src/components/TokenTable.jsx` — per-model token usage with segment columns
- [x] 5.6 Create `src/pages/BotDetail.jsx` — identity, config, activity, token usage, errors sections
- [x] 5.7 Create `src/App.jsx` — React Router setup (overview + detail routes), auth context, layout

## Phase 6: Dockerization and integration

- [x] 6.1 Create `backend/Dockerfile` — Python image, install deps, copy code, build frontend into static dir, run uvicorn
- [x] 6.2 Create `frontend/Dockerfile` (multi-stage build: node build → copy dist to backend static)
- [x] 6.3 Finalize `docker-compose.yml` — backend service, volumes for SQLite, Caddy config
- [x] 6.4 Create sidecar Docker Compose snippet for bot operators to copy

## Phase 7: Testing and validation

- [x] 7.1 Write backend tests — registration flow, ingestion, aggregation, auth
- [x] 7.2 Manual end-to-end test: register bot → start sidecar with mock logs → verify dashboard shows data
- [x] 7.3 Write deployment checklist verification script

---
_Generated from proposal.md and design.md_
