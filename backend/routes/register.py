from fastapi import APIRouter, Depends
from sqlmodel import Session

from backend.auth import generate_token, hash_token, require_basic_auth
from backend.database import get_session
from backend.models import Bot, BotRegisterRequest, BotRegisterResponse

router = APIRouter(prefix="/api", tags=["registration"])


@router.post("/register", response_model=BotRegisterResponse)
def register_bot(
    request: BotRegisterRequest,
    session: Session = Depends(get_session),
    _user: str = Depends(require_basic_auth),
) -> BotRegisterResponse:
    raw_token = generate_token()
    bot = Bot(
        name=request.name,
        bot_class=request.bot_class,
        token_hash=hash_token(raw_token),
    )
    session.add(bot)
    session.commit()
    session.refresh(bot)

    return BotRegisterResponse(
        bot_id=bot.id,
        name=bot.name,
        token=raw_token,
    )
