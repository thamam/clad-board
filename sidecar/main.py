import asyncio
import json
import logging
import os
import sys
from collections import deque
from pathlib import Path

import httpx

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [sidecar] %(levelname)s %(message)s",
)
logger = logging.getLogger("sidecar")

# --- Configuration ---

DASHBOARD_URL = os.environ.get("DASHBOARD_URL", "").rstrip("/")
REGISTRATION_TOKEN = os.environ.get("REGISTRATION_TOKEN", "")
LOG_PATH = os.environ.get("LOG_PATH", "stdout")

REQUIRED_FIELDS = {"timestamp", "bot_id", "event_type", "payload"}
VALID_EVENT_TYPES = {"startup", "heartbeat", "message", "token_usage", "error"}
BUFFER_MAX = 1000
BATCH_SIZE = 50
FLUSH_INTERVAL = 5  # seconds
MAX_BACKOFF = 60  # seconds


def validate_config() -> None:
    if not DASHBOARD_URL:
        logger.error("DASHBOARD_URL is required")
        sys.exit(1)
    if not REGISTRATION_TOKEN:
        logger.error("REGISTRATION_TOKEN is required")
        sys.exit(1)


# --- Log parsing ---


def parse_line(line: str) -> dict | None:
    line = line.strip()
    if not line:
        return None
    try:
        data = json.loads(line)
    except json.JSONDecodeError:
        return None

    missing = REQUIRED_FIELDS - set(data.keys())
    if missing:
        logger.warning("Skipping line with missing fields: %s", missing)
        return None

    if data["event_type"] not in VALID_EVENT_TYPES:
        logger.warning("Unknown event_type: %s", data["event_type"])
        return None

    return data


# --- Event buffer and forwarding ---


class EventForwarder:
    def __init__(self) -> None:
        self.buffer: deque[dict] = deque(maxlen=BUFFER_MAX)
        self.client = httpx.AsyncClient(
            base_url=DASHBOARD_URL,
            headers={"Authorization": f"Bearer {REGISTRATION_TOKEN}"},
            timeout=10.0,
        )
        self.backoff = 1

    def add(self, event: dict) -> None:
        self.buffer.append(event)

    async def flush(self) -> None:
        if not self.buffer:
            return

        batch = []
        while self.buffer and len(batch) < BATCH_SIZE:
            batch.append(self.buffer.popleft())

        try:
            response = await self.client.post("/api/ingest", json=batch)
            response.raise_for_status()
            self.backoff = 1
            logger.info("Flushed %d events (accepted)", len(batch))
        except (httpx.HTTPError, httpx.ConnectError) as e:
            logger.warning("Failed to flush: %s. Retrying in %ds", e, self.backoff)
            # Put events back at the front of the buffer
            for event in reversed(batch):
                self.buffer.appendleft(event)
            await asyncio.sleep(self.backoff)
            self.backoff = min(self.backoff * 2, MAX_BACKOFF)

    async def flush_loop(self) -> None:
        while True:
            await self.flush()
            await asyncio.sleep(FLUSH_INTERVAL)

    async def close(self) -> None:
        await self.flush()
        await self.client.aclose()


# --- Log tailing ---


async def tail_file(path: str, forwarder: EventForwarder) -> None:
    from watchfiles import awatch, Change

    log_path = Path(path)

    # Read existing content from end of file
    if log_path.exists():
        with open(log_path) as f:
            f.seek(0, 2)  # Seek to end
            pos = f.tell()
    else:
        pos = 0
        logger.info("Waiting for log file: %s", path)
        while not log_path.exists():
            await asyncio.sleep(1)

    logger.info("Tailing file: %s", path)

    async for changes in awatch(log_path.parent):
        for change_type, changed_path in changes:
            if Path(changed_path) != log_path:
                continue
            if change_type != Change.modified:
                if change_type == Change.deleted:
                    logger.warning("Log file deleted, waiting for recreation")
                    pos = 0
                continue

            with open(log_path) as f:
                # Handle file truncation/rotation
                f.seek(0, 2)
                file_size = f.tell()
                if file_size < pos:
                    logger.info("File truncated, reading from beginning")
                    pos = 0

                f.seek(pos)
                for line in f:
                    event = parse_line(line)
                    if event:
                        forwarder.add(event)
                pos = f.tell()


async def tail_stdin(forwarder: EventForwarder) -> None:
    logger.info("Reading from stdin")
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)

    while True:
        line_bytes = await reader.readline()
        if not line_bytes:
            await asyncio.sleep(0.1)
            continue
        event = parse_line(line_bytes.decode())
        if event:
            forwarder.add(event)


# --- Main ---


async def main() -> None:
    validate_config()
    forwarder = EventForwarder()

    logger.info("Sidecar starting — dashboard=%s, log_path=%s", DASHBOARD_URL, LOG_PATH)

    flush_task = asyncio.create_task(forwarder.flush_loop())

    try:
        if LOG_PATH == "stdout":
            await tail_stdin(forwarder)
        else:
            await tail_file(LOG_PATH, forwarder)
    except asyncio.CancelledError:
        pass
    finally:
        flush_task.cancel()
        await forwarder.close()
        logger.info("Sidecar stopped")


if __name__ == "__main__":
    asyncio.run(main())
