"""Pytest fixtures for FirstVoice backend tests."""

import pytest_asyncio
import uuid
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import NullPool
from sqlalchemy import text

import os

# Test database URL
TEST_DATABASE_URL = "postgresql+asyncpg://fv:devpass@localhost:5437/firstvoice"

os.environ["DATABASE_URL"] = TEST_DATABASE_URL
os.environ["SYNC_DATABASE_URL"] = TEST_DATABASE_URL.replace("+asyncpg", "")
os.environ["REDIS_URL"] = "redis://localhost:6379/1"
os.environ["APP_ENV"] = "testing"
os.environ["APP_SECRET"] = "test-secret-32-chars-long"

# Create fresh engine for tests with NullPool (no connection reuse issues)
test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    future=True,
    poolclass=NullPool,
)
TestSessionLocal = async_sessionmaker(test_engine, expire_on_commit=False, autoflush=False)

# Import app AFTER env vars set
from src.main import app
from src.database import get_db
from src.models.db_models import Community, User


async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
    """Override dependency to use test session."""
    async with TestSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db


@pytest_asyncio.fixture(autouse=True, scope="function")
async def clean_database():
    """Clean tables before each test."""
    async with test_engine.begin() as conn:
        await conn.execute(text("DELETE FROM audit_log"))
        await conn.execute(text("DELETE FROM recordings"))
        await conn.execute(text("DELETE FROM users"))
        await conn.execute(text("DELETE FROM communities"))
    yield


@pytest_asyncio.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Fresh test session per test."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()


@pytest_asyncio.fixture
async def test_client() -> AsyncGenerator[AsyncClient, None]:
    """Async HTTP client for FastAPI app."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client


@pytest_asyncio.fixture
async def test_community(db_session: AsyncSession) -> Community:
    """Create a test community."""
    community = Community(
        id=uuid.uuid4(),
        name="Test Māori Community",
        slug="test-maori",
        languages=["mri", "eng"],
        data_policy="community-review",
    )
    db_session.add(community)
    await db_session.commit()
    await db_session.refresh(community)
    return community


@pytest_asyncio.fixture
async def test_elder(db_session: AsyncSession, test_community: Community) -> User:
    """Create a test elder user."""
    elder = User(
        id=uuid.uuid4(),
        email="elder@test.firstvoice",
        name="Elder Test",
        role="elder",
        community_id=test_community.id,
        elder_key_token="test-elder-key-secret-token",
    )
    db_session.add(elder)
    await db_session.commit()
    await db_session.refresh(elder)
    return elder


@pytest_asyncio.fixture
async def test_admin(db_session: AsyncSession, test_community: Community) -> User:
    """Create a test admin user."""
    admin = User(
        id=uuid.uuid4(),
        email="admin@test.firstvoice",
        name="Admin Test",
        role="admin",
        community_id=test_community.id,
        elder_key_token="test-admin-key-secret-token",
    )
    db_session.add(admin)
    await db_session.commit()
    await db_session.refresh(admin)
    return admin


@pytest_asyncio.fixture
async def test_member(db_session: AsyncSession, test_community: Community) -> User:
    """Create a test member user."""
    member = User(
        id=uuid.uuid4(),
        email="member@test.firstvoice",
        name="Member Test",
        role="member",
        community_id=test_community.id,
    )
    db_session.add(member)
    await db_session.commit()
    await db_session.refresh(member)
    return member
