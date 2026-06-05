# FirstVoice

> **AI-native, community-controlled digital heritage platform.**
>
> Returning data sovereignty to Indigenous, endangered-language, and displaced communities.

## 🎬 Live Demo

- **Web App:** https://national-introductory-customs-started.trycloudflare.com (public demo)
- **API Docs:** https://gradually-reviews-damages-aberdeen.trycloudflare.com/docs (Swagger UI)
- **Landing Page:** https://national-introductory-customs-started.trycloudflare.com/landing

> ⚠️ These are temporary Cloudflare tunnel URLs for demo purposes. For a permanent deployment, we need MATIC for Polygon Amoy testnet + VPS hosting.

**Demo Elder Keys** (for login at `/login`):
- Cree: `8MnDY-TIm8Lp8uafw1cP1Zj0MFgYDn-spNHa4oAM9nE`
- Inuktitut: `mRrmXoowyG-bCR2YTGyqVj_SGUC0BrxYgMnoeZs5V7Q`
- Ojibwe: `2mokRpg7dLSnZ8rHfPJ4HuqK-9hJglJI_NBqxJ5kQmY`
- Māori: `89IEoGRExfirgUhtnC-vZwHproT-b8piSLFy_mXyPV4`
- Hawaiian: `RuCqUPEfd7YEk9hEuuf9XN2sxZuQwXlYUFkkn0cL1zY`

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

## 🚀 Quick Start

```bash
# 1. Clone
git clone https://github.com/ctmakc/firstvoice.git
cd firstvoice

# 2. Start infrastructure (Postgres + PostGIS, Redis, MinIO)
cd infra && docker compose up -d postgres redis minio

# 3. Install API dependencies
cd ../apps/api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 4. Configure environment
cp .env.example .env  # or use the provided .env
# Edit DATABASE_URL, REDIS_URL, MINIO_* as needed

# 5. Run migrations
alembic upgrade head

# 6. Seed demo data
python scripts/seed.py

# 7. Start API
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload

# 8. In another terminal, start web
cd ../web
pnpm install
pnpm dev --port 3001

# 9. Open the app
open http://localhost:3001        # Web PWA
open http://localhost:8001/docs   # API docs (Swagger)
```

### One-Command Full Stack (Docker)

```bash
cd infra
docker compose up -d --build
# App will be available at http://localhost:3050
```

## 📁 Project Structure

```
firstvoice/
├── apps/
│   ├── api/              # FastAPI backend (AI, Web3, admin, auth)
│   │   ├── src/
│   │   │   ├── main.py           # FastAPI app entry
│   │   │   ├── routers/          # API endpoints
│   │   │   ├── models/           # DB models + schemas
│   │   │   ├── services/         # AI + Web3 + storage
│   │   │   ├── middleware/       # Auth, rate limit, errors
│   │   │   └── workers/          # Celery tasks
│   │   ├── contracts/            # Hardhat + Solidity
│   │   ├── migrations/           # Alembic
│   │   └── scripts/seed.py       # Demo data
│   └── web/              # Next.js 16 PWA frontend
│       ├── src/
│       │   ├── app/              # App Router pages
│       │   ├── components/       # React components
│       │   └── hooks/            # useAuth, useApi
│       └── public/               # PWA manifest, service worker
├── infra/
│   └── docker-compose.yml  # One-command full stack
├── docs/
│   ├── PRD.md              # Product Requirements Document
│   ├── BUILD.md            # Technical Architecture
│   └── GRANTS.md           # Grant templates & tracker
└── .github/workflows/      # CI/CD
```

## 🌍 Target Communities

| Phase | Region | Languages | Grant Focus |
|-------|--------|-----------|-------------|
| **1** | 🇨🇦 Canada | Cree, Inuktitut, Ojibwe, Dene, Haida | SSHRC, Canadian Heritage ILP, First Nations Tech Council |
| **2** | 🇳🇿 New Zealand | Te Reo Māori | Te Taura Whiri, Callaghan Innovation |
| **3** | 🇺🇦 Ukraine | Crimean Tatar, Hutsul | Humanitarian tech, diaspora grants |

## ✨ Key Differentiators

- 🔒 **Sacred/Public Toggle** — No other platform lets communities gate AI training per-item
- 🗣️ **AI Voice Companion** — Fine-tuned TTS so the language can "speak" again
- ⛓️ **Non-speculative Web3** — Soulbound provenance tokens, zero speculation
- 📜 **OCAP-by-design** — Technical architecture enforces data sovereignty
- 🎁 **Grant-ready open source** — AGPL, built for institutional funding
- 📱 **Offline-First PWA** — Record in the bush, sync when back in town
- 🎙️ **Browser Recorder** — No app install required, works on any phone

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Next.js 16 (App Router), PWA, offline-first, plain CSS |
| **Backend** | FastAPI, async SQLAlchemy, PostgreSQL + PostGIS, Redis, MinIO |
| **AI** | faster-whisper (ASR), Gemini (translation/NLP), Coqui TTS / Piper |
| **Web3** | web3.py + Polygon Amoy (Soulbound ERC-721 provenance) |
| **Infra** | Docker Compose, Caddy, GitHub Actions CI/CD |

## ✅ MVP Status

### Completed
- [x] Docker Compose stack (Postgres + PostGIS, Redis, MinIO, API, Web, Celery Worker)
- [x] Database schema + Alembic migrations + comprehensive seed script
- [x] Auth middleware (NextAuth JWT + Elder Key header)
- [x] Recording upload with MinIO storage + presigned URLs
- [x] Community governance (invite, roles: elder/admin/member/superadmin)
- [x] Sacred/Public/Community-Review access control enforcement
- [x] AI transcription pipeline (faster-whisper)
- [x] AI translation + entity extraction (Gemini)
- [x] TTS scaffold (Coqui XTTS + Piper fallback)
- [x] Soulbound Provenance NFT contract (Solidity + Hardhat)
- [x] Web3 minting service (Polygon Amoy relayer)
- [x] PWA frontend with offline support (IndexedDB queue + service worker)
- [x] Browser audio recorder with WebM/Opus format
- [x] Full frontend pages: Feed, Communities, Community Detail, Recorder, Story Detail, Admin, Login, Landing
- [x] Admin moderation panel (approve/reject + provenance mint)
- [x] Audit log for all data changes
- [x] CI/CD (GitHub Actions: lint, typecheck, test, build)
- [x] AGPL-3.0 license

### Next Steps
- [ ] Deploy contract to Polygon Amoy testnet (needs MATIC faucet)
- [ ] i18n (EN / FR / Indigenous languages)
- [ ] Integration tests (pytest + Playwright)
- [ ] Real audio file generation for demo recordings
- [ ] Stripe billing for premium features
- [ ] Mobile app (Capacitor / React Native)

## 💰 Grant Fit

| Program | Amount | Fit |
|---------|--------|-----|
| SSHRC (Canada) | $150K–$400K | Indigenous research + digital humanities |
| Canadian Heritage ILP | $100K–$500K | Language revitalization tech |
| Te Taura Whiri (NZ) | NZ$50K–$300K | Māori digital tools |
| Filecoin Dev Grants | $5K–$50K | Decentralized storage |
| Gitcoin Grants | $10K–$100K | Open-source public good |
| Protocol Labs | $10K–$100K | Decentralized knowledge |

## 🤝 Contributing

We welcome contributors, especially:
- Indigenous community organizers and language keepers
- Computational linguists working on low-resource languages
- AI safety researchers focused on cultural bias
- Web3 developers building non-speculative tooling

See [docs/BUILD.md](docs/BUILD.md) for architecture details and [docs/GRANTS.md](docs/GRANTS.md) for funding strategy.

## 🧭 Principles

1. **Community-first** — Technology serves the community, never extracts from it
2. **OCAP-by-design** — Ownership, Control, Access, Possession are technical guarantees
3. **Open source** — AGPL, no paywalls, no proprietary lock-in
4. **No token speculation** — Governance-only, non-transferable tokens
5. **Offline-first** — Works in remote communities with intermittent connectivity

## 📄 License

[AGPL-3.0](LICENSE) — Data sovereignty includes software sovereignty.

---

*Built with respect for the voices that came before us.*
