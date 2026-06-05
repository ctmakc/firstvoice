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
| **Frontend** | Next.js 16 (App Router), PWA, offline-first |
| **Backend** | FastAPI, PostgreSQL + PostGIS, Redis, MinIO |
| **AI** | faster-whisper, Coqui TTS, Gemini |
| **Web3** | Ethers.js + Polygon (Soulbound provenance) |
| **Infra** | Docker Compose, Caddy, self-hosted |

## MVP Status

See [`docs/BUILD.md`](docs/BUILD.md) for technical specification.

### MVP Roadmap (6 weeks)

- [ ] Week 1: Foundation — Docker, DB schema, auth, Elder Key system
- [ ] Week 2: Recorder — Mobile PWA, offline queue, audio upload
- [ ] Week 3: AI Pipeline — Whisper transcription, speaker diarization, Gemini NLP
- [ ] Week 4: Governance — Sacred/Public toggle, community admin panel, audit log
- [ ] Week 5: Provenance — Soulbound NFT minting (testnet, gasless)
- [ ] Week 6: Pilot Prep — i18n, accessibility, seed data, grant demo

## Grant Fit

| Program | Amount | Fit |
|---------|--------|-----|
| SSHRC (Canada) | $150K–$400K | Indigenous research + digital humanities |
| Canadian Heritage ILP | $100K–$500K | Language revitalization tech |
| Te Taura Whiri (NZ) | NZ$50K–$300K | Māori digital tools |
| Filecoin Dev Grants | $5K–$50K | Decentralized storage |
| Gitcoin Grants | $10K–$100K | Open-source public good |
| Protocol Labs | $10K–$100K | Decentralized knowledge |

## Getting Started

```bash
# Clone repos (coming soon)
git clone https://github.com/ctmakc/firstvoice-web.git
git clone https://github.com/ctmakc/firstvoice-api.git

# Start everything
cd firstvoice-api && docker compose up -d
```

## Principles

1. **Community-first** — Technology serves the community, never extracts from it
2. **OCAP-by-design** — Ownership, Control, Access, Possession are technical guarantees
3. **Open source** — AGPL, no paywalls, no proprietary lock-in
4. **No token speculation** — Governance-only, non-transferable tokens
5. **Offline-first** — Works in remote communities with intermittent connectivity

## License

AGPL-3.0 — Data sovereignty includes software sovereignty.

---

*Built with respect for the voices that came before us.*
