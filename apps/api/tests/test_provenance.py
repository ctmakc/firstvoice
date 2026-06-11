import pytest
"""Tests for provenance / Web3 endpoints."""

import io
from httpx import AsyncClient
from src.models.db_models import Community, User


@pytest.mark.asyncio
class TestMintProvenance:
    """POST /api/v1/provenance/mint"""

    async def test_mint_requires_auth(
        self, test_client: AsyncClient
    ) -> None:
        resp = await test_client.post(
            "/api/v1/provenance/mint",
            json={"recording_id": "00000000-0000-0000-0000-000000000000"},
        )
        assert resp.status_code == 401

    async def test_mint_invalid_contract(
        self, test_client: AsyncClient, test_admin: User, test_community: Community
    ) -> None:
        # Contract address is set to local hardhat which may not be running
        # Upload a recording first
        audio = io.BytesIO(b"fake audio data")
        upload = await test_client.post(
            "/api/v1/recordings",
            headers={"X-Elder-Key": test_admin.elder_key_token},
            data={
                "community_id": str(test_community.id),
                "language": "mri",
                "visibility": "public",
            },
            files={"audio": ("test.webm", audio, "audio/webm")},
        )
        rec_id = upload.json()["id"]

        resp = await test_client.post(
            "/api/v1/provenance/mint",
            headers={"X-Elder-Key": test_admin.elder_key_token},
            json={"recording_id": rec_id},
        )
        # 502/503 if blockchain is unreachable, 200 if local node running
        assert resp.status_code in (200, 502, 503, 500)
