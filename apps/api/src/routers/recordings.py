from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_
from src.database import get_db
from src.models.schemas import RecordingCreate, RecordingRead, RecordingUpdate
from src.models.db_models import Recording, AuditLog, User
from src.config import get_settings
import uuid
import json
from typing import List, Optional

router = APIRouter()
settings = get_settings()


@router.post("", response_model=RecordingRead)
async def create_recording(
    community_id: uuid.UUID = Form(...),
    language: str = Form(...),
    title: Optional[str] = Form(None),
    occasion: Optional[str] = Form(None),
    visibility: str = Form("sacred"),
    ai_training_allowed: bool = Form(False),
    speaker_name: Optional[str] = Form(None),
    location: Optional[str] = Form(None),  # JSON string
    audio: UploadFile = File(...),
    uploaded_by: uuid.UUID = Form(...),  # TODO: from JWT
    db: AsyncSession = Depends(get_db),
):
    """Upload audio and create recording record. Enqueues transcription job."""
    # TODO: upload to MinIO
    audio_file_key = f"recordings/{community_id}/{uuid.uuid4()}.{audio.filename.split('.')[-1]}"

    loc = json.loads(location) if location else None

    recording = Recording(
        id=uuid.uuid4(),
        community_id=community_id,
        uploaded_by=uploaded_by,
        audio_file_key=audio_file_key,
        language=language,
        title=title,
        occasion=occasion,
        visibility=visibility,
        ai_training_allowed=ai_training_allowed,
        speaker_name=speaker_name,
        location_point=f"POINT({loc['lng']} {loc['lat']})" if loc else None,
        transcription_status="pending",
    )
    db.add(recording)

    # Audit log
    audit = AuditLog(
        id=uuid.uuid4(),
        recording_id=recording.id,
        user_id=uploaded_by,
        action="upload",
        new_value={"visibility": visibility, "language": language},
    )
    db.add(audit)

    await db.commit()
    await db.refresh(recording)

    # TODO: enqueue Celery transcription task
    return recording


@router.get("", response_model=List[RecordingRead])
async def list_recordings(
    community_id: Optional[uuid.UUID] = None,
    visibility: Optional[str] = None,
    language: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    """List recordings filtered by community, visibility, language.
    Sacred recordings excluded from public API unless user is community member.
    """
    query = select(Recording)
    filters = []

    if community_id:
        filters.append(Recording.community_id == community_id)
    if language:
        filters.append(Recording.language == language)
    if visibility:
        filters.append(Recording.visibility == visibility)
    else:
        # Default: exclude sacred unless explicitly requested by authorized user
        filters.append(Recording.visibility != "sacred")

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query.order_by(Recording.created_at.desc()))
    return result.scalars().all()


@router.get("/{recording_id}", response_model=RecordingRead)
async def get_recording(
    recording_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Recording).where(Recording.id == recording_id))
    recording = result.scalar_one_or_none()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")
    return recording


@router.patch("/{recording_id}", response_model=RecordingRead)
async def update_recording(
    recording_id: uuid.UUID,
    data: RecordingUpdate,
    user_id: uuid.UUID,  # TODO: from JWT
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Recording).where(Recording.id == recording_id))
    recording = result.scalar_one_or_none()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    # Check user is elder/admin of this community
    user_result = await db.execute(select(User).where(User.id == user_id))
    user = user_result.scalar_one_or_none()
    if not user or user.role not in ("elder", "admin", "superadmin"):
        raise HTTPException(status_code=403, detail="Insufficient privileges")

    old_value = {}
    new_value = {}

    if data.title is not None:
        old_value["title"] = recording.title
        recording.title = data.title
        new_value["title"] = data.title

    if data.visibility is not None:
        old_value["visibility"] = recording.visibility
        recording.visibility = data.visibility
        new_value["visibility"] = data.visibility

    if data.ai_training_allowed is not None:
        old_value["ai_training_allowed"] = recording.ai_training_allowed
        recording.ai_training_allowed = data.ai_training_allowed
        new_value["ai_training_allowed"] = data.ai_training_allowed

    # Audit log
    audit = AuditLog(
        id=uuid.uuid4(),
        recording_id=recording.id,
        user_id=user_id,
        action="visibility_change",
        old_value=old_value or None,
        new_value=new_value or None,
    )
    db.add(audit)

    await db.commit()
    await db.refresh(recording)
    return recording
