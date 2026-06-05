#!/usr/bin/env python3
"""
Comprehensive seed script for FirstVoice grant demo.
Creates realistic Indigenous communities, languages, users, and sample recordings.
"""
import sys
import os
import uuid
import datetime
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.orm import sessionmaker
from src.database import sync_engine, Base
from src.models.db_models import Community, User, Recording, AuditLog
from src.services.storage import get_minio

Session = sessionmaker(bind=sync_engine)


def seed() -> None:
    Base.metadata.create_all(bind=sync_engine)
    session = Session()

    # Check if already seeded
    existing = session.query(Community).filter_by(slug="cree-pilot").first()
    if existing:
        print("✅ Seed data already present.")
        session.close()
        return

    # ── Communities ──
    communities_data = [
        {
            "name": "Cree First Nation — Digital Heritage Pilot",
            "slug": "cree-pilot",
            "languages": ["cre", "eng"],
            "data_policy": "restricted",
            "region": "Northern Quebec",
            "description": "Pilot community for FirstVoice digital heritage preservation.",
        },
        {
            "name": "Inuit Heritage Trust",
            "slug": "inuit-heritage",
            "languages": ["iku", "eng"],
            "data_policy": "restricted",
            "region": "Nunavut",
            "description": "Preserving Inuktitut oral traditions and traditional knowledge.",
        },
        {
            "name": "Ojibwe Language Circle",
            "slug": "ojibwe-circle",
            "languages": ["oji", "eng"],
            "data_policy": "community-review",
            "region": "Great Lakes Region",
            "description": "Community-driven Ojibwe language revitalization.",
        },
        {
            "name": "Te Reo Māori Digital Archive",
            "slug": "maori-archive",
            "languages": ["mri", "eng"],
            "data_policy": "community-review",
            "region": "Aotearoa New Zealand",
            "description": "Māori language and whakapapa preservation for future generations.",
        },
        {
            "name": "Hawaiian Language Preservation Council",
            "slug": "hawaiian-council",
            "languages": ["haw", "eng"],
            "data_policy": "open",
            "region": "Hawaiʻi",
            "description": "Revitalizing ʻŌlelo Hawaiʻi through community recordings.",
        },
    ]

    communities = {}
    for cd in communities_data:
        c = Community(
            id=uuid.uuid4(),
            name=cd["name"],
            slug=cd["slug"],
            languages=cd["languages"],
            data_policy=cd["data_policy"],
        )
        session.add(c)
        communities[cd["slug"]] = c
        print(f"  Created community: {c.name}")

    session.flush()

    # ── Users ──
    users_data = [
        # Cree
        {"email": "elder.sarah@cree.firstvoice", "name": "Elder Sarah Whitefish",
         "role": "elder", "community_slug": "cree-pilot"},
        {"email": "admin.james@cree.firstvoice", "name": "James Thunderchild",
         "role": "admin", "community_slug": "cree-pilot"},
        {"email": "youth.maya@cree.firstvoice", "name": "Maya Littlebear",
         "role": "member", "community_slug": "cree-pilot"},
        # Inuit
        {"email": "elder.nanuq@inuit.firstvoice", "name": "Elder Nanuq Ujarak",
         "role": "elder", "community_slug": "inuit-heritage"},
        {"email": "coordinator.ava@inuit.firstvoice", "name": "Ava Tootoo",
         "role": "admin", "community_slug": "inuit-heritage"},
        # Ojibwe
        {"email": "elder.migizi@ojibwe.firstvoice", "name": "Elder Migizi (Eagle)",
         "role": "elder", "community_slug": "ojibwe-circle"},
        {"email": "linguist.david@ojibwe.firstvoice", "name": "David Thunderbird",
         "role": "admin", "community_slug": "ojibwe-circle"},
        # Māori
        {"email": "kaumātua.tane@maori.firstvoice", "name": "Kaumātua Tane Mahuta",
         "role": "elder", "community_slug": "maori-archive"},
        {"email": "whaea.hine@maori.firstvoice", "name": "Whāea Hine Moana",
         "role": "admin", "community_slug": "maori-archive"},
        {"email": "rangatahi.manaia@maori.firstvoice", "name": "Manaia Rangi",
         "role": "member", "community_slug": "maori-archive"},
        # Hawaiian
        {"email": "kupuna.makana@hawaiian.firstvoice", "name": "Kupuna Makana Kāne",
         "role": "elder", "community_slug": "hawaiian-council"},
        {"email": "director.lei@hawaiian.firstvoice", "name": "Lei Lokelani",
         "role": "admin", "community_slug": "hawaiian-council"},
        # Superadmin
        {"email": "admin@firstvoice.org", "name": "Platform Administrator",
         "role": "superadmin", "community_slug": None},
    ]

    users_by_email = {}
    import secrets
    for ud in users_data:
        community_id = communities[ud["community_slug"]].id if ud["community_slug"] else None
        token = secrets.token_urlsafe(32) if ud["role"] == "elder" else None
        u = User(
            id=uuid.uuid4(),
            email=ud["email"],
            name=ud["name"],
            role=ud["role"],
            community_id=community_id,
            elder_key_token=token,
        )
        session.add(u)
        users_by_email[ud["email"]] = u
        key_hint = f" (Elder Key: {token[:16]}...)" if token else ""
        print(f"  Created user: {u.name} [{u.role}]{key_hint}")

    session.flush()

    # ── Sample Recordings (with mock metadata, no actual audio files) ──
    recordings_data = [
        {
            "title": "The Story of the Caribou Migration",
            "language": "cre",
            "speaker_name": "Elder Sarah Whitefish",
            "visibility": "sacred",
            "occasion": "Winter Gathering",
            "transcript": "Tānisi nitôtêm... (The caribou have always walked this path...)",
            "translations": {"en": "The caribou have always walked this path..."},
            "community_slug": "cree-pilot",
            "uploaded_by_email": "elder.sarah@cree.firstvoice",
            "ai_training_allowed": False,
        },
        {
            "title": "Naming Ceremony Traditions",
            "language": "cre",
            "speaker_name": "James Thunderchild",
            "visibility": "public",
            "occasion": "Naming Ceremony",
            "transcript": "When a child is born, the elders gather...",
            "translations": {"en": "When a child is born, the elders gather to bestow a name..."},
            "community_slug": "cree-pilot",
            "uploaded_by_email": "admin.james@cree.firstvoice",
            "ai_training_allowed": True,
        },
        {
            "title": "Inuit Star Knowledge",
            "language": "iku",
            "speaker_name": "Elder Nanuq Ujarak",
            "visibility": "sacred",
            "occasion": "Spring Camp",
            "transcript": "ᓂᕆᔭᓐᓂᐊ... (The stars guide our way across the ice...)",
            "translations": {"en": "The stars guide our way across the ice..."},
            "community_slug": "inuit-heritage",
            "uploaded_by_email": "elder.nanuq@inuit.firstvoice",
            "ai_training_allowed": False,
        },
        {
            "title": "Sewing Caribou Skin",
            "language": "iku",
            "speaker_name": "Ava Tootoo",
            "visibility": "public",
            "occasion": "Community Workshop",
            "transcript": "First, you must thank the animal...",
            "translations": {"en": "First, you must thank the animal before touching the skin..."},
            "community_slug": "inuit-heritage",
            "uploaded_by_email": "coordinator.ava@inuit.firstvoice",
            "ai_training_allowed": True,
        },
        {
            "title": "Seven Fires Prophecy",
            "language": "oji",
            "speaker_name": "Elder Migizi (Eagle)",
            "visibility": "sacred",
            "occasion": "Midewiwin Ceremony",
            "transcript": "The Seven Fires prophecy tells of seven periods...",
            "translations": {"en": "The Seven Fires prophecy tells of seven periods in our history..."},
            "community_slug": "ojibwe-circle",
            "uploaded_by_email": "elder.migizi@ojibwe.firstvoice",
            "ai_training_allowed": False,
        },
        {
            "title": " birch bark canoe making",
            "language": "oji",
            "speaker_name": "David Thunderbird",
            "visibility": "public",
            "occasion": "Summer Gathering",
            "transcript": "You must find the right birch tree...",
            "translations": {"en": "You must find the right birch tree, one that has grown straight..."},
            "community_slug": "ojibwe-circle",
            "uploaded_by_email": "linguist.david@ojibwe.firstvoice",
            "ai_training_allowed": True,
        },
        {
            "title": "Whakapapa of Ngāti Porou",
            "language": "mri",
            "speaker_name": "Kaumātua Tane Mahuta",
            "visibility": "sacred",
            "occasion": "Marae Gathering",
            "transcript": "Tōku whakapapa ka huri mai i te whenua...",
            "translations": {"en": "My lineage comes from this land, from the first ancestors..."},
            "community_slug": "maori-archive",
            "uploaded_by_email": "kaumātua.tane@maori.firstvoice",
            "ai_training_allowed": False,
        },
        {
            "title": "Pōwhiri Protocol",
            "language": "mri",
            "speaker_name": "Whāea Hine Moana",
            "visibility": "public",
            "occasion": "Educational Workshop",
            "transcript": "When manuhiri arrive, the tangata whenua stand ready...",
            "translations": {"en": "When visitors arrive, the people of the land stand ready to welcome..."},
            "community_slug": "maori-archive",
            "uploaded_by_email": "whaea.hine@maori.firstvoice",
            "ai_training_allowed": True,
        },
        {
            "title": "The Story of Hiʻiaka",
            "language": "haw",
            "speaker_name": "Kupuna Makana Kāne",
            "visibility": "sacred",
            "occasion": "Makahiki Festival",
            "transcript": "ʻO Hiʻiaka ka wahine i ka uluwehi...",
            "translations": {"en": "Hiʻiaka is the woman of the forest..."},
            "community_slug": "hawaiian-council",
            "uploaded_by_email": "kupuna.makana@hawaiian.firstvoice",
            "ai_training_allowed": False,
        },
        {
            "title": "Heʻe Nalu (Surfing) Origins",
            "language": "haw",
            "speaker_name": "Lei Lokelani",
            "visibility": "public",
            "occasion": "Ocean Day",
            "transcript": "Surfing is not just sport, it is connection to the ocean...",
            "translations": {"en": "Surfing is not just sport, it is our connection to the ocean and the gods..."},
            "community_slug": "hawaiian-council",
            "uploaded_by_email": "director.lei@hawaiian.firstvoice",
            "ai_training_allowed": True,
        },
    ]

    for rd in recordings_data:
        community = communities[rd["community_slug"]]
        uploaded_by = users_by_email[rd["uploaded_by_email"]]
        rec_id = uuid.uuid4()
        key = f"recordings/{community.id}/{rec_id}.webm"

        r = Recording(
            id=rec_id,
            community_id=community.id,
            uploaded_by=uploaded_by.id,
            audio_file_key=key,
            language=rd["language"],
            title=rd["title"],
            occasion=rd["occasion"],
            visibility=rd["visibility"],
            ai_training_allowed=rd["ai_training_allowed"],
            speaker_name=rd["speaker_name"],
            transcript=rd["transcript"],
            translations=rd["translations"],
            transcription_status="completed",
            speaker_consent=True,
        )
        session.add(r)
        print(f"  Created recording: {r.title}")

    session.flush()

    # ── Audit Logs ──
    audit_actions = [
        {"action": "upload", "detail": "New recording uploaded"},
        {"action": "visibility_change", "detail": "Visibility changed to sacred"},
        {"action": "transcription_complete", "detail": "AI transcription finished"},
        {"action": "elder_approved", "detail": "Elder approved for public release"},
    ]

    for i, aud in enumerate(audit_actions):
        rec = session.query(Recording).order_by(Recording.created_at).offset(i % 5).first()
        if rec:
            a = AuditLog(
                id=uuid.uuid4(),
                recording_id=rec.id,
                user_id=rec.uploaded_by,
                action=aud["action"],
                new_value={"message": aud["detail"]},
            )
            session.add(a)

    session.commit()

    print("\n✅ Seed complete!")
    print(f"   Communities: {len(communities)}")
    print(f"   Users: {len(users_by_email)}")
    print(f"   Recordings: {len(recordings_data)}")
    print(f"   Audit Logs: {len(audit_actions)}")
    print("\n🔑 Elder Keys for demo login:")
    for u in users_by_email.values():
        if u.elder_key_token:
            print(f"   {u.name}: {u.elder_key_token}")

    session.close()


if __name__ == "__main__":
    seed()
