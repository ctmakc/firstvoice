# SSHRC Insight Development Grant — FirstVoice Proposal

## Program
**SSHRC Insight Development Grants**  
Amount: $50,000 – $150,000 CAD  
Duration: 1–2 years  
Deadline: Rolling (next intake: Fall 2026)  
URL: https://www.sshrc-crsh.gc.ca/funding-financement/programs-programmes/insight_development-savoir-engagement-engagement_savoir-eng.aspx

---

## 1. Project Title

**FirstVoice: A Community-Controlled AI-Native Platform for Indigenous Language Revitalization**

---

## 2. Lay Summary (150 words)

Over 70 Indigenous languages in Canada are critically endangered. Existing digital archives extract community data without returning control. FirstVoice is an open-source platform that combines AI speech technology (automatic transcription, translation, text-to-speech), Web3 provenance (tamper-proof attribution), and sacred governance (community-controlled access) to return data sovereignty to Indigenous communities. Unlike passive archives, FirstVoice is a living platform where communities decide what is public, what is sacred, and who can access it. OCAP principles (Ownership, Control, Access, Possession) are enforced at the technical level, not just in policy documents. This project will pilot FirstVoice with two First Nations communities, evaluate AI performance on low-resource languages, and co-design governance mechanisms with Indigenous advisors.

---

## 3. Research Objectives

### Primary Questions
1. How can fine-tuned ASR/TTS models perform on low-resource Indigenous languages with limited training data?
2. What technical mechanisms best enforce OCAP principles in digital heritage platforms?
3. How does community governance of sacred vs. public cultural data affect trust, participation, and language revitalization outcomes?

### Secondary Questions
4. Can decentralized provenance (blockchain-based attribution) provide legally meaningful evidence of cultural origin?
5. What UI/UX patterns best serve intergenerational knowledge transfer in remote communities?

---

## 4. Methodology

### Phase 1: Community Co-Design (Months 1–4)
- **Participatory design workshops** with 2 First Nations communities (target: Cree in Ontario/Manitoba, Haida in BC)
- Indigenous advisory board recruitment via First Nations Tech Council, Native Youth in STEM
- Co-design sessions: sacred/public classification UX, elder approval workflows, language-specific UI
- Deliverable: Community requirements document + signed data sharing agreements

### Phase 2: Technical Development (Months 3–12)
- **ASR fine-tuning**: faster-whisper large-v3 fine-tuned on community-collected audio (target: <10 hours for basic functionality)
- **TTS voice cloning**: Coqui XTTS v2 trained on approved speaker samples
- **Translation pipeline**: Gemini API with cultural context injection (occasion metadata)
- **Governance layer**: Smart contract (Soulbound NFT) deployment on Polygon Amoy testnet → mainnet evaluation
- **Decentralized storage**: IPFS/Filecoin integration for public content; encrypted local nodes for sacred archives
- Deliverable: Functional platform v1.0 with 2 language pilots

### Phase 3: Evaluation (Months 10–18)
- **Linguistic accuracy benchmarks**: WER (Word Error Rate) per language, BLEU score for translations
- **Trust surveys**: Pre/post pilot community trust in digital preservation (adapted from OCAP Trust Index)
- **Participation metrics**: Active recorders, hours recorded, intergenerational usage patterns
- **Legal review**: Provenance NFT admissibility for cultural claims (partner with Indigenous law faculty)
- Deliverable: Evaluation report + open-source release + academic paper

---

## 5. Theoretical Framework

### OCAP (Ownership, Control, Access, Possession)
Developed by the First Nations Information Governance Centre (FNIGC), OCAP is the gold standard for Indigenous data governance. FirstVoice is the first digital heritage platform to implement all four principles at the technical architecture level:
- **Ownership**: Community controls encryption keys for sacred content
- **Control**: Smart contract governance for policy changes (multi-sig elder council)
- **Access**: Role-based API permissions with immutable audit logs
- **Possession**: Monthly automated exports to community-controlled storage + optional local node

### Critical Data Studies + Indigenous Data Sovereignty
Drawing on Daly et al. (2021) on Indigenous data governance and Couldry & Mejias (2019) on data colonialism, this project positions technology as a decolonizing tool rather than an extractive one.

---

## 6. Expected Outcomes

### Academic
- 1 peer-reviewed paper in *Language Documentation & Conservation* or *Digital Humanities Quarterly*
- 1 conference presentation at ACL (computational linguistics) or NAISA (Native American and Indigenous Studies)
- Open-source codebase under AGPL-3.0

### Community
- 2 functional language preservation platforms (community-managed)
- 50+ hours of recorded audio per pilot community
- Trained community administrators (5–10 per community)
- Public language learning companion (TTS-based) for community schools

### Policy
- OCAP implementation blueprint for digital heritage platforms
- Recommendation for Indigenous data sovereignty in federal grant programs

---

## 7. Budget (CAD)

| Item | Amount | Justification |
|------|--------|---------------|
| **Personnel** | | |
| Principal Investigator (20% FTE, 18 mo) | $42,000 | Maksym Stepanenko — full-stack development, AI pipeline, Web3 integration |
| Indigenous Advisor (contract, 12 mo) | $18,000 | Community liaison, cultural review, governance design |
| Computational Linguist (contract, 6 mo) | $15,000 | Whisper fine-tuning, TTS optimization, accuracy evaluation |
| **Community Co-Design** | | |
| Travel + workshops (2 communities × 3 visits) | $8,000 | Participatory design sessions, elder consultations |
| Honoraria for community participants | $4,000 | Elders, youth, council members |
| **Technical Infrastructure** | | |
| Cloud compute (GPU for Whisper/TTS training) | $6,000 | Google Cloud / Lambda Labs GPU instances |
| Storage + bandwidth | $3,000 | MinIO + CDN for audio distribution |
| Blockchain gas + node hosting | $1,000 | Polygon mainnet deployment + monitoring |
| **Evaluation + Dissemination** | | |
| Legal review (provenance admissibility) | $3,000 | Indigenous law faculty consultation |
| Open-source documentation + video | $2,000 | Technical docs, demo video for grant reporting |
| Conference travel | $3,000 | ACL or NAISA presentation |
| **Administrative** | | |
| Institutional overhead (10%) | $10,500 | |
| **TOTAL** | **$115,500** | |

---

## 8. Timeline

| Phase | Months | Milestone |
|-------|--------|-----------|
| Foundation | 1–2 | Advisory board, community outreach, data agreements |
| Co-Design | 2–4 | Workshops, requirements, governance design |
| AI Pipeline | 3–8 | Whisper fine-tuning, TTS, Gemini translation, accuracy benchmarks |
| Web3 + Storage | 6–10 | Smart contract deploy, IPFS/Filecoin integration, local node option |
| Pilot Launch | 8–12 | Platform v1.0 in 2 communities, 50+ hours recorded |
| Evaluation | 10–18 | Trust surveys, usage metrics, legal review, paper writing |
| Open Source | 14–18 | Public release, documentation, conference presentation |

---

## 9. Team

| Role | Name | Background | Responsibility |
|------|------|-----------|---------------|
| **PI / Technologist** | Maksym Stepanenko | Full-stack engineer, AI/ML, Web3. Built 30+ production apps. | Architecture, AI pipeline, Web3 integration, grant management |
| **Indigenous Advisor** | TBD (recruiting) | Community organizer, tech-savvy, from target community | Cultural review, governance co-design, community trust-building |
| **Computational Linguist** | TBD (recruiting) | PhD/MA in endangered languages, Python/ML | ASR/TTS fine-tuning, accuracy evaluation, linguistic consultation |
| **Legal Consultant** | TBD | Indigenous law faculty | Provenance NFT admissibility, data sovereignty legal framework |

**Partnership targets:**
- First Nations Tech Council (BC)
- University of Victoria — Indigenous Studies + Linguistics
- UBC — First Nations House of Learning
- Te Taura Whiri i te Reo Māori (NZ bridge partner)

---

## 10. Why SSHRC

This project sits at the intersection of:
- **Digital Humanities** (language preservation, oral history digitization)
- **Computer Science** (low-resource NLP, speech technology)
- **Indigenous Studies** (data sovereignty, decolonization, OCAP)
- **Law** (cultural intellectual property, provenance evidence)

SSHRC Insight Development Grants explicitly support "novel or promising research" that bridges disciplines. The Indigenous language revitalization angle aligns with SSHRC's priority on research that addresses "major societal challenges" and the Truth and Reconciliation Commission's Calls to Action (#13–17 on language).

---

## 11. Risk Mitigation

| Risk | Mitigation |
|------|-----------|
| Community distrust | Indigenous advisor from Day 1; OCAP-first design; no data leaves without explicit consent |
| Low-resource AI failure | Fallback to human transcription pipeline; incremental improvement; partner with linguistics dept |
| Community dropout | Co-design ensures ownership; train local admins; platform remains open-source regardless |
| Blockchain skepticism | "Provenance" not "crypto"; no financial tokens; eco-friendly chain (Polygon PoS); optional feature |
| Grant dependency | Dual-track: grants + institutional SaaS contracts; low burn rate; open-source sustainability |

---

## 12. Letters of Support Needed

- [ ] First Nations Tech Council (advisory partnership)
- [ ] University of Victoria Indigenous Studies (academic affiliation)
- [ ] Target First Nation community council (pilot participation)
- [ ] HuggingFace (model hosting partnership)
- [ ] Filecoin Foundation (decentralized storage grant bridge)

---

## 13. Appendices

### A. OCAP Technical Implementation Matrix
| Principle | Technical Mechanism |
|-----------|---------------------|
| Ownership | Community holds encryption keys; platform cannot decrypt sacred content |
| Control | Smart contract multi-sig for policy changes; council voting via Snapshot |
| Access | Role-based API: viewer/recorder/reviewer/elder/admin; audit log immutable |
| Possession | Monthly auto-export to community S3; optional air-gapped local node |

### B. Pilot Community Profiles
1. **Cree First Nation (Ontario/Manitoba)** — 100K+ speakers but declining; strong institutional support; existing language programs
2. **Haida Nation (BC)** — Critically endangered (<10 fluent speakers); high symbolic value; active revitalization movement

### C. AI Performance Targets
| Metric | Target | Notes |
|--------|--------|-------|
| ASR WER (Cree) | <30% | With <10h training data |
| TTS MOS | >3.5/5 | Mean Opinion Score for naturalness |
| Translation BLEU | >25 | EN/FR from Cree with cultural context |
| Inference speed | <30s/min | CPU-only, no GPU required at edge |

### D. GitHub Repository
https://github.com/ctmakc/firstvoice

---

*Prepared: 2026-06-05*
*Version: 1.0*
*Status: Ready for submission with advisory board confirmation*
