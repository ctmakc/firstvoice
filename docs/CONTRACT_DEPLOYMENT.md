# FirstVoice Soulbound Provenance — Deployment Guide

## Overview

The `SoulboundProvenance` contract is an ERC-721 Soulbound (non-transferable) NFT that stores:
- `contentHash` (SHA-256 of the recording)
- `community` (name)
- `language` (ISO 639-3 code)
- `recordedAt` (timestamp)
- `aiTrainingAllowed` (bool)

**Network:** Polygon Amoy Testnet (for MVP) → Polygon Mainnet (for production)

---

## Prerequisites

1. Node.js 18+ and npm
2. A wallet with MATIC on Polygon Amoy testnet
3. Amoy RPC endpoint

---

## 1. Generate a Deployer Wallet

```bash
cd apps/api/contracts
npm install

# Generate a new wallet (save the output securely)
npx hardhat run -e "console.log(require('hardhat').ethers.Wallet.createRandom())"
```

Or use any existing wallet. **Never use a mainnet/production wallet for testnet.**

---

## 2. Get Amoy Testnet MATIC

Request faucet funds:

**Option A — Polygon Faucet (official):**
Visit https://faucet.polygon.technology/ and paste your wallet address.

**Option B — Alchemy Faucet:**
https://www.alchemy.com/faucets/polygon-amoy

**Option C — QuickNode Faucet:**
https://faucet.quicknode.com/polygon/amoy

Need: ~2 MATIC for deployment + testing.

---

## 3. Configure Environment

```bash
cd apps/api/contracts
cp .env.example .env
```

Edit `.env`:
```
POLYGON_RPC=https://rpc-amoy.polygon.technology
PRIVATE_KEY=0xYOUR_PRIVATE_KEY_HERE
RELAYER_ADDRESS=0xYOUR_WALLET_ADDRESS
```

The `RELAYER_ADDRESS` is the only address that can mint tokens. Use the deployer address for simplicity.

---

## 4. Compile the Contract

```bash
npx hardhat compile
```

You should see:
```
Compiled 1 Solidity file successfully
```

---

## 5. Deploy

```bash
npx hardhat run scripts/deploy.js --network amoy
```

Expected output:
```
Deploying with account: 0x...
Relayer address: 0x...
SoulboundProvenance deployed to: 0xCONTRACT_ADDRESS
Run the following to save the address:
export PROVENANCE_CONTRACT_ADDRESS=0xCONTRACT_ADDRESS
```

**Save the contract address.** This is needed for the backend `.env`.

---

## 6. Verify the Deployment

### Check on Amoy Explorer
Visit: `https://www.oklink.com/amoy/address/0xCONTRACT_ADDRESS`

Or: `https://amoy.polygonscan.com/address/0xCONTRACT_ADDRESS`

### Test Mint (optional)

```bash
npx hardhat console --network amoy
```

```javascript
const contract = await ethers.getContractAt("SoulboundProvenance", "0xCONTRACT_ADDRESS");
await contract.mint(
  "0xYOUR_ADDRESS",
  "0x1234567890abcdef...",
  "Cree First Nation",
  "cre",
  0,
  false
);
```

---

## 7. Update Backend Configuration

In `/data/projects/firstvoice/.env` (or `.env.local`):

```env
POLYGON_RPC=https://rpc-amoy.polygon.technology
PROVENANCE_CONTRACT_ADDRESS=0xYOUR_DEPLOYED_ADDRESS
RELAYER_PRIVATE_KEY=0xYOUR_PRIVATE_KEY
```

Restart the API worker:
```bash
cd /data/projects/firstvoice/infra
docker compose restart api worker
```

---

## 8. Production (Polygon Mainnet)

When ready for production:

1. **Get mainnet MATIC** via exchange or bridge
2. **Update hardhat.config.js:**
```javascript
networks: {
  polygon: {
    url: process.env.POLYGON_RPC || "https://polygon-rpc.com",
    accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
  },
}
```
3. **Deploy:**
```bash
npx hardhat run scripts/deploy.js --network polygon
```
4. **Verify on Polygonscan:**
```bash
npx hardhat verify --network polygon 0xCONTRACT_ADDRESS 0xRELAYER_ADDRESS
```

---

## Contract Addresses

| Network | Address | Tx Hash | Date |
|---------|---------|---------|------|
| Amoy Testnet | TBD | TBD | TBD |
| Polygon Mainnet | TBD | TBD | TBD |

---

## Security Notes

- The relayer private key is the only key that can mint. Store it securely (environment variable, never in code).
- Soulbound enforcement: `_beforeTokenTransfer` blocks all transfers. Only minting is allowed.
- No burn function: tokens are permanent, matching the "provenance" use case.
- Upgrade path: deploy new contract + migration script if metadata schema changes.

---

## Gas Costs (Amoy Testnet)

| Operation | Gas Used | Approx. Cost (MATIC) |
|-----------|----------|---------------------|
| Deploy | ~2,500,000 | ~0.0025 |
| Mint | ~150,000 | ~0.00015 |

---

*Last updated: 2026-06-05*
