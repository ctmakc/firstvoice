# FirstVoice Aotearoa — One-Page Summary

**For:** Te Mātāwai 2026-2027 Investment Round  
**Amount Requested:** NZ$90,000  
**Duration:** 12 months (July 2026 – June 2027)  
**Contact:** Maksym Stepanenko, maksym@firstvoice.dev

---

## In One Sentence

FirstVoice is an AI-native, community-controlled digital heritage platform that lets Māori elders record stories in te reo Māori, have them automatically transcribed and translated, and decide — story by story — what is public, what is sacred, and whether AI may learn from their voice.

## The Problem

- 40% of the world's 7,000 languages are critically endangered
- Te reo Māori faces ongoing decline in daily speakers
- Existing digital tools **extract** community data without returning control
- Archives store recordings on servers communities don't own, under terms they didn't write
- There is **zero** existing platform that lets communities gate AI training per-item

## Our Solution

**Three pillars, one platform:**

| Pillar | Technology | Community Outcome |
|--------|-----------|-------------------|
| **🎙️ Record** | Browser audio recorder + offline-first PWA | Elders record on any phone, no app install |
| **🧠 Understand** | Fine-tuned Whisper ASR + Gemini translation | Automatic transcription + English translation + entity tagging |
| **🔒 Govern** | Sacred/Public toggle + Elder approval + Blockchain provenance | Community council controls every recording. AI training gated per-item. Immutable attribution on Polygon. |

## OCAP-by-Design

FirstVoice enforces **Ownership, Control, Access, Possession** at the technical level:

- **Ownership:** Communities hold encryption keys for sacred recordings
- **Control:** Visibility (Sacred / Community-Review / Public) set per recording by community council
- **Access:** Elder key authentication — only council members can approve public release
- **Possession:** All data stored in community-chosen jurisdiction (MinIO S3-compatible, self-hostable)

## 12-Month Pilot Plan

| Month | Activity | Deliverable |
|-------|----------|-------------|
| 1–2 | Community hui + co-design with 2 iwi/hapū | Signed partnership agreements + governance protocols |
| 3–4 | Platform localisation (te reo UI + cultural metadata) | Localised MVP |
| 5–6 | Elder training + recording workshops | 50+ recordings uploaded |
| 7–8 | AI fine-tuning on community-validated transcripts | ASR model achieving >70% accuracy |
| 9–10 | Community review + iteration | Elder feedback incorporated |
| 11–12 | Evaluation + open-source release | Public codebase + evaluation report |

## Team

| Role | Person | Expertise |
|------|--------|-----------|
| **Technologist / Lead** | Maksym Stepanenko | Full-stack + AI/ML (10+ years) |
| **Māori Advisor** | [To be recruited] | Iwi liaison + cultural protocol |
| **Computational Linguist** | [To be recruited] | Te reo Māori NLP + ASR |
| **Community Coordinator** | [To be recruited] | Marae-based facilitation |

## Budget (NZ$90,000)

| Category | Amount |
|----------|--------|
| Community co-design (2 communities) | $25,000 |
| AI/ML development | $20,000 |
| Platform engineering | $25,000 |
| Cloud infrastructure | $8,000 |
| Project management | $7,000 |
| Open-source release | $5,000 |

## Why Now

1. **AI speech technology has crossed a threshold** — Whisper ASR works on low-resource languages with small fine-tuning datasets
2. **Web3 provenance is mature** — Polygon Amoy testnet + Soulbound NFTs provide non-speculative attribution
3. **Funding climate is right** — Te Mātāwai, MBIE, and international donors are actively seeking Indigenous-led tech solutions
4. **Open-source infrastructure exists** — FirstVoice MVP is already built (FastAPI + Next.js + Docker). Pilot = localisation + community partnership.

## Live Demo

**MVP running now:** http://localhost:3001 (local development)  
**Source code:** https://github.com/ctmakc/firstvoice  
**License:** AGPL-3.0 (no paywalls, no proprietary lock-in)

## Contact

📧 maksym@firstvoice.dev  
🔗 github.com/ctmakc/firstvoice  

---

*Built with respect for the voices that came before us.*
