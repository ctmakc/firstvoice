from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from src.models.schemas import UserCreate, UserRead
from src.models.db_models import User
from src.middleware.auth import get_current_user
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
            # Never trust a client-supplied role: new users always start as
            # viewers. Role changes happen only through authenticated admin paths.
            role="viewer",
            oauth_provider=data.oauth_provider,
            oauth_id=data.oauth_id,
        )
        db.add(user)

    await db.commit()
    await db.refresh(user)
    return user


@router.get("/me", response_model=UserRead)
async def get_me(
    current_user: User = Depends(get_current_user),
):
    """Get the current user, resolved from the session cookie or X-Elder-Key."""
    return current_user


@router.post("/elder-key")
async def generate_elder_key(
    user_id: uuid.UUID,
    community_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Generate an opaque Elder Key for community council members.

    Only admins may issue Elder Keys, and only for their own community
    (superadmins may issue for any community).
    """
    if current_user.role not in ("admin", "superadmin"):
        raise HTTPException(status_code=403, detail="Admin privileges required")
    if current_user.role != "superadmin" and current_user.community_id != community_id:
        raise HTTPException(status_code=403, detail="Not authorized for this community")

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
