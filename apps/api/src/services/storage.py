from minio import Minio
from src.config import get_settings
import io
from typing import BinaryIO

settings = get_settings()

_minio_client: Minio | None = None


def get_minio() -> Minio:
    global _minio_client
    if _minio_client is None:
        _minio_client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )
        # Ensure bucket exists
        if not _minio_client.bucket_exists(settings.minio_bucket):
            _minio_client.make_bucket(settings.minio_bucket)
    return _minio_client


def upload_audio(file_key: str, data: BinaryIO, length: int, content_type: str = "audio/webm") -> None:
    client = get_minio()
    client.put_object(
        settings.minio_bucket,
        file_key,
        data,
        length,
        content_type=content_type,
    )


def download_audio(file_key: str) -> bytes:
    client = get_minio()
    response = client.get_object(settings.minio_bucket, file_key)
    return response.read()


def get_presigned_url(file_key: str, expiry: int = 3600) -> str:
    client = get_minio()
    return client.presigned_get_object(settings.minio_bucket, file_key, expires=expiry)
