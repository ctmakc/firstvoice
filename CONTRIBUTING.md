# Contributing to FirstVoice

Thank you for your interest in FirstVoice. We welcome contributors from all backgrounds, especially Indigenous community members, linguists, and engineers passionate about language revitalization.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/firstvoice.git`
3. Copy `.env.example` to `.env` and configure
4. Start the stack: `cd infra && docker compose up -d --build`
5. Run migrations: `cd apps/api && alembic upgrade head`
6. Seed data: `python apps/api/scripts/seed.py`

## Code Guidelines

### Backend (Python)
- Follow PEP 8
- Use type hints
- Add docstrings for public functions
- Run `ruff check .` before committing
- Run `pytest` to ensure tests pass

### Frontend (TypeScript / Next.js)
- Mobile-first design (375px base)
- Plain CSS / CSS Modules — **no Tailwind**
- Accessibility: keyboard nav, ARIA labels, focus-visible
- Match existing dark theme tokens
- Run `npm run lint && npm run typecheck` before committing

### Commit Messages
Use conventional commits:
- `feat(api): add transcription pipeline`
- `fix(web): offline sync bug`
- `docs: update grant strategy`

## Areas of Contribution

### 🎙️ Language & Culture
- Help curate language datasets
- Review translations for cultural accuracy
- Test with community members
- Provide feedback on sacred/public classification UX

### 🤖 AI / ML
- Fine-tune Whisper for specific languages
- Improve TTS voice quality
- Reduce model size for edge deployment
- Add speaker diarization

### ⛓️ Web3
- Optimize gas costs for provenance minting
- Add Layer 2 support (e.g., zkSync, Scroll)
- Build DAO governance frontend
- Integrate decentralized storage (IPFS + Filecoin)

### 🛠️ Infrastructure
- Improve Docker Compose setup
- Add Kubernetes manifests
- Optimize CI/CD pipelines
- Security audits

## Reporting Issues

When reporting bugs, please include:
- Steps to reproduce
- Expected vs. actual behavior
- Environment (OS, browser, Docker version)
- Screenshots if applicable

For **security issues**, email `security@firstvoice.dev` instead of opening a public issue.

## Community

- Discussions: GitHub Discussions
- Indigenous advisors: Contact via email
- Grants & partnerships: See [docs/GRANTS.md](docs/GRANTS.md)

## Code of Conduct

This project follows the [Contributor Covenant Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/).

**Key principle:** FirstVoice exists to serve communities. All contributions must respect Indigenous data sovereignty and OCAP principles.
