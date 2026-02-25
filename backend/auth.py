import os
import secrets

import bcrypt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials, HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select

from backend.database import get_session
from backend.models import Bot

basic_security = HTTPBasic()
bearer_security = HTTPBearer()

DASHBOARD_USER = os.environ.get("DASHBOARD_USER", "admin")
DASHBOARD_PASS = os.environ.get("DASHBOARD_PASS", "changeme")


def hash_token(token: str) -> str:
    return bcrypt.hashpw(token.encode(), bcrypt.gensalt()).decode()


def verify_token(token: str, token_hash: str) -> bool:
    return bcrypt.checkpw(token.encode(), token_hash.encode())


def generate_token() -> str:
    return secrets.token_urlsafe(32)


def require_basic_auth(
    credentials: HTTPBasicCredentials = Depends(basic_security),
) -> str:
    if not (
        secrets.compare_digest(credentials.username.encode(), DASHBOARD_USER.encode())
        and secrets.compare_digest(credentials.password.encode(), DASHBOARD_PASS.encode())
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def require_bot_token(
    credentials: HTTPAuthorizationCredentials = Security(bearer_security),
    session: Session = Depends(get_session),
) -> Bot:
    token = credentials.credentials
    bots = session.exec(select(Bot)).all()
    for bot in bots:
        if verify_token(token, bot.token_hash):
            if bot.status != "active":
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Bot is inactive",
                )
            return bot
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token",
    )
