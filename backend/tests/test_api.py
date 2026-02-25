from datetime import datetime, timezone


def test_register_bot(client, basic_auth):
    response = client.post(
        "/api/register",
        json={"name": "Test Bot", "bot_class": "openclaw"},
        auth=basic_auth,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Bot"
    assert "bot_id" in data
    assert "token" in data


def test_register_requires_auth(client):
    response = client.post(
        "/api/register",
        json={"name": "Test Bot", "bot_class": "openclaw"},
    )
    assert response.status_code == 401


def test_register_wrong_auth(client):
    response = client.post(
        "/api/register",
        json={"name": "Test Bot", "bot_class": "openclaw"},
        auth=("wrong", "credentials"),
    )
    assert response.status_code == 401


def test_list_bots_empty(client, basic_auth):
    response = client.get("/api/bots", auth=basic_auth)
    assert response.status_code == 200
    assert response.json() == []


def test_list_bots_after_register(client, basic_auth):
    client.post(
        "/api/register",
        json={"name": "Bot A", "bot_class": "openclaw"},
        auth=basic_auth,
    )
    response = client.get("/api/bots", auth=basic_auth)
    assert response.status_code == 200
    bots = response.json()
    assert len(bots) == 1
    assert bots[0]["name"] == "Bot A"
    assert bots[0]["computed_status"] == "offline"


def test_ingest_events(client, basic_auth):
    # Register a bot
    reg = client.post(
        "/api/register",
        json={"name": "Ingest Bot", "bot_class": "openclaw"},
        auth=basic_auth,
    ).json()
    token = reg["token"]
    bot_id = reg["bot_id"]

    # Ingest heartbeat
    now = datetime.now(timezone.utc).isoformat()
    response = client.post(
        "/api/ingest",
        json=[
            {
                "timestamp": now,
                "bot_id": bot_id,
                "event_type": "heartbeat",
                "payload": {"uptime_seconds": 100},
            }
        ],
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["accepted"] == 1


def test_ingest_invalid_token(client):
    response = client.post(
        "/api/ingest",
        json=[
            {
                "timestamp": "2026-01-01T00:00:00Z",
                "bot_id": "fake",
                "event_type": "heartbeat",
                "payload": {},
            }
        ],
        headers={"Authorization": "Bearer invalidtoken"},
    )
    assert response.status_code == 401


def test_bot_detail(client, basic_auth):
    # Register
    reg = client.post(
        "/api/register",
        json={"name": "Detail Bot", "bot_class": "letta"},
        auth=basic_auth,
    ).json()
    token = reg["token"]
    bot_id = reg["bot_id"]

    # Ingest startup + message + token_usage
    now = datetime.now(timezone.utc).isoformat()
    events = [
        {
            "timestamp": now,
            "bot_id": bot_id,
            "event_type": "startup",
            "payload": {
                "version": "1.0.0",
                "models": ["gemini-2.5-flash"],
                "channels": ["telegram"],
                "skills": ["summarize"],
                "tools": [{"name": "calc", "enabled": True}],
            },
        },
        {
            "timestamp": now,
            "bot_id": bot_id,
            "event_type": "message",
            "payload": {"direction": "in", "channel": "telegram"},
        },
        {
            "timestamp": now,
            "bot_id": bot_id,
            "event_type": "token_usage",
            "payload": {"model": "gemini-2.5-flash", "tokens_in": 100, "tokens_out": 50},
        },
    ]
    client.post(
        "/api/ingest",
        json=events,
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get detail
    response = client.get(f"/api/bots/{bot_id}", auth=basic_auth)
    assert response.status_code == 200
    detail = response.json()
    assert detail["name"] == "Detail Bot"
    assert detail["bot_class"] == "letta"
    assert detail["version"] == "1.0.0"
    assert detail["messages_in"] == 1
    assert len(detail["token_usage"]) == 1
    assert detail["token_usage"][0]["model"] == "gemini-2.5-flash"
    assert detail["token_usage"][0]["all_time_in"] == 100


def test_bot_detail_not_found(client, basic_auth):
    response = client.get("/api/bots/nonexistent", auth=basic_auth)
    assert response.status_code == 404


def test_heartbeat_updates_status_to_online(client, basic_auth, session):
    """Regression: status computation must work after DB round-trip.

    SQLite strips timezone info, so datetimes must be stored as naive-UTC
    to avoid TypeError when comparing with utcnow().
    """
    reg = client.post(
        "/api/register",
        json={"name": "Heartbeat Bot", "bot_class": "openclaw"},
        auth=basic_auth,
    ).json()
    token = reg["token"]
    bot_id = reg["bot_id"]

    # Ingest heartbeat
    now = datetime.now(timezone.utc).isoformat()
    client.post(
        "/api/ingest",
        json=[{
            "timestamp": now,
            "bot_id": bot_id,
            "event_type": "heartbeat",
            "payload": {"uptime_seconds": 60},
        }],
        headers={"Authorization": f"Bearer {token}"},
    )

    # Force a fresh load from DB (evict cached objects)
    session.expire_all()

    # List bots — this triggers _compute_status with DB-loaded last_heartbeat
    response = client.get("/api/bots", auth=basic_auth)
    assert response.status_code == 200
    bots = response.json()
    bot = next(b for b in bots if b["id"] == bot_id)
    assert bot["computed_status"] == "online"
