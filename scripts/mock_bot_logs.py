"""Generate mock bot log lines for end-to-end testing.

Usage:
    python scripts/mock_bot_logs.py > logs/bot.log

Generates a realistic sequence of bot events: startup, heartbeats,
messages, token_usage, and an occasional error.
"""

import json
import sys
import time
from datetime import datetime, timezone
from uuid import uuid4

BOT_ID = sys.argv[1] if len(sys.argv) > 1 else str(uuid4())


def emit(event_type: str, payload: dict) -> None:
    line = json.dumps({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "bot_id": BOT_ID,
        "event_type": event_type,
        "payload": payload,
    })
    print(line, flush=True)


def main() -> None:
    print(f"# Mock bot logs for bot_id={BOT_ID}", file=sys.stderr)

    # Startup event
    emit("startup", {
        "version": "1.2.0",
        "models": ["gemini-2.5-flash", "claude-sonnet-4-6"],
        "channels": ["telegram", "whatsapp"],
        "skills": ["summarize", "web_search"],
        "tools": [
            {"name": "calculator", "enabled": True},
            {"name": "code_runner", "enabled": False},
        ],
    })

    # Initial channel statuses — both connected
    emit("channel_status", {"channel_name": "telegram", "status": "connected"})
    emit("channel_status", {"channel_name": "whatsapp", "status": "connected"})

    uptime = 0
    msg_count = 0

    while True:
        time.sleep(5)
        uptime += 5

        # Heartbeat every cycle
        emit("heartbeat", {"uptime_seconds": uptime})

        # Simulate incoming message
        if msg_count % 3 == 0:
            emit("message", {"direction": "in", "channel": "telegram", "session_id": "sess-001"})
            emit("token_usage", {"model": "gemini-2.5-flash", "tokens_in": 256, "tokens_out": 128})
            emit("message", {"direction": "out", "channel": "telegram", "session_id": "sess-001"})

        # Occasional error
        if msg_count % 10 == 7:
            emit("error", {"message": "Connection timeout to Telegram API", "severity": "warning"})

        # Simulate whatsapp disconnect/reconnect cycle
        if msg_count % 12 == 8:
            emit("channel_status", {"channel_name": "whatsapp", "status": "disconnected", "error_message": "Connection closed by peer"})
        if msg_count % 12 == 10:
            emit("channel_status", {"channel_name": "whatsapp", "status": "connected"})

        msg_count += 1


if __name__ == "__main__":
    main()
