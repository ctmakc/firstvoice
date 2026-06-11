"""Tests for authentication endpoints."""

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db_models import User


@pytest.mark.asyncio
class TestAuthCallback:
    """POST /api/v1/auth/callback — OAuth user creation/update."""

    async def test_create_new_oauth_user(self, test_client: AsyncClient) -> None:
        payload = {
            "email": "newuser@example.com",
            "name": "New User",
            "role": "member",
            "oauth_provider": "google",
            "oauth_id": "google-12345",
        }
        resp = await test_client.post("/api/v1/auth/callback", json=payload)
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "newuser@example.com"
        assert data["name"] == "New User"
        assert data["role"] == "member"
        assert "id" in data

    async def test_update_existing_oauth_user(self, test_client: AsyncClient, db_session: AsyncSession) -> None:
        # Create first
        payload = {
            "email": "existing@example.com",
            "name": "Old Name",
            "role": "member",
            "oauth_provider": "google",
            "oauth_id": "google-67890",
        }
        r1 = await test_client.post("/api/v1/auth/callback", json=payload)
        assert r1.status_code == 200

        # Update name
        payload["name"] = "Updated Name"
        r2 = await test_client.post("/api/v1/auth/callback", json=payload)
        assert r2.status_code == 200
        data = r2.json()
        assert data["name"] == "Updated Name"
        assert data["email"] == "existing@example.com"


@pytest.mark.asyncio
class TestGetMe:
    """GET /api/v1/auth/me — retrieve current user."""

    async def test_get_me_by_email(self, test_client: AsyncClient) -> None:
        # First create user
        await test_client.post("/api/v1/auth/callback", json={
            "email": "byemail@example.com",
            "name": "By Email",
            "role": "member",
            "oauth_provider": "google",
            "oauth_id": "google-byemail",
        })

        resp = await test_client.get("/api/v1/auth/me?email=byemail@example.com")
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == "byemail@example.com"

    async def test_get_me_unauthorized(self, test_client: AsyncClient) -> None:
        resp = await test_client.get("/api/v1/auth/me")
        assert resp.status_code == 401

    async def test_get_me_by_elder_key(
        self, test_client: AsyncClient, test_elder: User
    ) -> None:
        resp = await test_client.get(
            "/api/v1/auth/me",
            headers={"X-Elder-Key": test_elder.elder_key_token},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert data["email"] == test_elder.email
        assert data["role"] == "elder"
        assert data["name"] == "Elder Test"

    async def test_get_me_invalid_elder_key(self, test_client: AsyncClient) -> None:
        resp = await test_client.get(
            "/api/v1/auth/me",
            headers={"X-Elder-Key": "totally-invalid-key"},
        )
        assert resp.status_code == 401


@pytest.mark.asyncio
class TestElderKeyGeneration:
    """POST /api/v1/auth/elder-key — generate elder key."""

    async def test_generate_elder_key(
        self, test_client: AsyncClient, test_admin: User, test_community
    ) -> None:
        resp = await test_client.post(
            "/api/v1/auth/elder-key",
            params={"user_id": str(test_admin.id), "community_id": str(test_community.id)},
        )
        assert resp.status_code == 200
        data = resp.json()
        assert "elder_key" in data
        assert len(data["elder_key"]) > 20
        assert str(data["community_id"]) == str(test_community.id)

    async def test_generate_elder_key_user_not_found(self, test_client: AsyncClient, test_community) -> None:
        fake_id = "00000000-0000-0000-0000-000000000000"
        resp = await test_client.post(
            "/api/v1/auth/elder-key",
            params={"user_id": fake_id, "community_id": str(test_community.id)},
        )
        assert resp.status_code == 404
