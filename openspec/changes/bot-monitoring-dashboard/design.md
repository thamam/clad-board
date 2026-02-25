# Design: bot-monitoring-dashboard

## Context
This is a greenfield project. No existing codebase — only the system spec
(`bot-dashboard-spec.md`). The dashboard will be deployed on an existing AWS
EC2 instance alongside bot infrastructure, using Docker Compose and Caddy for
HTTPS termination.

Target bots (OpenClaw, Letta) already run in Docker. The sidecar will be added
to their Compose stacks as a new service sharing the log volume.

## Decisions

### Decision: Backend framework
**Chosen:** FastAPI (Python)
**Rationale:** Matches the existing bot ecosystem (Python-based), async-first,
built-in OpenAPI docs, minimal boilerplate. The team already knows Python.
**Alternatives considered:** Express.js (would add Node to the stack), Go
(faster but higher learning curve, less flexible for rapid iteration).

### Decision: Database
**Chosen:** SQLite via SQLModel ORM
**Rationale:** Zero-ops, single-file database, sufficient for the expected
scale (tens of bots, thousands of events/day). SQLModel provides both
Pydantic validation and SQLAlchemy ORM in one. Standard SQL ensures easy
migration to Postgres later.
**Alternatives considered:** Postgres (overkill for MVP), DynamoDB (vendor
lock-in, harder aggregation queries).

### Decision: Frontend framework
**Chosen:** React with Vite + Tailwind CSS
**Rationale:** Widely known, fast dev experience with Vite HMR. Tailwind for
utility-first styling without CSS files. React Query for server state and
polling.
**Alternatives considered:** Vue (less ecosystem), vanilla JS (too slow to
build), Next.js (SSR not needed for internal dashboard).

### Decision: Sidecar language
**Chosen:** Python
**Rationale:** Consistency with the backend, shared schema validation code,
simpler Docker build. The sidecar is IO-bound (file watching + HTTP), so
Python performance is adequate.
**Alternatives considered:** Go (smaller binary but adds a second language to
maintain).

### Decision: Auth strategy
**Chosen:** HTTP Basic Auth for dashboard, Bearer token for sidecar API
**Rationale:** Simplest possible auth for an internal monitoring tool. Caddy
can optionally enforce Basic Auth at the proxy layer for zero-code protection.
Bearer tokens for sidecars are generated at registration time.
**Alternatives considered:** OAuth (overkill for single-user MVP), API keys
in headers (essentially what we're doing with tokens).

### Decision: Frontend serving
**Chosen:** FastAPI serves static build files
**Rationale:** Single container for backend + frontend, simpler deployment.
React app is built at Docker build time and served as static files. No need
for a separate frontend container or Nginx.
**Alternatives considered:** Separate frontend container (more complex Compose),
Caddy serves static files (splits concerns but adds routing complexity).

## Architecture / Approach

```
┌─────────────────┐     ┌─────────────────┐
│  Bot Container   │     │  Bot Container   │
│  (OpenClaw)      │     │  (Letta)         │
│  └─ logs/bot.log │     │  └─ logs/bot.log │
└────────┬────────┘     └────────┬────────┘
         │ volume mount           │ volume mount
┌────────▼────────┐     ┌────────▼────────┐
│  Sidecar         │     │  Sidecar         │
│  - tail logs     │     │  - tail logs     │
│  - parse JSON    │     │  - parse JSON    │
│  - POST /ingest  │     │  - POST /ingest  │
└────────┬────────┘     └────────┬────────┘
         │ HTTPS                  │ HTTPS
         └──────────┬─────────────┘
              ┌─────▼─────┐
              │   Caddy    │
              │  (HTTPS)   │
              └─────┬─────┘
              ┌─────▼─────┐
              │  Dashboard  │
              │  Backend    │
              │  (FastAPI)  │
              │  + static   │
              │    frontend │
              │  + SQLite   │
              └────────────┘
```

### Backend modules
- `main.py` — FastAPI app, middleware, static file serving
- `models.py` — SQLModel models (Bot, Event, TokenAggregate)
- `database.py` — DB engine, session, init
- `routes/ingest.py` — `POST /api/ingest` (sidecar-facing, token auth)
- `routes/bots.py` — `GET /api/bots`, `GET /api/bots/:id` (dashboard-facing)
- `routes/register.py` — `POST /api/register` (admin)
- `auth.py` — Basic Auth dependency, token validation
- `aggregation.py` — Token usage aggregation logic

### Frontend structure
- `src/App.jsx` — Router, auth context
- `src/pages/Overview.jsx` — Bot grid with cards
- `src/pages/BotDetail.jsx` — Detailed bot view
- `src/components/BotCard.jsx` — Individual bot card
- `src/components/TokenTable.jsx` — Token usage breakdown
- `src/components/StatusBadge.jsx` — Online/idle/offline indicator
- `src/api.js` — API client with React Query hooks

## Data Model

### `bots` table
| Column | Type | Notes |
|---|---|---|
| id | TEXT (UUID) | Primary key |
| name | TEXT | Human-readable |
| class | TEXT | Framework (openclaw, letta) |
| token | TEXT | Registration token (hashed) |
| registered_at | DATETIME | |
| status | TEXT | active / inactive |
| last_heartbeat | DATETIME | Updated on heartbeat event |
| last_startup | JSON | Latest startup payload |

### `events` table
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Auto-increment PK |
| bot_id | TEXT (UUID) | FK → bots |
| event_type | TEXT | startup/heartbeat/message/token_usage/error |
| payload | JSON | Raw payload |
| timestamp | DATETIME | From the event |
| received_at | DATETIME | Server receive time |

### `token_aggregates` table
| Column | Type | Notes |
|---|---|---|
| id | INTEGER | Auto-increment PK |
| bot_id | TEXT (UUID) | FK → bots |
| model | TEXT | LLM model name |
| tokens_in_total | INTEGER | All-time input tokens |
| tokens_out_total | INTEGER | All-time output tokens |
| updated_at | DATETIME | Last update |

Note: `last_24h` and `month_to_date` are computed at query time from the
events table, while `all_time` uses the pre-computed aggregates table.

## API Changes

All new endpoints (no existing API):

| Method | Path | Auth | Purpose |
|---|---|---|---|
| POST | /api/ingest | Bearer token | Receive telemetry events |
| POST | /api/register | Basic Auth | Register new bot |
| GET | /api/bots | Basic Auth | List all bots |
| GET | /api/bots/:id | Basic Auth | Bot detail + metrics |

## Risks and Mitigations

| Risk | Mitigation |
|---|---|
| SQLite write contention under high event volume | Single writer pattern, WAL mode, batch inserts |
| Sidecar buffer loss on crash | Accept data loss for MVP; add disk-based buffer later |
| Log file rotation breaks tailing | Use `watchfiles` with inode tracking; re-open on rotate |
| Token stored in plain text in DB | Hash tokens with bcrypt; compare on auth |
| Basic Auth credentials in env vars | Acceptable for internal tool; upgrade to OAuth later |
