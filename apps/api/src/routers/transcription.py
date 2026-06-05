from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import get_db
from src.models.db_models import Recording
import uuid

router = APIRouter()


@router.get("/{recording_id}/status")
async def transcription_status(
    recording_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Recording).where(Recording.id == recording_id)
    )
    recording = result.scalar_one_or_none()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    return {
        "recording_id": recording_id,
        "status": recording.transcription_status,
        "transcript_preview": recording.transcript[:200] if recording.transcript else None,
        "confidence": None,  # populated when completed
    }


@router.get("/{recording_id}/result")
async def transcription_result(
    recording_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Recording).where(Recording.id == recording_id)
    )
    recording = result.scalar_one_or_none()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    if recording.transcription_status != "completed":
        raise HTTPException(status_code=400, detail="Transcription not yet completed")

    return {
        "recording_id": recording_id,
        "status": "completed",
        "transcript": recording.transcript,
        "transcript_latin": recording.transcript_latin,
        "segments": recording.segments,
        "entities": recording.entities,
        "translations": recording.translations,
    }
