from datetime import datetime, timezone
from typing import Optional
from uuid import uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel, JSON, Column


def utcnow() -> datetime:
    """Return current UTC time as a naive datetime (no tzinfo).

    SQLite strips timezone info on storage, so we store naive-UTC consistently
    to avoid aware-vs-naive comparison errors on read-back.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Bot(SQLModel, table=True):
    __tablename__ = "bots"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    name: str
    bot_class: str
    token_hash: str
    registered_at: datetime = Field(default_factory=utcnow)
    status: str = Field(default="active")
    last_heartbeat: Optional[datetime] = None
    last_startup: Optional[dict] = Field(default=None, sa_column=Column(JSON))


class Event(SQLModel, table=True):
    __tablename__ = "events"

    id: Optional[int] = Field(default=None, primary_key=True)
    bot_id: str = Field(foreign_key="bots.id", index=True)
    event_type: str = Field(index=True)
    payload: dict = Field(sa_column=Column(JSON))
    timestamp: datetime
    received_at: datetime = Field(default_factory=utcnow)


class TokenAggregate(SQLModel, table=True):
    __tablename__ = "token_aggregates"

    id: Optional[int] = Field(default=None, primary_key=True)
    bot_id: str = Field(foreign_key="bots.id", index=True)
    model: str
    tokens_in_total: int = Field(default=0)
    tokens_out_total: int = Field(default=0)
    updated_at: datetime = Field(default_factory=utcnow)


class ChannelStatus(SQLModel, table=True):
    __tablename__ = "channel_statuses"
    __table_args__ = (UniqueConstraint("bot_id", "channel_name"),)
    id: Optional[int] = Field(default=None, primary_key=True)
    bot_id: str = Field(foreign_key="bots.id", index=True)
    channel_name: str
    status: str = Field(default="connected")  # connected | disconnected | error
    error_message: Optional[str] = None
    last_status_change: datetime = Field(default_factory=utcnow)
    last_seen: datetime = Field(default_factory=utcnow)


# --- Pydantic schemas for API requests/responses ---

class BotRegisterRequest(SQLModel):
    name: str
    bot_class: str


class BotRegisterResponse(SQLModel):
    bot_id: str
    name: str
    token: str


class IngestEvent(SQLModel):
    timestamp: str
    bot_id: str
    event_type: str
    payload: dict


class IngestRequest(SQLModel):
    events: list[IngestEvent]


class BotSummary(SQLModel):
    id: str
    name: str
    bot_class: str
    status: str
    registered_at: datetime
    last_heartbeat: Optional[datetime] = None
    computed_status: str = "offline"
    message_count: int = 0
    error_count: int = 0
    channels_up: int = 0
    channels_total: int = 0


class TokenUsageSegment(SQLModel):
    model: str
    tokens_in: int
    tokens_out: int


class TokenUsageDetail(SQLModel):
    model: str
    all_time_in: int = 0
    all_time_out: int = 0
    last_24h_in: int = 0
    last_24h_out: int = 0
    mtd_in: int = 0
    mtd_out: int = 0


class ChannelStatusResponse(SQLModel):
    channel_name: str
    status: str
    error_message: Optional[str] = None
    last_status_change: datetime
    last_seen: datetime


class BotDetail(SQLModel):
    id: str
    name: str
    bot_class: str
    status: str
    registered_at: datetime
    last_heartbeat: Optional[datetime] = None
    computed_status: str = "offline"
    # Configuration (from last startup)
    version: Optional[str] = None
    uptime_seconds: Optional[int] = None
    models: list[str] = []
    channels: list[str] = []
    channel_statuses: list[ChannelStatusResponse] = []
    skills: list[str] = []
    tools: list[dict] = []
    # Activity
    messages_in: int = 0
    messages_out: int = 0
    last_message_at: Optional[datetime] = None
    # Token usage
    token_usage: list[TokenUsageDetail] = []
    # Errors
    error_count: int = 0
    last_error_message: Optional[str] = None
    last_error_at: Optional[datetime] = None
