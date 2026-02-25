# Delta for authentication

## ADDED Requirements

### Requirement: basic-auth
The system SHALL protect all dashboard pages with HTTP Basic Auth.

#### Scenario: valid credentials
- GIVEN valid admin credentials configured via environment variables
- WHEN a user provides correct username and password
- THEN the system SHALL grant access to the dashboard

#### Scenario: invalid credentials
- GIVEN a user provides incorrect credentials
- WHEN they attempt to access the dashboard
- THEN the system SHALL return HTTP 401 and prompt for credentials

### Requirement: sidecar-token-auth
The system SHALL authenticate sidecar API requests separately from dashboard auth.

#### Scenario: sidecar uses token
- GIVEN a sidecar with a valid registration token
- WHEN it sends requests to `/api/ingest`
- THEN the system SHALL authenticate via the token (not Basic Auth)

### Requirement: credential-configuration
The system SHALL read auth credentials from environment variables.

#### Scenario: env var config
- GIVEN environment variables `DASHBOARD_USER` and `DASHBOARD_PASS` are set
- WHEN the backend starts
- THEN the system SHALL use those values for Basic Auth validation
