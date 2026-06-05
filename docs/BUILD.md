# FirstVoice — BUILD Specification

> Technical blueprint for MVP (Months 1–2). Goal: **one language pilot, 50 hours recorded, grant demo ready**.

---

## 1. Tech Stack

| Layer | Tool | Version | Why |
|-------|------|---------|-----|
| **Frontend** | Next.js (App Router) | 16.x | PWA-ready, SSR, your proven stack |
| **Styling** | Plain CSS + CSS Modules | — | Design system consistency, no Tailwind bloat |
| **Backend API** | FastAPI | 0.115+ | Async Python, auto OpenAPI, AI ecosystem |
| **DB** | PostgreSQL | 16+ | Reliability, JSONB, pgvector (semantic search) |
| **Cache / Jobs** | Redis + Celery | 7.x / 5.x | Async transcription queue, offline sync |
| **Storage** | MinIO | latest | S3-compatible, self-hostable |
| **AI ASR** | faster-whisper | large-v3 | Local, fast, fine-tunable |
| **AI TTS** | Coqui TTS / Piper | latest | Lightweight, fine-tunable per speaker |
| **AI NLP** | Gemini (cloudcode-pa) | — | Translation, entity extraction, summaries |
| **Search** | pgvector + Postgres FTS | 0.7+ | No extra infra, vector search for semantic |
| **Web3** | Ethers.js | 6.x | Provenance minting on Polygon (testnet for MVP) |
| **Auth** | NextAuth.js v5 | beta | OAuth + custom Elder Key tokens |
| **PWA** | Serwist (next-pwa successor) | latest | Service worker, offline cache, background sync |
| **Infra** | Docker + Docker Compose | — | One-command local, VPS-ready |

---

## 2. Project Structure

```
firstvoice/
├── apps/
│   ├── web/                    # Next.js 16 PWA
│   │   ├── src/
│   │   │   ├── app/            # App Router
│   │   │   ├── components/     # UI kit (60+ components, reusable)
│   │   │   ├── hooks/          # useRecorder, useOffline, useAuth
│   │   │   ├── lib/            # API clients, utils, constants
│   │   │   └── types/          # Shared TS types
│   │   ├── public/             # Icons, manifest, SW
│   │   └── package.json
│   │
│   └── api/                    # FastAPI backend
│       ├── src/
│       │   ├── main.py
│       │   ├── config.py
│       │   ├── routers/
│       │   │   ├── auth.py
│       │   │   ├── recordings.py
│       │   │   ├── communities.py
│       │   │   ├── speakers.py
│       │   │   ├── transcription.py
│       │   │   ├── translation.py
│       │   │   └── provenance.py
│       │   ├── models/         # Pydantic + SQLAlchemy
│       │   ├── services/       # AI pipelines, storage, Web3
│       │   ├── workers/        # Celery tasks
│       │   └── alembic/        # Migrations
│       └── requirements.txt
│
├── packages/
│   └── shared-types/           # Zod + Pydantic shared schemas
│
├── infra/
│   ├── docker-compose.yml
│   ├── docker-compose.prod.yml
│   ├── nginx.conf
│   └── init-scripts/
│
├── docs/
│   ├── PRD.md
│   ├── BUILD.md
│   └── GRANTS.md               # Grant templates + tracker
│
├── models/                     # Fine-tuned AI models (Git LFS or separate)
└── README.md
```

---

## 3. MVP Scope (Weeks 1–6)

### Week 1: Foundation
- [ ] Repo scaffold (monorepo or separate repos? → **separate repos**, simpler grant demos)
- [ ] Docker Compose: Postgres + Redis + MinIO + API + Web
- [ ] Database schema + migrations (Alembic)
- [ ] Auth: NextAuth OAuth + Elder Key table
- [ ] Base layout, design tokens, typography

### Week 2: Recorder Core
- [ ] PWA manifest + Service Worker + offline queue
- [ ] `useRecorder` hook: MediaRecorder API, compressed audio (Opus/WebM → WAV)
- [ ] Upload queue: IndexedDB → background sync when online
- [ ] `/api/recordings` POST: receive + store in MinIO + enqueue transcription

### Week 3: AI Pipeline
- [ ] Celery worker: `faster-whisper` transcription
- [ ] Speaker diarization (pyannote.audio or whisperX)
- [ ] Gemini integration: translation (en/fr) + entity extraction
- [ ] `/api/transcription/{id}` GET: poll status
- [ ] Story Card UI: audio player + transcript + translation

### Week 4: Community Governance
- [ ] Community admin panel (/admin/community)
- [ ] Sacred/Public toggle on recording metadata
- [ ] Role-based access: viewer / recorder / reviewer / elder / admin
- [ ] Audit log: every visibility change recorded

### Week 5: Web3 Provenance (Light)
- [ ] Polygon Mumbai/Amoy testnet contract: SoulboundProvenanceNFT
- [ ] Mint on "publish" action (relayed, gasless for user)
- [ ] Store tx_hash in recording record

### Week 6: Polish + Pilot Prep
- [ ] i18n: English + French (for Canada) + Māori (for NZ prep)
- [ ] Mobile-first responsive (375px base)
- [ ] Accessibility: keyboard nav, ARIA labels, reduced motion
- [ ] Seed data: 5 demo stories in 1 language
- [ ] Grant demo script + video

---

## 4. API Specification

### 4.1 Recordings

```
POST   /api/v1/recordings              # Upload audio + metadata
GET    /api/v1/recordings              # List (filtered by community + visibility)
GET    /api/v1/recordings/{id}         # Detail with transcript + translation
PATCH  /api/v1/recordings/{id}         # Update visibility, tags, transcript corrections
DELETE /api/v1/recordings/{id}         # Soft delete (community admin only)
```

**POST /api/v1/recordings** Request:
```json
{
  "community_id": "uuid",
  "audio_file": "multipart/form-data",
  "metadata": {
    "language": "cre",
    "title": "Story of the Caribou",
    "occasion": "Winter Gathering",
    "location": { "lat": 52.1, "lng": -97.5 },
    "visibility": "sacred",
    "ai_training_allowed": false,
    "speaker_name": "Elder Mary"
  }
}
```

**Response:**
```json
{
  "id": "uuid",
  "status": "uploaded",
  "transcription_job_id": "celery-task-id",
  "audio_url": "https://minio/...",
  "created_at": "2026-06-04T..."
}
```

### 4.2 Transcription

```
GET /api/v1/transcription/{recording_id}/status
GET /api/v1/transcription/{recording_id}/result
```

**Result Response:**
```json
{
  "status": "completed",
  "transcript": "ᓂᐦᐃᔭᐍᐣ...",
  "transcript_latin": "nîhiya...",
  "segments": [
    { "start": 0.0, "end": 4.2, "text": "...", "speaker_id": "A" }
  ],
  "entities": [
    { "type": "person", "text": "Wîsakecâk", "start": 12.5 }
  ],
  "confidence": 0.87
}
```

### 4.3 Translation

```
POST /api/v1/translation
{
  "recording_id": "uuid",
  "target_language": "en",
  "context": "folklore"  // helps Gemini with cultural nuance
}
```

### 4.4 Communities

```
POST   /api/v1/communities              # Create (super admin)
GET    /api/v1/communities/{id}        # Public profile + language list
GET    /api/v1/communities/{id}/members # Admin only
POST   /api/v1/communities/{id}/invite # Admin invites user by email
PATCH  /api/v1/communities/{id}/policy  # Update data policy (council vote)
```

### 4.5 Provenance

```
POST /api/v1/provenance/mint
{
  "recording_id": "uuid",
  "community_address": "0x...",
  "metadata_uri": "ipfs://..."
}
```

---

## 5. Database Schema (PostgreSQL)

### 5.1 Core Tables

```sql
-- Communities
CREATE TABLE communities (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    slug VARCHAR(100) UNIQUE NOT NULL,
    territory_geo JSONB,              -- GeoJSON polygon
    languages VARCHAR(10)[],          -- ISO 639-3 codes
    data_policy VARCHAR(20) DEFAULT 'restricted', -- public | restricted | sacred_default
    council_members UUID[],           -- FK to users
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Users
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE,
    name VARCHAR(255),
    avatar_url TEXT,
    role VARCHAR(20) DEFAULT 'viewer', -- viewer | recorder | reviewer | elder | admin | superadmin
    community_id UUID REFERENCES communities(id),
    elder_key_token VARCHAR(64) UNIQUE, -- opaque token for API access
    oauth_provider VARCHAR(50),
    oauth_id VARCHAR(255),
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Recordings
CREATE TABLE recordings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    community_id UUID NOT NULL REFERENCES communities(id),
    uploaded_by UUID NOT NULL REFERENCES users(id),
    audio_file_key VARCHAR(500) NOT NULL,     -- MinIO object key
    duration_seconds INTEGER,
    format VARCHAR(10) DEFAULT 'webm',
    title VARCHAR(500),
    language VARCHAR(10) NOT NULL,
    transcript TEXT,
    transcript_latin TEXT,                    -- romanization if needed
    segments JSONB,                           -- [{start, end, text, speaker_id}]
    translations JSONB,                       -- {en: "...", fr: "..."}
    entities JSONB,                           -- [{type, text, start, end}]
    visibility VARCHAR(20) DEFAULT 'sacred',  -- public | sacred | restricted
    ai_training_allowed BOOLEAN DEFAULT FALSE,
    speaker_name VARCHAR(255),
    speaker_consent VARCHAR(20) DEFAULT 'pending', -- pending | explicit | inferred | withdrawn
    occasion VARCHAR(255),
    location_point GEOGRAPHY(POINT, 4326),
    provenance_tx_hash VARCHAR(66),
    provenance_token_id VARCHAR(100),
    transcription_status VARCHAR(20) DEFAULT 'pending', -- pending | processing | completed | failed
    created_at TIMESTAMPTZ DEFAULT now(),
    updated_at TIMESTAMPTZ DEFAULT now()
);

-- Audit Log (immutable)
CREATE TABLE audit_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID REFERENCES recordings(id),
    user_id UUID REFERENCES users(id),
    action VARCHAR(50) NOT NULL,         -- upload | visibility_change | delete | mint_provenance
    old_value JSONB,
    new_value JSONB,
    created_at TIMESTAMPTZ DEFAULT now()
);

-- Vector index for semantic search (pgvector)
CREATE TABLE recording_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    recording_id UUID REFERENCES recordings(id),
    embedding VECTOR(1536),              -- OpenAI text-embedding-3-small or local model
    content_type VARCHAR(20)             -- transcript | translation | summary
);
CREATE INDEX ON recording_embeddings USING ivfflat (embedding vector_cosine_ops);
```

---

## 6. AI Pipeline Architecture

### 6.1 Transcription Worker (Celery)

```python
# tasks/transcription.py
@app.task(bind=True, max_retries=3)
def transcribe_recording(self, recording_id: str):
    rec = get_recording(recording_id)
    audio_path = download_from_minio(rec.audio_file_key)
    
    # 1. Transcribe with faster-whisper
    model = get_whisper_model(rec.language)  # cached per language
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    # 2. Speaker diarization (whisperX)
    diarized = diarize(audio_path, segments)
    
    # 3. Update recording
    update_recording(recording_id, {
        "transcript": " ".join([s.text for s in segments]),
        "segments": [serialize(s) for s in diarized],
        "transcription_status": "completed",
        "confidence": info.language_probability
    })
    
    # 4. Enqueue translation + entity extraction
    translate_and_extract.delay(recording_id)
```

### 6.2 Translation + NLP Worker

```python
@app.task
def translate_and_extract(recording_id: str):
    rec = get_recording(recording_id)
    
    # Gemini for translation
    translations = {}
    for lang in ['en', 'fr']:
        translations[lang] = gemini_translate(
            rec.transcript, 
            source=rec.language, 
            target=lang,
            context=rec.occasion
        )
    
    # Gemini for entity extraction
    entities = gemini_extract_entities(rec.transcript, rec.language)
    
    update_recording(recording_id, {
        "translations": translations,
        "entities": entities
    })
    
    # Enqueue embedding index
    index_embedding.delay(recording_id)
```

### 6.3 TTS Fine-tuning (Future — Month 3+)

```python
# Manual pipeline per community
# 1. Collect 1+ hours of approved speaker audio
# 2. Preprocess (normalize, split)
# 3. Fine-tune Coqui TTS XTTS v2 on community data
# 4. Export ONNX for edge inference
# 5. Store model in MinIO, register in DB
```

---

## 7. PWA Requirements

### 7.1 Offline-First Flow

```
User opens app (no internet)
  → Service Worker serves cached shell
  → Recorder works fully offline (MediaRecorder + IndexedDB)
  → User records 3 stories
  → Background Sync API queues uploads
  → When connection returns: auto-uploads + enqueues transcription
```

### 7.2 Tech Implementation

- **Serwist** (next-pwa replacement) for SW generation
- **IndexedDB** (via idb-keyval) for audio blob queue
- **Background Sync API** for upload retry
- **Periodic Sync** (where supported) for content refresh
- **Network-first** for API calls, **cache-first** for static assets

### 7.3 Mobile Optimizations

- **Audio format:** Opus in WebM container (smallest, best quality)
- **Compression:** ffmpeg.wasm client-side if needed
- **Battery:** Batch uploads at night / on WiFi
- **Bandwidth:** Text-first story cards, audio on-demand

---

## 8. Web3 Integration (MVP Lite)

### 8.1 Smart Contract

```solidity
// SoulboundProvenance.sol
contract SoulboundProvenance is ERC721 {
    struct Provenance {
        bytes32 contentHash;      // SHA-256 of recording
        string community;           // Community name
        string language;            // ISO 639-3
        uint256 recordedAt;
        bool aiTrainingAllowed;
    }
    
    mapping(uint256 => Provenance) public provenance;
    
    function mint(
        address to,
        bytes32 contentHash,
        string memory community,
        string memory language,
        bool aiTrainingAllowed
    ) external returns (uint256 tokenId) {
        tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);  // _beforeTokenTransfer blocks transfers
        provenance[tokenId] = Provenance(...);
    }
    
    function _beforeTokenTransfer(...) internal override {
        require(from == address(0), "Soulbound: non-transferable");
        super._beforeTokenTransfer(...);
    }
}
```

### 8.2 Gasless Minting

- **Relayer:** OpenZeppelin Defender or custom relayer (backend pays gas)
- **User flow:** Community admin clicks "Mint Provenance" → backend sends tx → returns tx_hash
- **Cost:** ~$0.01-0.05 per mint on Polygon

### 8.3 MVP Limitation

- Provenance is **optional** per community
- Testnet only until mainnet funding secured
- No DeFi, no token economics, no speculation

---

## 9. Auth & Authorization

### 9.1 Auth Flow

```
User visits app
  → NextAuth OAuth (Google, GitHub, or custom) → creates User record
  → Checks if user has community invite
  → If invited → show community content
  → If not → show waitlist / public demo
```

### 9.2 Elder Key System

```
Community admin generates Elder Key (opaque 32-byte token)
  → Sends to new council member via secure channel (Signal, email)
  → Council member enters key → upgraded to 'elder' role
  → Elder Key has permissions: ["review", "publish", "invite", "admin"]
  → Rotatable if compromised
```

### 9.3 Permission Matrix

| Action | Viewer | Recorder | Reviewer | Elder | Admin | Superadmin |
|--------|--------|----------|----------|-------|-------|------------|
| View public stories | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| View sacred stories | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Record/upload | ❌ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Review/approve | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| Change visibility | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Invite members | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Mint provenance | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Delete/withdraw | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Create community | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ |

---

## 10. Infrastructure

### 10.1 Docker Compose (Local Dev)

```yaml
# docker-compose.yml
version: "3.8"
services:
  postgres:
    image: postgis/postgis:16-3.4
    environment:
      POSTGRES_DB: firstvoice
      POSTGRES_USER: fv
      POSTGRES_PASSWORD: devpass
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports: ["5433:5432"]

  redis:
    image: redis:7-alpine
    ports: ["6380:6379"]

  minio:
    image: minio/minio:latest
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: firstvoice
      MINIO_ROOT_PASSWORD: devpass123
    ports: ["9000:9000", "9001:9001"]
    volumes: ["minio_data:/data"]

  api:
    build: ./apps/api
    environment:
      DATABASE_URL: postgresql://fv:devpass@postgres:5432/firstvoice
      REDIS_URL: redis://redis:6379/0
      MINIO_ENDPOINT: minio:9000
      GEMINI_API_KEY: ${GEMINI_API_KEY}
    ports: ["8000:8000"]
    depends_on: [postgres, redis, minio]
    volumes:
      - whisper_models:/app/models

  web:
    build: ./apps/web
    environment:
      NEXTAUTH_SECRET: ${NEXTAUTH_SECRET}
      NEXTAUTH_URL: http://localhost:3000
      API_URL: http://api:8000
    ports: ["3000:3000"]
    depends_on: [api]

  worker:
    build: ./apps/api
    command: celery -A src.celery_app worker --loglevel=info --concurrency=2
    environment:
      DATABASE_URL: postgresql://fv:devpass@postgres:5432/firstvoice
      REDIS_URL: redis://redis:6379/0
      MINIO_ENDPOINT: minio:9000
      GEMINI_API_KEY: ${GEMINI_API_KEY}
    depends_on: [postgres, redis, minio]
    volumes:
      - whisper_models:/app/models
      - /dev/shm:/dev/shm  # Shared memory for Whisper
    deploy:
      resources:
        limits:
          memory: 4G

volumes:
  postgres_data:
  minio_data:
  whisper_models:
```

### 10.2 Production (VPS)

- **Host:** One of your empty VPSes (не freelance-docker, не docker-1)
- **Reverse proxy:** Caddy (auto HTTPS)
- **SSL:** Let's Encrypt via Caddy
- **Backup:** Daily pg_dump + MinIO mirror to cheap S3 (Wasabi/Backblaze)
- **Monitoring:** Uptime Kuma + basic logging

---

## 11. CI/CD

| Stage | Tool | What |
|-------|------|------|
| Lint | ESLint (web) + Ruff (api) | Pre-commit hooks |
| Type Check | tsc --noEmit + mypy | Strict mode |
| Test | Vitest (web) + pytest (api) | Unit + integration |
| Build | GitHub Actions | Docker images |
| Deploy | Self-hosted runner or SSH | VPS deploy |

### 11.1 GitHub Actions Workflow

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]
jobs:
  web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npm run lint
      - run: npm run typecheck
      - run: npm run test
      - run: npm run build
  api:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
      - run: pip install -r apps/api/requirements.txt
      - run: cd apps/api && ruff check .
      - run: cd apps/api && pytest
```

---

## 12. Test Strategy

### 12.1 Backend (pytest)

```
tests/
├── conftest.py              # Fixtures: db, client, minio mock
├── test_auth.py             # OAuth + Elder Key flows
├── test_recordings.py       # CRUD + visibility enforcement
├── test_transcription.py    # Mock whisper, test pipeline
├── test_communities.py      # RBAC, invites, policy changes
└── test_provenance.py       # Mock contract, test mint flow
```

### 12.2 Frontend (Vitest + Playwright)

```
tests/
├── unit/                    # Component logic, hooks
├── integration/             # API mocking, form flows
└── e2e/                     # Playwright: record → upload → review
```

### 12.3 Critical Paths to Test

1. Offline recording → online sync → transcription completes
2. Sacred flag blocks public API access (security)
3. Elder Key rotation doesn't break existing sessions
4. Provenance mint succeeds and tx_hash is stored
5. Community A cannot see Community B's sacred content

---

## 13. Performance Targets

| Metric | Target | Notes |
|--------|--------|-------|
| Time to interactive (PWA) | <2s on 4G | Lazy load audio player |
| Recording start latency | <500ms | MediaRecorder warm-up |
| Transcription (1 min audio) | <30s | faster-whisper on CPU |
| Transcription (batch) | <2h per 50 hours | Celery queue + GPU if available |
| API response (list) | <200ms | Paginated, cached |
| Upload (10MB audio) | <30s on 4G | Resumable multipart |

---

## 14. Security Checklist

- [ ] **CORS:** Strict origin whitelist
- [ ] **Rate limiting:** Redis-based per IP + per user
- [ ] **File validation:** Audio MIME type + magic bytes, max 100MB
- [ ] **SQL injection:** SQLAlchemy ORM only, no raw queries
- [ ] **XSS:** Content Security Policy, sanitize all user input
- [ ] **Secrets:** `.env` in Docker secrets, never in repo
- [ ] **Encryption:** Sacred audio encrypted at rest (AES-256-GCM)
- [ ] **Audit:** Every data access logged immutably
- [ ] **Consent:** Speaker consent tracked per recording, withdrawable

---

## 15. Next Steps (Immediate)

1. **Create repos:** `firstvoice-web` + `firstvoice-api` (private until MVP, then public)
2. **Set up dev environment:** `docker compose up` → all green
3. **Recruit Indigenous advisor:** Reach out to First Nations Tech Council or local Friendship Centre
4. **Pick pilot language:** Cree or Ojibwe (Canada) — largest grant potential
5. **Draft first grant:** SSHRC or Canadian Heritage ILP (deadlines usually fall/winter)

---

*BUILD Version: 1.0*
*Date: 2026-06-04*
*Status: Ready for scaffold*
