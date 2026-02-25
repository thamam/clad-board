# Delta for dashboard-ui

## ADDED Requirements

### Requirement: overview-page
The system SHALL display an overview page as the default view.

#### Scenario: bot grid
- GIVEN registered bots exist
- WHEN the user navigates to the overview page
- THEN the system SHALL display a grid of bot cards
- AND each card SHALL show: name, class, status indicator, last heartbeat, message count, error count

#### Scenario: status indicator colors
- GIVEN a bot card on the overview page
- WHEN the bot status is `online`
- THEN the status indicator SHALL be green
- WHEN the bot status is `idle`
- THEN the status indicator SHALL be yellow
- WHEN the bot status is `offline`
- THEN the status indicator SHALL be red

#### Scenario: empty state
- GIVEN no bots are registered
- WHEN the user views the overview page
- THEN the system SHALL display a message prompting bot registration

### Requirement: bot-detail-page
The system SHALL display a detail page for each bot.

#### Scenario: identity section
- GIVEN a bot with startup data
- WHEN the user navigates to the bot detail page
- THEN the system SHALL display: name, class, version, uptime

#### Scenario: configuration section
- GIVEN a bot with startup configuration
- WHEN the user views the configuration section
- THEN the system SHALL display: models, channels, skills, and tools with enabled/disabled badges

#### Scenario: activity section
- GIVEN a bot with message events
- WHEN the user views the activity section
- THEN the system SHALL display: messages in count, messages out count, last message timestamp

#### Scenario: token usage table
- GIVEN a bot with token_usage events
- WHEN the user views the token usage section
- THEN the system SHALL display a table with columns: Model, Tokens In, Tokens Out
- AND rows segmented by: All Time, Last 24h, Month-to-Date

#### Scenario: errors section
- GIVEN a bot with error events
- WHEN the user views the errors section
- THEN the system SHALL display: error count, last error message, last error timestamp

### Requirement: polling
The system SHALL poll the API at a regular interval to refresh data.

#### Scenario: auto-refresh
- GIVEN the dashboard is open
- WHEN the polling interval elapses (e.g., 10 seconds)
- THEN the system SHALL fetch updated data from the API
- AND update the UI without full page reload

### Requirement: navigation
The system SHALL support navigation between overview and bot detail pages.

#### Scenario: navigate to detail
- GIVEN the overview page is displayed
- WHEN the user clicks a bot card
- THEN the system SHALL navigate to that bot's detail page

#### Scenario: navigate back
- GIVEN the bot detail page is displayed
- WHEN the user clicks the back/overview link
- THEN the system SHALL navigate to the overview page
