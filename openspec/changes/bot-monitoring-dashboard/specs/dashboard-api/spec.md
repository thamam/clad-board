# Delta for dashboard-api

## ADDED Requirements

### Requirement: ingest-endpoint
The system SHALL expose `POST /api/ingest` for receiving telemetry events.

#### Scenario: batch ingestion
- GIVEN a sidecar with multiple buffered events
- WHEN it sends a POST with an array of events
- THEN the system SHALL process each event individually
- AND return HTTP 200 with a count of accepted events

### Requirement: bot-detail-endpoint
The system SHALL expose `GET /api/bots/:id` for retrieving bot details.

#### Scenario: full bot detail
- GIVEN a registered bot with telemetry data
- WHEN an authenticated user requests its details
- THEN the system SHALL return:
  - Identity: name, class, version, uptime
  - Configuration: models, channels, skills, tools
  - Activity: messages in/out counts, last message timestamp
  - Token usage: per-model breakdown with all-time/24h/MTD segments
  - Errors: count, last error message and timestamp

### Requirement: bot-status-computation
The system SHALL compute bot status from heartbeat recency.

#### Scenario: online status
- GIVEN a bot whose last heartbeat was within the last 2 minutes
- WHEN status is queried
- THEN the system SHALL return `online`

#### Scenario: idle status
- GIVEN a bot whose last heartbeat was between 2 and 10 minutes ago
- WHEN status is queried
- THEN the system SHALL return `idle`

#### Scenario: offline status
- GIVEN a bot whose last heartbeat was more than 10 minutes ago
- WHEN status is queried
- THEN the system SHALL return `offline`

### Requirement: data-storage
The system SHALL use SQLite with standard SQL queries.

#### Scenario: schema
- GIVEN the database is initialized
- THEN it SHALL contain tables: `bots`, `events`, `token_aggregates`

### Requirement: cors-and-serving
The system SHALL serve the frontend static files and handle CORS for API routes.
