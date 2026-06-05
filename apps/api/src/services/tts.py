import io
import os
import tempfile
import wave
from typing import List

import numpy as np

from src.config import get_settings
from src.services.storage import upload_audio

settings = get_settings()


def _numpy_to_wav_bytes(audio_array: np.ndarray, sample_rate: int = 22050) -> bytes:
    """Convert a numpy float audio array to WAV bytes using stdlib wave."""
    buf = io.BytesIO()
    audio_int16 = (np.array(audio_array) * 32767).astype(np.int16)
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(audio_int16.tobytes())
    return buf.getvalue()


def synthesize_text(text: str, language: str, speaker_samples: List[bytes]) -> bytes:
    """Synthesize speech using Coqui XTTS v2, falling back to Piper."""
    if not text or not text.strip():
        raise ValueError("Text must be non-empty")

    try:
        return _synthesize_xtts(text, language, speaker_samples)
    except Exception as xtts_err:
        try:
            return _synthesize_piper(text, language)
        except Exception as piper_err:
            raise RuntimeError(
                f"TTS synthesis failed. XTTS error: {xtts_err}. Piper error: {piper_err}"
            ) from xtts_err


def _synthesize_xtts(text: str, language: str, speaker_samples: List[bytes]) -> bytes:
    from TTS.api import TTS

    tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2")

    speaker_wav_paths = []
    try:
        for sample in speaker_samples:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                f.write(sample)
                speaker_wav_paths.append(f.name)

        wav = tts.tts(text=text, speaker_wav=speaker_wav_paths, language=language)
        return _numpy_to_wav_bytes(np.array(wav), 22050)
    finally:
        for p in speaker_wav_paths:
            try:
                os.unlink(p)
            except OSError:
                pass


def _synthesize_piper(text: str, language: str) -> bytes:
    try:
        from piper import PiperVoice
    except ImportError as exc:
        raise RuntimeError("Piper TTS not installed") from exc

    model_path = os.environ.get("PIPER_MODEL_PATH", f"piper_models/{language}")
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Piper model not found at {model_path}")

    voice = PiperVoice.load(model_path)
    audio_bytes = b"".join(voice.synthesize(text))
    return audio_bytes


def store_tts_result(recording_id: str, language: str, audio_bytes: bytes) -> str:
    """Store synthesized TTS audio in MinIO."""
    file_key = f"tts/{language}/{recording_id}.wav"
    data = io.BytesIO(audio_bytes)
    upload_audio(file_key, data, len(audio_bytes), content_type="audio/wav")
    return file_key
