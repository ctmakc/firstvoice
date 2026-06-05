#!/usr/bin/env bash
set -euo pipefail

# FirstVoice — Production Deploy Script
# Usage: ./scripts/deploy.sh [host] [domain]
# Example: ./scripts/deploy.sh root@31.42.188.28 firstvoice.dev

HOST=${1:-}
DOMAIN=${2:-firstvoice.dev}
REPO_DIR="/opt/firstvoice"

echo "🚀 FirstVoice Production Deploy"
echo "   Host: ${HOST}"
echo "   Domain: ${DOMAIN}"
echo ""

if [[ -z "$HOST" ]]; then
    echo "❌ Usage: $0 <user@host> <domain>"
    echo "   Example: $0 root@31.42.188.28 firstvoice.dev"
    exit 1
fi

# Generate .env.prod
cat > .env.prod <<EOF
# FirstVoice Production Environment
# Generated on $(date -u +%Y-%m-%dT%H:%M:%SZ)

DOMAIN=${DOMAIN}
POSTGRES_PASSWORD=$(openssl rand -hex 32)
MINIO_ROOT_USER=firstvoice
MINIO_ROOT_PASSWORD=$(openssl rand -hex 32)
NEXTAUTH_SECRET=$(openssl rand -hex 32)
APP_SECRET=$(openssl rand -hex 32)

# AI Services (fill in after deploy)
GEMINI_API_KEY=

# Blockchain (fill in after contract deploy)
PROVENANCE_CONTRACT_ADDRESS=
POLYGON_RPC=https://rpc-amoy.polygon.technology
RELAYER_PRIVATE_KEY=
EOF

echo "📦 1. Syncing code to ${HOST}..."
rsync -avz \
    --exclude='.git' \
    --exclude='node_modules' \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='.next' \
    --exclude='*.pyc' \
    --exclude='screenshots/' \
    --exclude='docs/*.md' \
    -e ssh . "${HOST}:${REPO_DIR}/"

echo "📦 2. Copying production env..."
scp .env.prod "${HOST}:${REPO_DIR}/infra/.env"

echo "🐳 3. Building and starting services..."
ssh "${HOST}" "cd ${REPO_DIR}/infra && \
    docker compose -f docker-compose.prod.yml down 2>/dev/null || true && \
    docker compose -f docker-compose.prod.yml up -d --build && \
    sleep 10 && \
    docker compose -f docker-compose.prod.yml ps"

echo ""
echo "✅ Deploy complete!"
echo ""
echo "   🌐 Web: https://${DOMAIN}"
echo "   📚 API Docs: https://${DOMAIN}/docs"
echo "   💊 MinIO Console: https://${DOMAIN}/minio/"
echo ""
echo "📋 Next steps:"
echo "   1. Run migrations: ssh ${HOST} 'cd ${REPO_DIR}/apps/api && docker compose -f ../../infra/docker-compose.prod.yml exec api alembic upgrade head'"
echo "   2. Seed data: ssh ${HOST} 'cd ${REPO_DIR}/apps/api && docker compose -f ../../infra/docker-compose.prod.yml exec api python scripts/seed.py'"
echo "   3. Add GEMINI_API_KEY to ${REPO_DIR}/infra/.env"
echo "   4. Deploy contract + add PROVENANCE_CONTRACT_ADDRESS to .env"
echo ""
echo "🔐 Secrets saved to: .env.prod (DO NOT COMMIT)"
