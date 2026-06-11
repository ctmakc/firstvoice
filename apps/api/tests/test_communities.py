"""Tests for community endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.db_models import Community, User


@pytest.mark.asyncio
class TestCreateCommunity:
    """POST /api/v1/communities"""

    async def test_create_community(self, test_client: AsyncClient) -> None:
        payload = {
            "name": "Ngāti Porou Heritage",
            "slug": "ngati-porou",
            "languages": ["mri", "eng"],
            "data_policy": "restricted",
        }
        resp = await test_client.post("/api/v1/communities", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["name"] == "Ngāti Porou Heritage"
        assert data["slug"] == "ngati-porou"
        assert data["languages"] == ["mri", "eng"]
        assert data["data_policy"] == "restricted"
        assert "id" in data


@pytest.mark.asyncio
class TestListCommunities:
    """GET /api/v1/communities"""

    async def test_list_communities(
        self, test_client: AsyncClient, test_community: Community
    ) -> None:
        resp = await test_client.get("/api/v1/communities")
        assert resp.status_code == 200
        data = resp.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        slugs = [c["slug"] for c in data]
        assert test_community.slug in slugs


@pytest.mark.asyncio
class TestInviteMember:
    """POST /api/v1/communities/{id}/invite"""

    async def test_invite_existing_user(
        self, test_client: AsyncClient, test_admin: User, test_community: Community, test_member: User
    ) -> None:
        # Use admin's elder key for auth
        resp = await test_client.post(
            f"/api/v1/communities/{test_community.id}/invite",
            json={"email": test_member.email, "role": "viewer"},
            headers={"X-Elder-Key": test_admin.elder_key_token},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == test_member.email
        assert data["role"] == "viewer"

    async def test_invite_unauthorized(
        self, test_client: AsyncClient, test_community: Community, test_member: User
    ) -> None:
        resp = await test_client.post(
            f"/api/v1/communities/{test_community.id}/invite",
            json={"email": test_member.email, "role": "viewer"},
        )
        assert resp.status_code == 401
