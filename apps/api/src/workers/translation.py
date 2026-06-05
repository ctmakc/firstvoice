import json
import uuid
from typing import Any

from src.celery_app import celery_app
from src.config import get_settings
from src.database import sync_engine
from src.models.db_models import Recording, AuditLog
from sqlalchemy.orm import Session

settings = get_settings()

_genai_configured = False
_gemini_model: Any = None


def _get_gemini_model() -> Any:
    """Lazy-configure and return the Gemini generative model."""
    global _genai_configured, _gemini_model
    if not _genai_configured:
        import google.generativeai as genai
        genai.configure(api_key=settings.gemini_api_key)
        _genai_configured = True
        _gemini_model = genai.GenerativeModel("gemini-1.5-flash")
    return _gemini_model


@celery_app.task(bind=True, max_retries=3)
def translate_and_extract(self, recording_id: str) -> dict:
    """Translate transcript to English and French and extract named entities."""
    db = Session(bind=sync_engine)
    try:
        recording = db.query(Recording).filter(Recording.id == recording_id).first()
        if not recording:
            raise ValueError(f"Recording {recording_id} not found")
        if not recording.transcript:
            raise ValueError(f"Recording {recording_id} has no transcript")

        model = _get_gemini_model()
        occasion_context = recording.occasion or "general oral tradition"
        language_name = recording.language or "unknown"

        prompt = f"""You are a linguist and ethnographer assisting an Indigenous language preservation platform.

Given the following transcript in language "{language_name}", perform two tasks:

1. Translate the transcript into English and French. Preserve cultural nuance and context.
2. Extract named entities of types: person, place, plant, animal. Include their approximate character positions (start and end indices) in the ORIGINAL transcript text.

Occasion / context: {occasion_context}

Transcript:
{recording.transcript}

Return ONLY a JSON object with exactly this structure (no markdown, no extra text):
{{
  "translations": {{"en": "...", "fr": "..."}},
  "entities": [
    {{"type": "person|place|plant|animal", "text": "...", "start": 0, "end": 5}}
  ]
}}"""

        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Strip markdown code fences if present
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.startswith("```"):
            raw_text = raw_text[3:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]
        raw_text = raw_text.strip()

        result = json.loads(raw_text)

        translations = result.get("translations", {})
        entities = result.get("entities", [])

        # Validate and sanitize entities
        sanitized_entities = []
        for ent in entities:
            ent_type = ent.get("type", "").lower()
            if ent_type not in ("person", "place", "plant", "animal"):
                continue
            text = ent.get("text", "")
            start = ent.get("start")
            end = ent.get("end")
            if start is None or end is None:
                idx = recording.transcript.find(text)
                start = idx if idx != -1 else 0
                end = start + len(text) if idx != -1 else len(text)
            sanitized_entities.append({
                "type": ent_type,
                "text": text,
                "start": start,
                "end": end,
            })

        recording.translations = translations
        recording.entities = sanitized_entities

        audit = AuditLog(
            id=uuid.uuid4(),
            recording_id=recording.id,
            user_id=recording.uploaded_by,
            action="translation_extracted",
            new_value={
                "languages": list(translations.keys()),
                "entity_count": len(sanitized_entities),
            },
        )
        db.add(audit)
        db.commit()

        return {
            "recording_id": recording_id,
            "translations": translations,
            "entity_count": len(sanitized_entities),
        }

    except Exception as exc:
        db.rollback()
        raise self.retry(exc=exc, countdown=60)

    finally:
        db.close()
