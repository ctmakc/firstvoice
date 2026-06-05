from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.schemas import UserCreate, UserRead
from src.models.db_models import User
from sqlalchemy import select
import uuid

router = APIRouter()


@router.post("/callback", response_model=UserRead)
async def oauth_callback(
    data: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """Create or update user after OAuth login."""
    result = await db.execute(
        select(User).where(
            User.oauth_provider == data.oauth_provider,
            User.oauth_id == data.oauth_id,
        )
    )
    user = result.scalar_one_or_none()

    if user:
        # Update existing
        user.name = data.name or user.name
        user.email = data.email or user.email
    else:
        user = User(
            id=uuid.uuid4(),
            email=data.email,
            name=data.name,
            role=data.role,
            oauth_provider=data.oauth_provider,
            oauth_id=data.oauth_id,
        )
        db.add(user)

    await db.commit()
    await db.refresh(user)
    return user


@router.get("/me", response_model=UserRead)
async def get_me(
    request: Request,
    email: str = "",
    db: AsyncSession = Depends(get_db),
):
    """Get current user. Supports email query param or X-Elder-Key header."""
    elder_key = request.headers.get("X-Elder-Key")
    if elder_key:
        result = await db.execute(select(User).where(User.elder_key_token == elder_key))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="Invalid Elder Key")
        return user

    if email:
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    raise HTTPException(status_code=401, detail="Authentication required")


@router.post("/elder-key")
async def generate_elder_key(
    user_id: uuid.UUID,
    community_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Generate an opaque Elder Key for community council members."""
    import secrets
    token = secrets.token_urlsafe(32)

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.elder_key_token = token
    user.community_id = community_id
    user.role = "elder"
    await db.commit()

    return {"elder_key": token, "community_id": community_id}
