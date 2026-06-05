#!/usr/bin/env python3
import sys
import os

# Ensure src is importable when running from scripts/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from sqlalchemy.orm import sessionmaker
from src.database import sync_engine, Base
from src.models.db_models import Community, User
import uuid


Session = sessionmaker(bind=sync_engine)


def seed() -> None:
    Base.metadata.create_all(bind=sync_engine)
    session = Session()

    existing = session.query(Community).filter_by(slug="cree-pilot").first()
    if existing:
        print("Seed data already present (community slug='cree-pilot').")
        session.close()
        return

    community = Community(
        id=uuid.uuid4(),
        name="Cree First Nation",
        slug="cree-pilot",
        languages=["cre"],
        data_policy="restricted",
    )
    session.add(community)
    session.flush()

    admin = User(
        id=uuid.uuid4(),
        email="admin@cree-pilot.firstvoice",
        name="Demo Admin",
        role="admin",
        community_id=community.id,
    )
    elder = User(
        id=uuid.uuid4(),
        email="elder@cree-pilot.firstvoice",
        name="Demo Elder",
        role="elder",
        community_id=community.id,
    )
    session.add(admin)
    session.add(elder)
    session.commit()

    print(f"Seeded community {community.id} ({community.name})")
    print(f"  Admin user: {admin.id} ({admin.email})")
    print(f"  Elder user: {elder.id} ({elder.email})")
    session.close()


if __name__ == "__main__":
    seed()
