from typing import Optional, Dict, List
from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID


# ─── Community ───

class CommunityBase(BaseModel):
    name: str
    slug: str
    languages: List[str] = []
    data_policy: str = "restricted"


class CommunityCreate(CommunityBase):
    pass


class CommunityRead(CommunityBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ─── User ───

class UserBase(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    role: str = "viewer"
    community_id: Optional[UUID] = None


class UserCreate(UserBase):
    oauth_provider: Optional[str] = None
    oauth_id: Optional[str] = None


class UserRead(UserBase):
    id: UUID
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Recording ───

class Segment(BaseModel):
    start: float
    end: float
    text: str
    speaker_id: Optional[str] = None


class RecordingCreate(BaseModel):
    community_id: UUID
    language: str = Field(..., max_length=10)
    title: Optional[str] = None
    occasion: Optional[str] = None
    visibility: str = "sacred"
    ai_training_allowed: bool = False
    speaker_name: Optional[str] = None
    location: Optional[Dict[str, float]] = None  # {"lat": 0.0, "lng": 0.0}


class RecordingUpdate(BaseModel):
    title: Optional[str] = None
    transcript: Optional[str] = None
    visibility: Optional[str] = None
    ai_training_allowed: Optional[bool] = None
    speaker_consent: Optional[str] = None


class RecordingRead(BaseModel):
    id: UUID
    community_id: UUID
    uploaded_by: UUID
    audio_file_key: str
    duration_seconds: Optional[int]
    title: Optional[str]
    language: str
    transcript: Optional[str]
    transcript_latin: Optional[str]
    segments: Optional[List[Segment]]
    translations: Optional[Dict[str, str]]
    entities: Optional[List[Dict]]
    visibility: str
    ai_training_allowed: bool
    speaker_name: Optional[str]
    speaker_consent: str
    occasion: Optional[str]
    transcription_status: str
    provenance_tx_hash: Optional[str]
    provenance_token_id: Optional[str] = None
    confidence: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ─── Audit Log ───

class AuditLogRead(BaseModel):
    id: UUID
    recording_id: Optional[UUID]
    user_id: Optional[UUID]
    action: str
    old_value: Optional[Dict]
    new_value: Optional[Dict]
    created_at: datetime

    class Config:
        from_attributes = True
