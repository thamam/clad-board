from datetime import datetime

from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from backend.auth import require_bot_token
from backend.database import get_session
from backend.models import Bot, Event, IngestEvent, TokenAggregate, utcnow

router = APIRouter(prefix="/api", tags=["ingestion"])


def _process_event(event: IngestEvent, bot: Bot, session: Session) -> None:
    db_event = Event(
        bot_id=bot.id,
        event_type=event.event_type,
        payload=event.payload,
        timestamp=datetime.fromisoformat(event.timestamp).replace(tzinfo=None),
    )
    session.add(db_event)

    if event.event_type == "heartbeat":
        bot.last_heartbeat = utcnow()
        session.add(bot)

    elif event.event_type == "startup":
        bot.last_startup = event.payload
        session.add(bot)

    elif event.event_type == "token_usage":
        model_name = event.payload.get("model", "unknown")
        tokens_in = event.payload.get("tokens_in", 0)
        tokens_out = event.payload.get("tokens_out", 0)

        agg = session.exec(
            select(TokenAggregate).where(
                TokenAggregate.bot_id == bot.id,
                TokenAggregate.model == model_name,
            )
        ).first()

        if agg:
            agg.tokens_in_total += tokens_in
            agg.tokens_out_total += tokens_out
            agg.updated_at = utcnow()
        else:
            agg = TokenAggregate(
                bot_id=bot.id,
                model=model_name,
                tokens_in_total=tokens_in,
                tokens_out_total=tokens_out,
            )
        session.add(agg)


@router.post("/ingest")
def ingest_events(
    events: list[IngestEvent],
    bot: Bot = Depends(require_bot_token),
    session: Session = Depends(get_session),
) -> dict:
    accepted = 0
    for event in events:
        _process_event(event, bot, session)
        accepted += 1
    session.commit()
    return {"accepted": accepted}
