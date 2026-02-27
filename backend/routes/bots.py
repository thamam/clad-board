from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, func, select

from backend.aggregation import get_token_usage_detail
from backend.auth import require_basic_auth
from backend.database import get_session
from backend.models import Bot, BotDetail, BotSummary, ChannelStatus, ChannelStatusResponse, Event, utcnow

router = APIRouter(prefix="/api", tags=["bots"])


def _compute_status(last_heartbeat: datetime | None) -> str:
    if last_heartbeat is None:
        return "offline"
    now = utcnow()
    delta = (now - last_heartbeat).total_seconds()
    if delta <= 120:
        return "online"
    if delta <= 600:
        return "idle"
    return "offline"


@router.get("/bots", response_model=list[BotSummary])
def list_bots(
    session: Session = Depends(get_session),
    _user: str = Depends(require_basic_auth),
) -> list[BotSummary]:
    bots = session.exec(select(Bot)).all()
    result = []
    for bot in bots:
        msg_count = session.exec(
            select(func.count(Event.id)).where(
                Event.bot_id == bot.id, Event.event_type == "message"
            )
        ).one()
        err_count = session.exec(
            select(func.count(Event.id)).where(
                Event.bot_id == bot.id, Event.event_type == "error"
            )
        ).one()

        channel_records = session.exec(
            select(ChannelStatus).where(ChannelStatus.bot_id == bot.id)
        ).all()
        channels_total = len(channel_records)
        channels_up = sum(1 for ch in channel_records if ch.status == "connected")

        result.append(
            BotSummary(
                id=bot.id,
                name=bot.name,
                bot_class=bot.bot_class,
                status=bot.status,
                registered_at=bot.registered_at,
                last_heartbeat=bot.last_heartbeat,
                computed_status=_compute_status(bot.last_heartbeat),
                message_count=msg_count,
                error_count=err_count,
                channels_up=channels_up,
                channels_total=channels_total,
            )
        )
    return result


@router.get("/bots/{bot_id}", response_model=BotDetail)
def get_bot_detail(
    bot_id: str,
    session: Session = Depends(get_session),
    _user: str = Depends(require_basic_auth),
) -> BotDetail:
    bot = session.get(Bot, bot_id)
    if not bot:
        raise HTTPException(status_code=404, detail="Bot not found")

    # Message counts
    messages_in = session.exec(
        select(func.count(Event.id)).where(
            Event.bot_id == bot_id,
            Event.event_type == "message",
            Event.payload["direction"].as_string() == "in",
        )
    ).one()
    messages_out = session.exec(
        select(func.count(Event.id)).where(
            Event.bot_id == bot_id,
            Event.event_type == "message",
            Event.payload["direction"].as_string() == "out",
        )
    ).one()

    # Last message timestamp
    last_msg = session.exec(
        select(Event.timestamp)
        .where(Event.bot_id == bot_id, Event.event_type == "message")
        .order_by(Event.timestamp.desc())
        .limit(1)
    ).first()

    # Error info
    error_count = session.exec(
        select(func.count(Event.id)).where(
            Event.bot_id == bot_id, Event.event_type == "error"
        )
    ).one()
    last_error = session.exec(
        select(Event)
        .where(Event.bot_id == bot_id, Event.event_type == "error")
        .order_by(Event.timestamp.desc())
        .limit(1)
    ).first()

    # Uptime from last heartbeat
    last_hb = session.exec(
        select(Event)
        .where(Event.bot_id == bot_id, Event.event_type == "heartbeat")
        .order_by(Event.timestamp.desc())
        .limit(1)
    ).first()
    uptime = last_hb.payload.get("uptime_seconds") if last_hb else None

    # Configuration from last startup
    startup = bot.last_startup or {}

    # Token usage
    token_usage = get_token_usage_detail(bot_id, session)

    # Channel statuses
    channel_records = session.exec(
        select(ChannelStatus).where(ChannelStatus.bot_id == bot_id)
    ).all()
    channel_statuses = [
        ChannelStatusResponse(
            channel_name=ch.channel_name,
            status=ch.status,
            error_message=ch.error_message,
            last_status_change=ch.last_status_change,
            last_seen=ch.last_seen,
        )
        for ch in channel_records
    ]

    return BotDetail(
        id=bot.id,
        name=bot.name,
        bot_class=bot.bot_class,
        status=bot.status,
        registered_at=bot.registered_at,
        last_heartbeat=bot.last_heartbeat,
        computed_status=_compute_status(bot.last_heartbeat),
        version=startup.get("version"),
        uptime_seconds=uptime,
        models=startup.get("models", []),
        channels=startup.get("channels", []),
        channel_statuses=channel_statuses,
        skills=startup.get("skills", []),
        tools=startup.get("tools", []),
        messages_in=messages_in,
        messages_out=messages_out,
        last_message_at=last_msg,
        token_usage=token_usage,
        error_count=error_count,
        last_error_message=last_error.payload.get("message") if last_error else None,
        last_error_at=last_error.timestamp if last_error else None,
    )
