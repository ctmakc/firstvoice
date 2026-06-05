from fastapi import Request, HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError
from typing import Optional
import uuid

from src.config import get_settings
from src.database import get_db
from src.models.db_models import User

settings = get_settings()


def _extract_auth_token(request: Request) -> tuple[Optional[str], Optional[str]]:
    """Return (method, token). Method is 'jwt' or 'elder_key'."""
    cookie = (
        request.cookies.get("next-auth.session-token")
        or request.cookies.get("__Secure-next-auth.session-token")
    )
    if cookie:
        return ("jwt", cookie)

    elder_key = request.headers.get("X-Elder-Key")
    if elder_key:
        return ("elder_key", elder_key)

    return (None, None)


async def _resolve_user(method: str, token: str, db: AsyncSession) -> Optional[User]:
    if method == "jwt":
        try:
            payload = jwt.decode(token, settings.nextauth_secret, algorithms=["HS256"])
        except JWTError:
            return None

        email = payload.get("email")
        sub = payload.get("sub")
        if email:
            result = await db.execute(select(User).where(User.email == email))
            user = result.scalar_one_or_none()
            if user:
                return user

        if sub:
            result = await db.execute(select(User).where(User.oauth_id == sub))
            user = result.scalar_one_or_none()
            if user:
                return user

        return None

    if method == "elder_key":
        result = await db.execute(select(User).where(User.elder_key_token == token))
        return result.scalar_one_or_none()

    return None


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> User:
    method, token = _extract_auth_token(request)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required",
        )

    user = await _resolve_user(method, token, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )
    return user


async def get_current_user_optional(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> Optional[User]:
    method, token = _extract_auth_token(request)
    if not token:
        return None
    try:
        return await _resolve_user(method, token, db)
    except Exception:
        return None
