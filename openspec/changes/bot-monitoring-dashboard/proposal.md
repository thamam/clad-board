# Proposal: bot-monitoring-dashboard

## Intent
Build a unified web-based monitoring dashboard for AI agent bots. The system
provides real-time visibility into bot health, configuration, and resource usage
via a sidecar pattern — bots emit structured JSON logs, lightweight sidecars
forward telemetry to a central dashboard, and operators view everything through
a secured web interface.

## Scope

### Included
- Dashboard backend (FastAPI + SQLite) with telemetry ingestion API
- Dashboard frontend (React + Tailwind) with overview and bot detail views
- Sidecar agent that tails bot logs and forwards events
- Bot registration flow with token-based auth
- Token usage aggregation (all-time, 24h, month-to-date)
- HTTP Basic Auth for dashboard access
- Docker Compose deployment with Caddy HTTPS
- Log schema contract (startup, heartbeat, message, token_usage, error events)

### Out of scope
- Command & control (start/stop bots, send messages)
- HTTP endpoints on bot side
- Real-time websocket streaming (polling for MVP)
- Multi-user roles or permissions
- Alerting or notifications
- Historical charts or time-series visualization

## Approach
Three-service architecture: a Python sidecar container per bot instance, a
FastAPI backend serving both the REST API and static frontend, and a React SPA.
SQLite for data storage (upgrade path to Postgres). Caddy reverse proxy for
HTTPS. All services orchestrated via Docker Compose on an existing EC2 instance.

## Affected Specs
- `telemetry-ingestion` — event schema, ingestion API, token aggregation
- `bot-registration` — registration flow, token generation, bot registry
- `sidecar` — log tailing, parsing, forwarding, retry logic
- `dashboard-api` — REST endpoints, data queries, auth middleware
- `dashboard-ui` — overview page, bot detail page, polling
- `authentication` — HTTP Basic Auth, session management

## Success Criteria
- [ ] Dashboard accessible at `dashboard.neuronbox.ai` with HTTPS
- [ ] Bot registration creates token, sidecar connects using it
- [ ] Sidecar correctly tails and forwards all 5 event types
- [ ] Overview page shows all bots with live status (online/idle/offline)
- [ ] Bot detail page shows config, activity, token usage, and errors
- [ ] Token usage aggregated across all-time, 24h, and month-to-date segments
- [ ] HTTP Basic Auth protects all dashboard pages
- [ ] Full Docker Compose stack starts with `docker compose up`
