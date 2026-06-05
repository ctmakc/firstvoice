from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.schemas import CommunityCreate, CommunityRead
from src.models.db_models import Community
import uuid
from typing import List

router = APIRouter()


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
