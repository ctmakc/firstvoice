import pytest
"""Tests for admin endpoints."""

import io
from httpx import AsyncClient
from src.models.db_models import Community, User


@pytest.mark.asyncio
class TestAuditLog:
    """GET /api/v1/admin/audit-log"""

    async def test_audit_log_requires_auth(
        self, test_client: AsyncClient
    ) -> None:
        resp = await test_client.get("/api/v1/admin/audit-log")
        assert resp.status_code == 401

    async def test_audit_log_returns_entries(
        self, test_client: AsyncClient, test_elder: User, test_community: Community
    ) -> None:
        # Upload a recording to generate audit entry
        audio = io.BytesIO(b"fake audio data")
        await test_client.post(
            "/api/v1/recordings",
            headers={"X-Elder-Key": test_elder.elder_key_token},
            data={
                "community_id": str(test_community.id),
                "language": "mri",
                "visibility": "public",
            },
            files={"audio": ("test.webm", audio, "audio/webm")},
        )

        resp = await test_client.get(
            "/api/v1/admin/audit-log",
            headers={"X-Elder-Key": test_elder.elder_key_token},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        # Should have at least the upload audit entry
        assert len(data) >= 1
        assert data[0]["action"] == "upload"
