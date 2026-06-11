import pytest
"""Tests for recording endpoints."""

import io
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db_models import Community, User, Recording


@pytest.mark.asyncio
class TestUploadRecording:
    """POST /api/v1/recordings"""

    async def test_upload_audio(
        self, test_client: AsyncClient, test_elder: User, test_community: Community
    ) -> None:
        audio = io.BytesIO(b"fake audio data for testing")
        resp = await test_client.post(
            "/api/v1/recordings",
            headers={"X-Elder-Key": test_elder.elder_key_token},
            data={
                "community_id": str(test_community.id),
                "language": "mri",
                "title": "Tūmatauenga Story",
                "occasion": "Marae Gathering",
                "visibility": "sacred",
                "speaker_name": "Elder Test",
            },
            files={"audio": ("test.webm", audio, "audio/webm")},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["title"] == "Tūmatauenga Story"
        assert data["language"] == "mri"
        assert data["visibility"] == "sacred"
        assert data["speaker_name"] == "Elder Test"
        assert data["transcription_status"] == "pending"
        assert "id" in data
        assert "audio_file_key" in data

    async def test_upload_without_auth(
        self, test_client: AsyncClient, test_community: Community
    ) -> None:
        audio = io.BytesIO(b"fake audio data")
        resp = await test_client.post(
            "/api/v1/recordings",
            data={
                "community_id": str(test_community.id),
                "language": "mri",
                "visibility": "public",
            },
            files={"audio": ("test.webm", audio, "audio/webm")},
        )
        assert resp.status_code == 401

    async def test_upload_invalid_audio_format(
        self, test_client: AsyncClient, test_elder: User, test_community: Community
    ) -> None:
        audio = io.BytesIO(b"fake audio data")
        resp = await test_client.post(
            "/api/v1/recordings",
            headers={"X-Elder-Key": test_elder.elder_key_token},
            data={
                "community_id": str(test_community.id),
                "language": "mri",
                "visibility": "public",
            },
            files={"audio": ("test.txt", audio, "text/plain")},
        )
        assert resp.status_code == 400


@pytest.mark.asyncio
class TestListRecordings:
    """GET /api/v1/recordings"""

    async def test_list_public_recordings(
        self, test_client: AsyncClient, test_member: User, test_community: Community
    ) -> None:
        # Create a public recording first (via upload test helper)
        # For now, just check list endpoint returns list
        resp = await test_client.get("/api/v1/recordings")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)

    async def test_list_with_community_filter(
        self, test_client: AsyncClient, test_community: Community
    ) -> None:
        resp = await test_client.get(
            f"/api/v1/recordings?community_id={test_community.id}"
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)


@pytest.mark.asyncio
class TestUpdateRecording:
    """PATCH /api/v1/recordings/{id}"""

    async def test_approve_recording(
        self, test_client: AsyncClient, test_admin: User, test_elder: User, test_community: Community
    ) -> None:
        # Upload a sacred recording as elder
        audio = io.BytesIO(b"fake audio data")
        upload_resp = await test_client.post(
            "/api/v1/recordings",
            headers={"X-Elder-Key": test_elder.elder_key_token},
            data={
                "community_id": str(test_community.id),
                "language": "mri",
                "title": "Sacred Story",
                "visibility": "sacred",
            },
            files={"audio": ("test.webm", audio, "audio/webm")},
        )
        rec_id = upload_resp.json()["id"]

        # Admin changes to public
        patch = await test_client.patch(
            f"/api/v1/recordings/{rec_id}",
            headers={"X-Elder-Key": test_admin.elder_key_token},
            json={"visibility": "public"},
        )
        assert patch.status_code == 200
        data = patch.json()
        assert data["visibility"] == "public"

    async def test_update_without_privileges(
        self, test_client: AsyncClient, test_member: User, test_elder: User, test_community: Community
    ) -> None:
        # Upload as elder
        audio = io.BytesIO(b"fake audio data")
        upload = await test_client.post(
            "/api/v1/recordings",
            headers={"X-Elder-Key": test_elder.elder_key_token},
            data={
                "community_id": str(test_community.id),
                "language": "mri",
                "visibility": "sacred",
            },
            files={"audio": ("test.webm", audio, "audio/webm")},
        )
        rec_id = upload.json()["id"]

        # Member tries to change (should fail)
        patch = await test_client.patch(
            f"/api/v1/recordings/{rec_id}",
            headers={"X-Elder-Key": test_member.elder_key_token},
            json={"visibility": "public"},
        )
        assert patch.status_code == 403
