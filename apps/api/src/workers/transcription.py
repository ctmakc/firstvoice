import os
import tempfile
import uuid
from typing import Any

from src.celery_app import celery_app
from src.config import get_settings
from src.database import sync_engine
from src.models.db_models import Recording, AuditLog
from src.services.storage import download_audio
from sqlalchemy.orm import Session

settings = get_settings()
_whisper_model: Any = None


def get_whisper_model() -> Any:
    """Lazy-load and cache the faster-whisper model."""
    global _whisper_model
    if _whisper_model is None:
        from faster_whisper import WhisperModel
        _whisper_model = WhisperModel(
            "large-v3",
            device="cpu",
            compute_type="int8",
        )
    return _whisper_model


@celery_app.task(bind=True, max_retries=3)
def transcribe_recording(self, recording_id: str) -> dict:
    """Transcribe a recording using faster-whisper and enqueue translation."""
    db = Session(bind=sync_engine)
    try:
        recording = db.query(Recording).filter(Recording.id == recording_id).first()
        if not recording:
            raise ValueError(f"Recording {recording_id} not found")

        if recording.transcription_status == "completed":
            return {"status": "already_completed", "recording_id": recording_id}

        # Mark as processing
        recording.transcription_status = "processing"
        db.commit()

        # Download audio from MinIO
        audio_bytes = download_audio(recording.audio_file_key)

        # Write to temporary file
        suffix = f".{recording.format}" if recording.format else ".webm"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
            tmp.write(audio_bytes)
            tmp_path = tmp.name

        try:
            model = get_whisper_model()
            segments_iter, info = model.transcribe(tmp_path, beam_size=5)

            segments = []
            transcript_parts = []
            for segment in segments_iter:
                segments.append({
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text.strip(),
                    "speaker_id": None,  # TODO: speaker diarization
                })
                transcript_parts.append(segment.text.strip())

            transcript = " ".join(transcript_parts)
            confidence = getattr(info, "language_probability", None)
            if confidence is None:
                confidence = getattr(info, "avg_logprob", None)

            recording.transcript = transcript
            recording.segments = segments
            recording.confidence = confidence
            recording.transcription_status = "completed"

            audit = AuditLog(
                id=uuid.uuid4(),
                recording_id=recording.id,
                user_id=recording.uploaded_by,
                action="transcription_completed",
                new_value={
                    "confidence": confidence,
                    "segments_count": len(segments),
                    "language_detected": getattr(info, "language", None),
                },
            )
            db.add(audit)
            db.commit()

            # Enqueue translation + entity extraction
            from src.workers.translation import translate_and_extract
            translate_and_extract.delay(recording_id)

            return {
                "recording_id": recording_id,
                "status": "completed",
                "segments_count": len(segments),
                "confidence": confidence,
            }
        finally:
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    except Exception as exc:
        db.rollback()
        try:
            recording = db.query(Recording).filter(Recording.id == recording_id).first()
            if recording:
                recording.transcription_status = "failed"
                db.commit()
        except Exception:
            pass
        raise self.retry(exc=exc, countdown=60)

    finally:
        db.close()
