from datetime import timedelta

from sqlmodel import Session, func, select

from backend.models import Event, TokenAggregate, TokenUsageDetail, utcnow


def get_token_usage_detail(bot_id: str, session: Session) -> list[TokenUsageDetail]:
    # All-time from pre-computed aggregates
    aggregates = session.exec(
        select(TokenAggregate).where(TokenAggregate.bot_id == bot_id)
    ).all()

    if not aggregates:
        return []

    now = utcnow()
    twenty_four_h_ago = now - timedelta(hours=24)
    month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    results = []
    for agg in aggregates:
        # Last 24h from events table
        last_24h = session.exec(
            select(
                func.coalesce(func.sum(Event.payload["tokens_in"].as_integer()), 0),
                func.coalesce(func.sum(Event.payload["tokens_out"].as_integer()), 0),
            ).where(
                Event.bot_id == bot_id,
                Event.event_type == "token_usage",
                Event.payload["model"].as_string() == agg.model,
                Event.timestamp >= twenty_four_h_ago,
            )
        ).one()

        # Month-to-date from events table
        mtd = session.exec(
            select(
                func.coalesce(func.sum(Event.payload["tokens_in"].as_integer()), 0),
                func.coalesce(func.sum(Event.payload["tokens_out"].as_integer()), 0),
            ).where(
                Event.bot_id == bot_id,
                Event.event_type == "token_usage",
                Event.payload["model"].as_string() == agg.model,
                Event.timestamp >= month_start,
            )
        ).one()

        results.append(
            TokenUsageDetail(
                model=agg.model,
                all_time_in=agg.tokens_in_total,
                all_time_out=agg.tokens_out_total,
                last_24h_in=last_24h[0],
                last_24h_out=last_24h[1],
                mtd_in=mtd[0],
                mtd_out=mtd[1],
            )
        )

    return results
