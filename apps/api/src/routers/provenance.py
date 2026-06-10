import hashlib
import uuid

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from src.database import get_db
from src.middleware.auth import get_current_user
from src.models.db_models import Recording, User, AuditLog, Community
from src.services.provenance import mint_provenance, get_provenance
from src.services.storage import download_audio

router = APIRouter()


def _sha256_bytes(data: bytes) -> str:
    return "0x" + hashlib.sha256(data).hexdigest()


class MintRequest(BaseModel):
    recording_id: uuid.UUID


@router.post("/mint")
async def mint_provenance_endpoint(
    data: MintRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Mint a Soulbound Provenance NFT for a recording."""
    if current_user.role not in ("elder", "admin", "superadmin"):
        raise HTTPException(status_code=403, detail="Only elders and admins can mint provenance")

    recording_id = data.recording_id
    result = await db.execute(select(Recording).where(Recording.id == recording_id))
    recording = result.scalar_one_or_none()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    if recording.provenance_tx_hash:
        raise HTTPException(status_code=400, detail="Provenance already minted for this recording")

    try:
        audio_bytes = download_audio(recording.audio_file_key)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to download audio: {exc}")

    content_hash = _sha256_bytes(audio_bytes)

    comm_result = await db.execute(
        select(Community).where(Community.id == recording.community_id)
    )
    community = comm_result.scalar_one_or_none()
    community_name = community.name if community else "unknown"

    try:
        tx_hash, token_id = mint_provenance(
            recording_id=str(recording_id),
            content_hash=content_hash,
            community=community_name,
            language=recording.language,
            ai_allowed=recording.ai_training_allowed or False,
        )
    except ValueError as exc:
        raise HTTPException(status_code=503, detail=f"Provenance service misconfigured: {exc}")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Blockchain mint failed: {exc}")

    recording.provenance_tx_hash = tx_hash
    if token_id is not None:
        recording.provenance_token_id = str(token_id)

    audit = AuditLog(
        id=uuid.uuid4(),
        recording_id=recording.id,
        user_id=current_user.id,
        action="mint_provenance",
        new_value={"tx_hash": tx_hash, "token_id": token_id, "content_hash": content_hash},
    )
    db.add(audit)
    await db.commit()
    await db.refresh(recording)

    return {"tx_hash": tx_hash, "token_id": token_id}


@router.get("/{recording_id}")
async def get_provenance_endpoint(
    recording_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """Get provenance details for a recording."""
    result = await db.execute(select(Recording).where(Recording.id == recording_id))
    recording = result.scalar_one_or_none()
    if not recording:
        raise HTTPException(status_code=404, detail="Recording not found")

    on_chain = None
    if recording.provenance_token_id:
        try:
            on_chain = get_provenance(int(recording.provenance_token_id))
        except Exception:
            on_chain = None

    return {
        "recording_id": recording_id,
        "provenance_tx_hash": recording.provenance_tx_hash,
        "provenance_token_id": recording.provenance_token_id,
        "on_chain_metadata": on_chain,
    }
