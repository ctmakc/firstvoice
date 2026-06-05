from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.schemas import CommunityCreate, CommunityRead, UserRead
from src.models.db_models import Community, User
from src.middleware.auth import get_current_user
import uuid
from typing import List

router = APIRouter()


def _require_community_admin(current_user: User, community_id: uuid.UUID) -> None:
    if current_user.role not in ("admin", "superadmin"):
        raise HTTPException(status_code=403, detail="Admin access required")
    if current_user.role != "superadmin" and current_user.community_id != community_id:
        raise HTTPException(status_code=403, detail="Not your community")


@router.post("", response_model=CommunityRead)
async def create_community(
    data: CommunityCreate,
    db: AsyncSession = Depends(get_db),
):
    community = Community(
        id=uuid.uuid4(),
        name=data.name,
        slug=data.slug,
        languages=data.languages,
        data_policy=data.data_policy,
    )
    db.add(community)
    await db.commit()
    await db.refresh(community)
    return community


@router.get("", response_model=List[CommunityRead])
async def list_communities(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Community))
    return result.scalars().all()


@router.get("/{community_id}", response_model=CommunityRead)
async def get_community(
    community_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Community).where(Community.id == community_id))
    community = result.scalar_one_or_none()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    return community


class InvitePayload(BaseModel):
    email: str
    role: str = "viewer"


@router.post("/{community_id}/invite")
async def invite_member(
    community_id: uuid.UUID,
    data: InvitePayload,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_community_admin(current_user, community_id)

    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()
    if user:
        user.community_id = community_id
        user.role = data.role
    else:
        user = User(
            id=uuid.uuid4(),
            email=data.email,
            role=data.role,
            community_id=community_id,
        )
        db.add(user)

    await db.commit()
    await db.refresh(user)
    return {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
        "community_id": community_id,
    }


@router.get("/{community_id}/members", response_model=List[UserRead])
async def list_members(
    community_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_community_admin(current_user, community_id)
    result = await db.execute(select(User).where(User.community_id == community_id))
    return result.scalars().all()


@router.patch("/{community_id}/policy", response_model=CommunityRead)
async def update_policy(
    community_id: uuid.UUID,
    data_policy: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_community_admin(current_user, community_id)
    result = await db.execute(select(Community).where(Community.id == community_id))
    community = result.scalar_one_or_none()
    if not community:
        raise HTTPException(status_code=404, detail="Community not found")
    community.data_policy = data_policy
    await db.commit()
    await db.refresh(community)
    return community
