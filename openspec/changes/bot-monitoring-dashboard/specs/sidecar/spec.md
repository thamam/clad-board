# Delta for sidecar

## ADDED Requirements

### Requirement: log-tailing
The sidecar SHALL continuously tail the bot's log source.

#### Scenario: file-based logs
- GIVEN LOG_PATH is set to a file path (e.g., `/logs/bot.log`)
- WHEN new lines are appended to the file
- THEN the sidecar SHALL read and process each new line

#### Scenario: stdout logs
- GIVEN LOG_PATH is set to "stdout"
- WHEN the bot container emits lines to stdout
- THEN the sidecar SHALL read and process each line from the shared stream

### Requirement: log-parsing
The sidecar SHALL parse each log line as JSON and validate against the schema.

#### Scenario: valid JSON log line
- GIVEN a log line containing valid JSON with `timestamp`, `bot_id`, `event_type`, `payload`
- WHEN the sidecar processes the line
- THEN it SHALL forward the event to the Dashboard API

#### Scenario: non-JSON log line
- GIVEN a log line that is not valid JSON
- WHEN the sidecar processes the line
- THEN it SHALL skip the line silently (no crash, no error propagation)

#### Scenario: missing required fields
- GIVEN a JSON log line missing `event_type`
- WHEN the sidecar processes the line
- THEN it SHALL skip the line and log a warning locally

### Requirement: event-forwarding
The sidecar SHALL forward parsed events to the Dashboard API.

#### Scenario: successful forwarding
- GIVEN a valid parsed event
- WHEN the sidecar sends it to `POST /api/ingest`
- THEN it SHALL include the registration token in the Authorization header

#### Scenario: connection failure
- GIVEN the Dashboard API is unreachable
- WHEN the sidecar attempts to forward an event
- THEN it SHALL buffer the event locally and retry with exponential backoff

#### Scenario: buffer overflow
- GIVEN the local buffer exceeds 1000 events
- WHEN new events arrive
- THEN the sidecar SHALL drop the oldest events to make room

### Requirement: configuration
The sidecar SHALL be configured via environment variables:
`DASHBOARD_URL`, `REGISTRATION_TOKEN`, `LOG_PATH`.

#### Scenario: missing required config
- GIVEN REGISTRATION_TOKEN is not set
- WHEN the sidecar starts
- THEN it SHALL exit with a clear error message
