# Delta for bot-registration

## ADDED Requirements

### Requirement: bot-registry
The system SHALL maintain a registry of bot instances with fields:
`bot_id` (UUID), `name` (string), `class` (string), `token` (string),
`registered_at` (timestamp), `status` (active/inactive).

#### Scenario: register new bot
- GIVEN an admin user is authenticated
- WHEN they POST to `/api/register` with `name` and `class`
- THEN the system SHALL create a new bot record with a generated UUID and token
- AND return the `bot_id` and `token` to the admin

#### Scenario: duplicate name
- GIVEN a bot with name "OpenClaw Production" already exists
- WHEN an admin registers another bot with the same name
- THEN the system SHALL allow it (names are not unique constraints; bot_id is)

### Requirement: token-auth
The system SHALL authenticate sidecar requests using the registration token.

#### Scenario: valid token
- GIVEN a bot with status `active`
- WHEN a request arrives with the bot's token in the Authorization header
- THEN the system SHALL accept the request

#### Scenario: invalid token
- GIVEN a request with an unrecognized token
- WHEN it arrives at `/api/ingest`
- THEN the system SHALL return HTTP 401

#### Scenario: inactive bot
- GIVEN a bot with status `inactive`
- WHEN a request arrives with that bot's token
- THEN the system SHALL return HTTP 403

### Requirement: list-bots
The system SHALL provide an endpoint to list all registered bots.

#### Scenario: list all bots
- GIVEN an authenticated dashboard user
- WHEN they GET `/api/bots`
- THEN the system SHALL return all registered bots with their current status
