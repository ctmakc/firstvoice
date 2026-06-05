from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
import uuid

from src.database import get_db
from src.middleware.auth import get_current_user
from src.models.db_models import AuditLog, Recording, User
from src.models.schemas import AuditLogRead, RecordingRead

router = APIRouter()


def _require_admin(user: User) -> None:
    if user.role not in ("admin", "superadmin"):
        raise HTTPException(status_code=403, detail="Admin access required")


class BulkVisibilityPayload(BaseModel):
    recording_ids: List[uuid.UUID]
    visibility: str


@router.get("/audit-log", response_model=List[AuditLogRead])
async def get_audit_log(
    community_id: Optional[uuid.UUID] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)

    query = select(AuditLog).join(Recording, AuditLog.recording_id == Recording.id)

    if current_user.role != "superadmin":
        query = query.where(Recording.community_id == current_user.community_id)

    if community_id:
        if current_user.role != "superadmin" and current_user.community_id != community_id:
            raise HTTPException(status_code=403, detail="Not authorized for this community")
        query = query.where(Recording.community_id == community_id)

    query = query.order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/bulk-visibility", response_model=List[RecordingRead])
async def bulk_visibility(
    data: BulkVisibilityPayload,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _require_admin(current_user)

    result = await db.execute(
        select(Recording).where(Recording.id.in_(data.recording_ids))
    )
    recordings = result.scalars().all()

    updated: List[Recording] = []
    for rec in recordings:
        if current_user.role != "superadmin" and rec.community_id != current_user.community_id:
            raise HTTPException(status_code=403, detail="Not authorized for one or more recordings")

        old_value = {"visibility": rec.visibility}
        rec.visibility = data.visibility
        new_value = {"visibility": data.visibility}

        audit = AuditLog(
            id=uuid.uuid4(),
            recording_id=rec.id,
            user_id=current_user.id,
            action="visibility_change",
            old_value=old_value,
            new_value=new_value,
        )
        db.add(audit)
        updated.append(rec)

    await db.commit()
    for rec in updated:
        await db.refresh(rec)
    return updated
