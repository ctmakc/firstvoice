import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer, Boolean, Text, ForeignKey, JSON, Float
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from geoalchemy2 import Geography
from src.database import Base


class Community(Base):
    __tablename__ = "communities"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(255), nullable=False)
    slug = Column(String(100), unique=True, nullable=False)
    territory_geo = Column(JSON)
    languages = Column(ARRAY(String(10)))
    data_policy = Column(String(20), default="restricted")
    council_members = Column(ARRAY(UUID(as_uuid=True)))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True)
    name = Column(String(255))
    avatar_url = Column(Text)
    role = Column(String(20), default="viewer")
    community_id = Column(UUID(as_uuid=True), ForeignKey("communities.id"))
    elder_key_token = Column(String(64), unique=True)
    oauth_provider = Column(String(50))
    oauth_id = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)


class Recording(Base):
    __tablename__ = "recordings"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    community_id = Column(UUID(as_uuid=True), ForeignKey("communities.id"), nullable=False)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    audio_file_key = Column(String(500), nullable=False)
    duration_seconds = Column(Integer)
    format = Column(String(10), default="webm")
    title = Column(String(500))
    language = Column(String(10), nullable=False)
    transcript = Column(Text)
    transcript_latin = Column(Text)
    segments = Column(JSON)
    translations = Column(JSON)
    entities = Column(JSON)
    visibility = Column(String(20), default="sacred")
    ai_training_allowed = Column(Boolean, default=False)
    speaker_name = Column(String(255))
    speaker_consent = Column(String(20), default="pending")
    occasion = Column(String(255))
    location_point = Column(Geography("POINT", srid=4326))
    provenance_tx_hash = Column(String(66))
    provenance_token_id = Column(String(100))
    transcription_status = Column(String(20), default="pending")
    confidence = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)


class AuditLog(Base):
    __tablename__ = "audit_log"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    recording_id = Column(UUID(as_uuid=True), ForeignKey("recordings.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    action = Column(String(50), nullable=False)
    old_value = Column(JSON)
    new_value = Column(JSON)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
