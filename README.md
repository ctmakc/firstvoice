# FirstVoice

> **AI-native, community-controlled digital heritage platform.**
>
> Returning data sovereignty to Indigenous, endangered-language, and displaced communities.

## The Problem

- **40% of the world's ~7,000 languages** are critically endangered
- One language dies every **2 weeks**
- Existing tools are passive archives — communities don't control their own stories
- Big Tech extracts data without respecting **OCAP** (Ownership, Control, Access, Possession)

## The Solution

FirstVoice combines:

1. **AI speech technology** — recording, transcription, text-to-speech, conversation
2. **Web3 provenance** — non-speculative, community-owned attribution
3. **Sacred governance** — communities decide what is public, what is sacred, who accesses it

### Core Loop

```
Community member records voice/story (mobile PWA)
         ↓
AI transcribes + translates + tags entities
         ↓
Community Council reviews → Public / Sacred / Restricted
         ↓
Public  → AI learning companion + map + school integration
Sacred  → Encrypted archive, council-controlled access
         ↓
Provenance NFT minted (non-transferable Soulbound)
```

## Quick Start

```bash
# 1. Clone
git clone https://github.com/ctmakc/firstvoice.git
cd firstvoice

# 2. Configure environment
cp .env.example .env
# Edit .env with your GEMINI_API_KEY, OAuth credentials, etc.

# 3. Start everything (Postgres + PostGIS, Redis, MinIO, API, Web, Worker)
cd infra && docker compose up -d --build

# 4. Run migrations
cd ../apps/api && alembic upgrade head

# 5. Seed demo data
python scripts/seed.py

# 6. Open the app
open http://localhost:3050        # Web PWA
open http://localhost:8010/docs   # API docs (Swagger)
```

## Project Structure

```
firstvoice/
├── apps/
│   ├── api/           # FastAPI backend (AI, Web3, admin, auth)
│   └── web/           # Next.js 16 PWA frontend
├── infra/
│   └── docker-compose.yml   # One-command local stack
├── docs/
│   ├── PRD.md         # Product Requirements Document
│   ├── BUILD.md       # Technical Architecture
│   └── GRANTS.md      # Grant templates & tracker
├── contracts/         # Soulbound Provenance NFT (Hardhat + Solidity)
└── .github/workflows/ # CI/CD
```

## Target Communities

| Phase | Region | Languages | Grant Focus |
|-------|--------|-----------|-------------|
| **1** | 🇨🇦 Canada | Cree, Inuktitut, Ojibwe, Dene, Haida | SSHRC, Canadian Heritage ILP, First Nations Tech Council |
| **2** | 🇳🇿 New Zealand | Te Reo Māori | Te Taura Whiri, Callaghan Innovation |
| **3** | 🇺🇦 Ukraine | Crimean Tatar, Hutsul | Humanitarian tech, diaspora grants |

## Key Differentiators

- 🔒 **Sacred/Public Toggle** — No other platform lets communities gate AI training per-item
- 🗣️ **AI Voice Companion** — Fine-tuned TTS so the language can "speak" again
- ⛓️ **Non-speculative Web3** — Soulbound provenance tokens, zero speculation
- 📜 **OCAP-by-design** — Technical architecture enforces data sovereignty
- 🎁 **Grant-ready open source** — AGPL, built for institutional funding

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16 (App Router), PWA, offline-first, plain CSS |
| **Backend** | FastAPI, async SQLAlchemy, PostgreSQL + PostGIS, Redis, MinIO |
| **AI** | faster-whisper (ASR), Gemini (translation/NLP), Coqui TTS / Piper |
| **Web3** | web3.py + Polygon Amoy (Soulbound ERC-721 provenance) |
| **Infra** | Docker Compose, Caddy, GitHub Actions CI/CD |

## MVP Status

### ✅ Completed
- [x] Docker Compose stack (Postgres + PostGIS, Redis, MinIO, API, Web, Celery Worker)
- [x] Database schema + Alembic migrations + seed script
- [x] Auth middleware (NextAuth JWT + Elder Key header)
- [x] Recording upload with MinIO storage
- [x] Community governance (invite, roles, policy, audit log)
- [x] Sacred/Public access control enforcement
- [x] AI transcription pipeline (faster-whisper)
- [x] AI translation + entity extraction (Gemini)
- [x] TTS scaffold (Coqui XTTS + Piper fallback)
- [x] Soulbound Provenance NFT contract (Solidity + Hardhat)
- [x] Web3 minting service (Polygon Amoy relayer)
- [x] PWA frontend shell with recorder component
- [x] CI/CD (GitHub Actions: lint, typecheck, test, build)
- [x] AGPL-3.0 license

### 🚧 In Progress / Next
- [ ] Full frontend pages (login, feed, recorder, story detail, admin)
- [ ] Offline sync (IndexedDB + Background Sync API)
- [ ] i18n (EN / FR)
- [ ] PWA manifest + service worker
- [ ] Deploy contract to Polygon Amoy testnet
- [ ] Integration tests (pytest + Playwright)

## Grant Fit

| Program | Amount | Fit |
|---------|--------|-----|
| SSHRC (Canada) | $150K–$400K | Indigenous research + digital humanities |
| Canadian Heritage ILP | $100K–$500K | Language revitalization tech |
| Te Taura Whiri (NZ) | NZ$50K–$300K | Māori digital tools |
| Filecoin Dev Grants | $5K–$50K | Decentralized storage |
| Gitcoin Grants | $10K–$100K | Open-source public good |
| Protocol Labs | $10K–$100K | Decentralized knowledge |

## Contributing

We welcome contributors, especially:
- Indigenous community organizers and language keepers
- Computational linguists working on low-resource languages
- AI safety researchers focused on cultural bias
- Web3 developers building non-speculative tooling

See [docs/BUILD.md](docs/BUILD.md) for architecture details and [docs/GRANTS.md](docs/GRANTS.md) for funding strategy.

## Principles

1. **Community-first** — Technology serves the community, never extracts from it
2. **OCAP-by-design** — Ownership, Control, Access, Possession are technical guarantees
3. **Open source** — AGPL, no paywalls, no proprietary lock-in
4. **No token speculation** — Governance-only, non-transferable tokens
5. **Offline-first** — Works in remote communities with intermittent connectivity

## License

[AGPL-3.0](LICENSE) — Data sovereignty includes software sovereignty.

---

*Built with respect for the voices that came before us.*
