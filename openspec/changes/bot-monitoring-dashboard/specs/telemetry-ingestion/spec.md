# Delta for telemetry-ingestion

## ADDED Requirements

### Requirement: event-schema
The system SHALL accept telemetry events as JSON objects with fields:
`timestamp` (ISO8601), `bot_id` (UUID), `event_type` (string), and `payload` (object).

#### Scenario: valid event ingestion
- GIVEN a registered bot with a valid token
- WHEN the sidecar sends a POST to `/api/ingest` with a valid event
- THEN the system SHALL store the event in the events table
- AND return HTTP 200

#### Scenario: unknown bot
- GIVEN an unregistered bot_id
- WHEN the sidecar sends a POST to `/api/ingest`
- THEN the system SHALL return HTTP 401

### Requirement: event-types
The system SHALL support the following event types:
`startup`, `heartbeat`, `message`, `token_usage`, `error`.

#### Scenario: startup event
- GIVEN a bot that just started
- WHEN a `startup` event is received with payload containing `version`, `models`, `channels`, `skills`, `tools`
- THEN the system SHALL store the configuration snapshot for the bot

#### Scenario: heartbeat event
- GIVEN a running bot
- WHEN a `heartbeat` event is received with `uptime_seconds`
- THEN the system SHALL update the bot's last-seen timestamp

#### Scenario: message event
- GIVEN a running bot
- WHEN a `message` event is received with `direction`, `channel`, and optional `session_id`
- THEN the system SHALL increment the bot's message counter for that direction

#### Scenario: token_usage event
- GIVEN a running bot
- WHEN a `token_usage` event is received with `model`, `tokens_in`, `tokens_out`
- THEN the system SHALL update token aggregates for that bot and model

#### Scenario: error event
- GIVEN a running bot
- WHEN an `error` event is received with `message` and `severity`
- THEN the system SHALL store the error and increment the error counter

### Requirement: token-aggregation
The system SHALL maintain pre-computed token usage aggregates per bot per model.

#### Scenario: aggregation segments
- GIVEN token_usage events for a bot
- WHEN aggregates are queried
- THEN the system SHALL return `all_time`, `last_24h`, and `month_to_date` segments
- AND each segment SHALL contain `tokens_in` and `tokens_out` totals

#### Scenario: month boundary
- GIVEN a new calendar month begins
- WHEN the `month_to_date` segment is queried
- THEN it SHALL only include events from the current month
