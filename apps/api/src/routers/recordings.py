from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.database import get_db
from src.models.schemas import RecordingCreate, RecordingRead, RecordingUpdate
from src.models.db_models import Recording, AuditLog, User
from src.middleware.auth import get_current_user, get_current_user_optional
from src.middleware.policy import require_recording_access
from src.services.storage import upload_audio, get_presigned_url
from src.config import get_settings
import uuid
import json
import io
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
    location: Optional[str] = Form(None),
    audio: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Validate file type
    allowed_types = {"audio/webm", "audio/wav", "audio/mpeg", "audio/mp4", "audio/ogg", "audio/flac"}
    if audio.content_type and audio.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported audio format: {audio.content_type}. Allowed: {', '.join(allowed_types)}"
        )

    content = await audio.read()

    # Validate file size
    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(
            status_code=413,
            detail=f"File too large: {len(content)} bytes. Maximum: {settings.max_upload_size_mb}MB"
        )

    ext = audio.filename.split(".")[-1] if audio.filename and "." in audio.filename else "webm"
    audio_file_key = f"recordings/{community_id}/{uuid.uuid4()}.{ext}"

    upload_audio(
        audio_file_key,
        io.BytesIO(content),
        len(content),
        content_type=audio.content_type or "audio/webm",
    )

    loc = json.loads(location) if location else None

    recording = Recording(
        id=uuid.uuid4(),
        community_id=community_id,
        uploaded_by=current_user.id,
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

    audit = AuditLog(
        id=uuid.uuid4(),
        recording_id=recording.id,
        user_id=current_user.id,
        action="upload",
        new_value={"visibility": visibility, "language": language},
    )
    db.add(audit)

    await db.commit()
    await db.refresh(recording)
    return recording


@router.get("", response_model=List[RecordingRead])
async def list_recordings(
    community_id: Optional[uuid.UUID] = None,
    visibility: Optional[str] = None,
    language: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user_optional),
):
    query = select(Recording)
    filters = []

    if community_id:
        filters.append(Recording.community_id == community_id)
    if language:
        filters.append(Recording.language == language)
    if visibility:
        filters.append(Recording.visibility == visibility)
    else:
        can_view_sacred = False
        if community_id and current_user:
            if current_user.role == "superadmin":
                can_view_sacred = True
            elif (
                current_user.community_id == community_id
                and current_user.role in ("elder", "admin", "superadmin")
            ):
                can_view_sacred = True
        if not can_view_sacred:
            filters.append(Recording.visibility != "sacred")

    if filters:
        query = query.where(and_(*filters))

    result = await db.execute(query.order_by(Recording.created_at.desc()))
    return result.scalars().all()


@router.get("/{recording_id}", response_model=RecordingRead)
async def get_recording(
    recording: Recording = Depends(require_recording_access),
):
    return recording


@router.get("/{recording_id}/audio-url")
async def get_audio_url(
    recording: Recording = Depends(require_recording_access),
):
    url = get_presigned_url(recording.audio_file_key, expiry=3600)
    return {"audio_url": url}


@router.patch("/{recording_id}", response_model=RecordingRead)
async def update_recording(
    recording_id: uuid.UUID,
    data: RecordingUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    recording: Recording = Depends(require_recording_access),
):
    if current_user.role not in ("elder", "admin", "superadmin"):
        raise HTTPException(status_code=403, detail="Insufficient privileges")
    if current_user.role != "superadmin" and current_user.community_id != recording.community_id:
        raise HTTPException(status_code=403, detail="Not authorized for this community")

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

    if data.transcript is not None:
        old_value["transcript"] = recording.transcript
        recording.transcript = data.transcript
        new_value["transcript"] = data.transcript

    if data.speaker_consent is not None:
        old_value["speaker_consent"] = recording.speaker_consent
        recording.speaker_consent = data.speaker_consent
        new_value["speaker_consent"] = data.speaker_consent

    audit = AuditLog(
        id=uuid.uuid4(),
        recording_id=recording.id,
        user_id=current_user.id,
        action="visibility_change",
        old_value=old_value or None,
        new_value=new_value or None,
    )
    db.add(audit)

    await db.commit()
    await db.refresh(recording)
    return recording
