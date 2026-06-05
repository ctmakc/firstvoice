"""001_initial

Revision ID: 001_initial
Revises:
Create Date: 2026-06-04 00:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from geoalchemy2 import Geography
import uuid

revision = "001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "communities",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("slug", sa.String(100), unique=True, nullable=False),
        sa.Column("territory_geo", sa.JSON()),
        sa.Column("languages", ARRAY(sa.String(10))),
        sa.Column("data_policy", sa.String(20), server_default="restricted"),
        sa.Column("council_members", ARRAY(UUID(as_uuid=True))),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "users",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("email", sa.String(255), unique=True),
        sa.Column("name", sa.String(255)),
        sa.Column("avatar_url", sa.Text()),
        sa.Column("role", sa.String(20), server_default="viewer"),
        sa.Column("community_id", UUID(as_uuid=True), sa.ForeignKey("communities.id")),
        sa.Column("elder_key_token", sa.String(64), unique=True),
        sa.Column("oauth_provider", sa.String(50)),
        sa.Column("oauth_id", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "recordings",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("community_id", UUID(as_uuid=True), sa.ForeignKey("communities.id"), nullable=False),
        sa.Column("uploaded_by", UUID(as_uuid=True), sa.ForeignKey("users.id"), nullable=False),
        sa.Column("audio_file_key", sa.String(500), nullable=False),
        sa.Column("duration_seconds", sa.Integer()),
        sa.Column("format", sa.String(10), server_default="webm"),
        sa.Column("title", sa.String(500)),
        sa.Column("language", sa.String(10), nullable=False),
        sa.Column("transcript", sa.Text()),
        sa.Column("transcript_latin", sa.Text()),
        sa.Column("segments", sa.JSON()),
        sa.Column("translations", sa.JSON()),
        sa.Column("entities", sa.JSON()),
        sa.Column("visibility", sa.String(20), server_default="sacred"),
        sa.Column("ai_training_allowed", sa.Boolean(), server_default=sa.text("false")),
        sa.Column("speaker_name", sa.String(255)),
        sa.Column("speaker_consent", sa.String(20), server_default="pending"),
        sa.Column("occasion", sa.String(255)),
        sa.Column("location_point", Geography("POINT", srid=4326)),
        sa.Column("provenance_tx_hash", sa.String(66)),
        sa.Column("provenance_token_id", sa.String(100)),
        sa.Column("transcription_status", sa.String(20), server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_table(
        "audit_log",
        sa.Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4),
        sa.Column("recording_id", UUID(as_uuid=True), sa.ForeignKey("recordings.id")),
        sa.Column("user_id", UUID(as_uuid=True), sa.ForeignKey("users.id")),
        sa.Column("action", sa.String(50), nullable=False),
        sa.Column("old_value", sa.JSON()),
        sa.Column("new_value", sa.JSON()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()")),
    )

    op.create_index("ix_recordings_community_id", "recordings", ["community_id"])
    op.create_index("ix_recordings_visibility", "recordings", ["visibility"])
    op.create_index("ix_audit_log_recording_id", "audit_log", ["recording_id"])
    op.create_index("ix_audit_log_user_id", "audit_log", ["user_id"])
    op.create_index("ix_users_community_id", "users", ["community_id"])
    op.create_index("ix_users_elder_key_token", "users", ["elder_key_token"])


def downgrade() -> None:
    op.drop_index("ix_users_elder_key_token", table_name="users")
    op.drop_index("ix_users_community_id", table_name="users")
    op.drop_index("ix_audit_log_user_id", table_name="audit_log")
    op.drop_index("ix_audit_log_recording_id", table_name="audit_log")
    op.drop_index("ix_recordings_visibility", table_name="recordings")
    op.drop_index("ix_recordings_community_id", table_name="recordings")
    op.drop_table("audit_log")
    op.drop_table("recordings")
    op.drop_table("users")
    op.drop_table("communities")
