# FirstVoice — Product Requirements Document

## 1. Vision Statement

**FirstVoice** is an AI-native, community-controlled digital heritage platform that returns data sovereignty to Indigenous, endangered-language, and displaced communities. It combines:

- **AI speech technology** (recording, transcription, text-to-speech, conversation)
- **Web3 provenance** (non-speculative, community-owned attribution)
- **Sacred governance** (communities decide what is public, what is sacred, who accesses it)

> *"Not an archive. Not a museum. A living voice controlled by the people it belongs to."*

---

## 2. Problem Analysis

### 2.1 Language Extinction Crisis
- **40% of the world's ~7,000 languages** are critically endangered
- One language dies approximately every **2 weeks**
- When a language dies, an entire worldview, legal system, medicinal knowledge, and oral history die with it

### 2.2 Existing Solutions Are Broken
| Existing Tool | Why It Fails |
|--------------|--------------|
| Wikitongues | Passive video archive, no AI, no community governance |
| ELAR (Endangered Languages Archive) | Academic-controlled, complex access, extractive |
| Rosetta Stone / Duolingo | Only commercially viable languages, no Indigenous content |
| Generic cloud storage | Communities lose control, no cultural context, no provenance |

### 2.3 The OCAP Gap
**OCAP Principles** (Ownership, Control, Access, Possession) are the gold standard for Indigenous data governance. No existing platform implements all four technically.

### 2.4 Why Now
- **AI speech models** (Whisper, Coqui TTS) have democratized to the point where a small team can fine-tune for low-resource languages
- **Web3 infrastructure** (Filecoin, Tezos) provides censorship-resistant, long-term storage without corporate gatekeeping
- **Grant environment** is flush with reconciliation, language revitalization, and AI-for-good funding (2026-2027)

---

## 3. Target Communities

### Phase 1: Turtle Island (Canada) — Months 1-3
- **70+ Indigenous languages** in various states of endangerment
- Massive grant availability via Canadian Heritage, SSHRC, First Nations Tech Council
- Truth and Reconciliation Commission **Call to Action #13-17** explicitly demands language revitalization tech
- Existing relationships possible through Métis Nation, Inuit Tapiriit Kanatami, AFN

### Phase 2: Aotearoa (New Zealand) — Months 4-6
- **Te Reo Māori** — official language but still endangered in daily use
- **Te Taura Whiri i te Reo Māori** (Māori Language Commission) actively funds digital tools
- **Callaghan Innovation** + **Te Māngai Pāho** seeking tech partners
- NZ government has explicit **Treaty of Waitangi** obligations to protect Māori culture

### Phase 3: Ukraine — Months 6-9
- **Crimean Tatar**, **Hutsul dialects**, **Lemko**, **Rusyn** — endangered due to displacement and Russification
- If geopolitical situation worsens, digital preservation becomes critical
- Ukrainian diaspora communities in Canada create natural bridge

---

## 4. Product Overview

### 4.1 Core Loop
```
Community Elder/Youth → Records voice/story (mobile PWA)
         ↓
AI transcribes + translates + tags entities
         ↓
Community Council reviews → approves Public / Sacred / Restricted
         ↓
Public → AI learning companion + map + school integration
Sacred → Encrypted archive, accessible only to authorized members
         ↓
Provenance NFT minted (non-transferable, attesting origin)
```

### 4.2 Key Differentiators
1. **Sacred/Public Toggle** — No other platform lets communities gate AI training and public access per-item
2. **AI Voice Companion** — Fine-tuned TTS means the language can "speak" again, even with few living speakers
3. **Non-speculative Web3** — Provenance tokens are Soulbound (non-transferable), no crypto speculation
4. **OCAP-by-design** — Technical architecture enforces Ownership/Control, not just policy documents
5. **Grant-ready open source** — AGPL or similar, built for institutional funding, not VC

---

## 5. Feature Specification

### MVP — Months 1-2 (Grant Demo Ready)

| Feature | User Story | Acceptance Criteria |
|---------|-----------|---------------------|
| **Mobile PWA Recorder** | As a community member, I open the app on my phone, hit one button, and record a story in my language, even offline | Works on Android/iOS browser, <3s to start recording, offline queue syncs when connected |
| **AI Transcription** | As a recorder, I see a transcript of my speech in the original language within 30 seconds | Whisper fine-tuned per language, speaker diarization, confidence score shown |
| **Translation Layer** | As a learner, I can read an English/French/Māori translation of the story | Gemini API for draft translation, community admin can edit/correct |
| **Sacred/Public Toggle** | As an Elder, I mark a recording as "Sacred — not for public AI training" | Flag stored in metadata, AI pipeline respects it, public API filters it out |
| **Story Cards** | As a visitor, I browse stories with audio + transcript + speaker name + photo | Beautiful, respectful card design, no autoplay, explicit consent for every media element |
| **Community Admin Panel** | As a council member, I invite users, review uploads, set visibility, export community data | Role-based access, bulk operations, audit log of every decision |

### V1 — Months 3-4 (Pilot Expansion)

| Feature | Description |
|---------|-------------|
| **AI Voice Companion** | Text-to-speech in the endangered language using fine-tuned Coqui TTS. Type a phrase → hear it spoken. |
| **Ancestral Map** | Stories geo-tagged on traditional territory map (Mapbox/Leaflet with Indigenous basemaps). Spatial audio — stories trigger when entering territory. |
| **Material Culture** | Upload photos of crafts, regalia, tools. AI generates descriptive metadata. Optional: 3D scan integration (photogrammetry via Polycam API). |
| **DAO-lite Governance** | Snapshot-style voting for: Which language to prioritize? Should a story go public? Who gets Elder Key? No financial tokens. |
| **School Mode** | Simplified UI for K-12 Indigenous immersion classrooms. Teacher dashboard, student progress, AI conversation partner with safety guardrails. |

### V2 — Months 5-6 (Scale)

| Feature | Description |
|---------|-------------|
| **Immersion Conversations** | AI chatbot that speaks the endangered language, adjusts difficulty, corrects pronunciation via speech recognition |
| **Cross-Community Federation** | Communities can share non-sacred language data peer-to-peer, building larger corpora while retaining local control |
| **Decentralized Storage** | IPFS for public content, encrypted Filecoin deals for sacred archives, local air-gapped node option |
| **Offline AI** | Core transcription and TTS models downloadable for completely offline operation (no internet = no surveillance) |

---

## 6. Technical Architecture

### 6.1 Stack

| Layer | Technology | Rationale |
|-------|-----------|-----------|
| **Frontend** | Next.js 16 (App Router), TypeScript, plain CSS (no Tailwind) | Your proven stack, fast, PWA-ready |
| **Backend API** | FastAPI (Python) | AI/ML ecosystem, async, OpenAPI |
| **Database** | PostgreSQL + PostGIS (for map) | Reliability, geospatial, JSONB for metadata |
| **Cache / Queue** | Redis + Celery | Async transcription jobs, offline sync |
| **Object Storage** | MinIO (S3-compatible) | Self-hostable, community can own infrastructure |
| **AI Inference** | Whisper (faster-whisper), Coqui TTS, Gemini | Best-in-class low-resource language support |
| **Web3** | Ethers.js + Polygon or Tezos | Low fees, eco-friendly, provenance use case |
| **Search** | Meilisearch or pgvector | Full-text across transcripts, semantic search |

### 6.2 Data Model (Core)

```
Community
├── id, name, territory_geo, council_members[]
├── languages[] (ISO 639-3 code)
├── data_policy: public | restricted | sacred_default
└── settings: auto_approve, review_required

Recording
├── id, community_id, uploaded_by
├── audio_file_url, duration, format
├── transcript (original language)
├── translations { en: "...", fr: "..." }
├── entities[] (people, places, plants, animals)
├── visibility: public | sacred | restricted
├── ai_training_allowed: bool (default FALSE)
├── provenance_tx_hash (Web3)
├── speaker_consent: explicit | inferred | withdrawn
└── metadata: occasion, date_recorded, location

Speaker
├── id, name_public, name_internal (optional)
├── community_id, role: elder | youth | learner
├── voice_samples[] (for TTS fine-tuning, consent required)
└── consent_receipt_url

ElderKey
├── token (opaque), community_id, issued_to
├── permissions[]: review | publish | invite | admin
└── expires_at
```

### 6.3 AI Pipeline

```
Audio Upload
    ↓
[faster-whisper] → Transcript + Timestamps + Speaker IDs
    ↓
[Gemini] → Translation + Named Entity Extraction + Summary
    ↓
[Community Review] → Visibility + AI_training flag set
    ↓
If public:
    [Coqui TTS] → Fine-tune voice model (if speaker consented)
    [pgvector] → Index for semantic search
    [IPFS pin] → Decentralized backup
If sacred:
    [Encrypt] → AES-256, key held by community council
    [Filecoin deal] → Encrypted, retrievable only with council multi-sig
```

---

## 7. Web3 & Data Sovereignty Design

### 7.1 OCAP Technical Enforcement

| Principle | Technical Implementation |
|-----------|-------------------------|
| **Ownership** | Community owns encryption keys; platform operator (us) cannot decrypt sacred content |
| **Control** | Smart contract governs access policy changes; council multi-sig required |
| **Access** | API keys scoped per community; rate-limited; audit log immutable on-chain |
| **Possession** | Monthly automated export to community-controlled S3/MinIO + optional local node |

### 7.2 Provenance NFT (Soulbound)

- **Standard:** ERC-721 or Tezos FA2
- **Transferability:** NONE (Soulbound)
- **Metadata:** Recording hash, community, date, language, consent status
- **Purpose:** Tamper-proof attestation of origin for legal/cultural claims, NOT speculation
- **Cost:** Subsidized by platform (gasless minting via relayer)

### 7.3 Governance (No Financial Tokens)

- **Voting:** Snapshot-style off-chain voting, signed by Elder Key holders
- **Actions:** Change visibility, approve new members, set AI training policy, allocate storage budget
- **Quorum:** Configurable per community (e.g., 3 of 5 council members)
- **No token economics** — avoids securities regulation, maintains grant eligibility

---

## 8. Grant Strategy

### 8.1 Grant Fit Matrix

| Program | Geography | Amount | Timeline | Fit Score |
|---------|-----------|--------|----------|-----------|
| **SSHRC Insight/Connection** | Canada | $150K–$400K | 12–24 mo | ★★★★★ |
| **Canadian Heritage ILP** | Canada | $100K–$500K | Annual | ★★★★★ |
| **First Nations Tech Council** | BC Canada | $50K–$200K | Rolling | ★★★★☆ |
| **Te Taura Whiri i te Reo Māori** | NZ | NZ$50K–$300K | Annual | ★★★★★ |
| **Callaghan Innovation R&D** | NZ | $50K–$500K | 6–18 mo | ★★★★☆ |
| **Filecoin Dev Grants** | Global | $5K–$50K | 6–8 wk | ★★★★☆ |
| **Protocol Labs (IPFS)** | Global | $10K–$100K | Rolling | ★★★★☆ |
| **Tezos Foundation** | Global | $10K–$100K | Rolling | ★★★★☆ |
| **Gitcoin Grants** | Global | $10K–$100K | Quarterly | ★★★★☆ |
| **Anthropic AI Safety** | Global | $50K–$200K | Rolling | ★★★☆☆ |
| **Mozilla MOSS** | Global | $10K–$50K | Rolling | ★★★★☆ |

### 8.2 Grant Narrative Anchors
1. **Reconciliation / Decolonization** — "Technology as restoration, not extraction"
2. **AI for Marginalized Languages** — "Whisper was trained on English; we're fine-tuning it on Dene"
3. **Data Sovereignty** — "OCAP-by-design, not by policy paper"
4. **Open Source Public Good** — "GPL/AGPL, no paywalls, no extraction"
5. **Climate + Culture** — "Oral history contains 10,000 years of ecological knowledge"

---

## 9. Business Model & Sustainability

### Phase 1: Grant-Funded (Months 0–18)
- 100% development funded by grants
- Open-source core released immediately
- Hosted SaaS free for underserved communities

### Phase 2: Hybrid (Months 18–36)
- **Free tier:** Core recording + transcription + small storage
- **Sponsored tier:** Museums, universities, government language programs pay for white-label + support
- **Enterprise tier:** National language commissions (e.g., Canadian Heritage) fund nationwide rollout
- **NO venture capital** — avoids pressure to monetize user data

### Phase 3: Foundation (Year 3+)
- Independent non-profit or B Corp
- Endowment from large grants + institutional contracts
- Community revenue-sharing if commercial use of voice data (with explicit consent)

---

## 10. Success Metrics (KPIs)

### Year 1
| Metric | Target |
|--------|--------|
| Languages onboarded | 5 (Canada: 3, NZ: 1, Ukraine: 1) |
| Hours of audio recorded | 500+ |
| Community members active | 200+ |
| Elders/council trained as admins | 50+ |
| AI TTS voices deployed | 5+ |
| Grant funding secured | $500K+ CAD |
| Open-source GitHub stars | 500+ |

### Year 2
| Metric | Target |
|--------|--------|
| Languages | 25 |
| Hours | 5,000 |
| Communities | 50 |
| School integrations | 20 |
| Self-hosted instances | 10 |

---

## 11. Risk Analysis

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| **Community distrust** | Medium | Critical | Indigenous advisory board from Day 1; OCAP-first design; no data leaves community without explicit consent |
| **Sacred content misuse** | Medium | Critical | Sacred flag enforced at API level; no AI training on sacred; community veto power; digital watermarking |
| **Grant dependency** | High | High | Dual-track: grants + SaaS revenue; maintain low burn; build toward institutional contracts |
| **Low-resource AI failure** | Medium | High | Fallback to human transcription pipeline; incremental AI improvement; partner with linguistics departments |
| **Web3 stigma** | Medium | Medium | Call it "provenance" not "crypto"; use Tezos (eco-friendly) or Polygon (low fees); no financial tokens |
| **Technical complexity** | Medium | Medium | MVP is simple recorder + Whisper; Web3 only for provenance hash; defer decentralized storage to V2 |
| **Ukrainian political sensitivity** | Low | Medium | Frame as cultural preservation, not political; partner with academic institutions, not partisan groups |

---

## 12. Team & Partnerships

### Core Team (Immediate)
| Role | Who | Responsibility |
|------|-----|---------------|
| **Founding Technologist** | Maksym | Full-stack, AI pipeline, architecture, DevOps |
| **Product/Grant Lead** | Maksym | PRD, grant writing, partnerships |

### To Recruit (Month 1-2)
| Role | Profile | How |
|------|---------|-----|
| **Indigenous Advisor** | Community organizer, tech-savvy, from target community | Outreach via First Nations Tech Council, Native Youth in STEM |
| **Computational Linguist** | PhD or MA in endangered languages, Python/ML experience | University partnerships (UBC, McGill, Victoria for Canada; Otago, Auckland for NZ) |
| **Community UX Researcher** | Experience in participatory design with Indigenous communities | Contract basis, remote |
| **Grant Writer (contract)** | SSHRC/Canadian Heritage experience | Upwork or academic network |

### Strategic Partners
- **Universities:** UBC Indigenous Studies, University of Victoria Linguistics, AUT NZ (Māori research)
- **NGOs:** Wikitongues (data partnership, not platform), First Peoples' Cultural Council (BC)
- **Tech:** HuggingFace (model hosting), Coqui (TTS), Filecoin Foundation (storage)

---

## 13. Roadmap

| Phase | Timeline | Deliverable | Grant Milestone |
|-------|----------|-------------|-----------------|
| **Foundation** | Weeks 1–2 | PRD, BUILD, repo scaffold, advisory board recruitment | — |
| **MVP Core** | Weeks 3–6 | PWA recorder + transcription + community panel + 1 language pilot | Seed grant demo |
| **Pilot** | Weeks 7–10 | Onboard 1 Canadian First Nation community, 50 hours recorded, feedback loop | Pilot report |
| **AI V1** | Months 3–4 | TTS voice clone, ancestral map, school mode | Expansion grant |
| **NZ Bridge** | Months 4–5 | i18n (Māori UI), Te Taura Whiri outreach, 1 iwi pilot | NZ partnership grant |
| **Open Source** | Month 5 | Public release, documentation, HuggingFace models | Community grant |
| **Ukraine Prep** | Month 6 | Crimean Tatar corpus prep, diaspora outreach | Humanitarian tech grant |
| **Scale** | Months 7–12 | 5 languages, 500 hours, $500K grants, 5 TTS voices | Major grant reporting |

---

## 14. Appendices

### A. Language Priority Shortlist (Canada)
1. **Cree** — 100K+ speakers but declining, massive corpus potential, strong institutional support
2. **Inuktitut** — Official language in Nunavut, government funding available
3. **Ojibwe/Ojibway** — Active revitalization movement in Ontario/Manitoba
4. **Dene** — Complex phonology, good test for AI low-resource performance
5. **Haida** — Critically endangered (<10 speakers), high symbolic value

### B. Language Priority Shortlist (NZ)
1. **Te Reo Māori** — Strong institutional support, large learner community, iwi partnerships open

### C. Language Priority Shortlist (Ukraine)
1. **Crimean Tatar** — Displaced, politically sensitive, strong diaspora in Canada
2. **Hutsul dialects** — Carpathian cultural heritage, tourism crossover potential

### D. Tech Principles
1. **Offline-first** — Communities in remote areas have intermittent connectivity
2. **Low-bandwidth** — Audio compression, progressive download, text-first fallbacks
3. **Accessibility** — WCAG 2.1 AA, screen reader support, dyslexia-friendly fonts
4. **Battery-conscious** — Background recording optimization, batch upload at night
5. **Security-by-default** — E2E encryption for sacred content, no telemetry without consent

---

*PRD Version: 1.0*
*Date: 2026-06-04*
*Next: BUILD.md technical specification*
