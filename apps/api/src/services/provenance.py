from typing import Any, Dict, Optional, Tuple

from web3 import Web3
from eth_account import Account
from eth_utils import keccak

from src.config import get_settings

settings = get_settings()

# Minimal ABI for SoulboundProvenance (self-contained)
_SOULBOUND_PROVENANCE_ABI = [
    {
        "inputs": [{"internalType": "address", "name": "_relayer", "type": "address"}],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "tokenId", "type": "uint256"},
            {"indexed": False, "internalType": "bytes32", "name": "contentHash", "type": "bytes32"},
            {"indexed": False, "internalType": "string", "name": "community", "type": "string"},
            {"indexed": False, "internalType": "string", "name": "language", "type": "string"},
            {"indexed": False, "internalType": "uint256", "name": "recordedAt", "type": "uint256"},
            {"indexed": False, "internalType": "bool", "name": "aiTrainingAllowed", "type": "bool"},
        ],
        "name": "ProvenanceMinted",
        "type": "event",
    },
    {
        "inputs": [
            {"internalType": "address", "name": "to", "type": "address"},
            {"internalType": "bytes32", "name": "contentHash", "type": "bytes32"},
            {"internalType": "string", "name": "community", "type": "string"},
            {"internalType": "string", "name": "language", "type": "string"},
            {"internalType": "uint256", "name": "recordedAt", "type": "uint256"},
            {"internalType": "bool", "name": "aiTrainingAllowed", "type": "bool"},
        ],
        "name": "mint",
        "outputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "provenance",
        "outputs": [
            {"internalType": "bytes32", "name": "contentHash", "type": "bytes32"},
            {"internalType": "string", "name": "community", "type": "string"},
            {"internalType": "string", "name": "language", "type": "string"},
            {"internalType": "uint256", "name": "recordedAt", "type": "uint256"},
            {"internalType": "bool", "name": "aiTrainingAllowed", "type": "bool"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "tokenId", "type": "uint256"}],
        "name": "ownerOf",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
]

_w3: Optional[Web3] = None
_contract: Optional[Any] = None


def _get_web3() -> Web3:
    """Lazy-initialize Web3 connection to Polygon Amoy."""
    global _w3
    if _w3 is None:
        _w3 = Web3(Web3.HTTPProvider(settings.polygon_rpc))
        if not _w3.is_connected():
            raise ConnectionError(f"Cannot connect to Polygon RPC: {settings.polygon_rpc}")
    return _w3


def _get_contract() -> Any:
    """Lazy-load contract instance."""
    global _contract
    if _contract is None:
        if not settings.provenance_contract_address:
            raise ValueError("PROVENANCE_CONTRACT_ADDRESS not configured")
        w3 = _get_web3()
        _contract = w3.eth.contract(
            address=Web3.to_checksum_address(settings.provenance_contract_address),
            abi=_SOULBOUND_PROVENANCE_ABI,
        )
    return _contract


def _get_relayer_account() -> Account:
    if not settings.relayer_private_key:
        raise ValueError("RELAYER_PRIVATE_KEY not configured")
    return Account.from_key(settings.relayer_private_key)


def mint_provenance(
    recording_id: str,
    content_hash: str,
    community: str,
    language: str,
    ai_allowed: bool,
) -> Tuple[str, Optional[int]]:
    """Mint a Soulbound Provenance NFT. Returns (tx_hash, token_id)."""
    w3 = _get_web3()
    contract = _get_contract()
    account = _get_relayer_account()

    content_hash_bytes = bytes.fromhex(content_hash.replace("0x", ""))

    tx = contract.functions.mint(
        account.address,
        content_hash_bytes,
        community,
        language,
        0,
        ai_allowed,
    ).build_transaction({
        "from": account.address,
        "nonce": w3.eth.get_transaction_count(account.address),
        "gas": 300000,
        "maxFeePerGas": w3.to_wei("30", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("2", "gwei"),
        "chainId": w3.eth.chain_id,
    })

    signed_tx = account.sign_transaction(tx)
    raw_tx = getattr(signed_tx, "raw_transaction", getattr(signed_tx, "rawTransaction", None))
    tx_hash = w3.eth.send_raw_transaction(raw_tx)
    tx_hash_hex = w3.to_hex(tx_hash)

    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
    if receipt.status != 1:
        raise RuntimeError(f"Transaction failed on-chain: {tx_hash_hex}")

    # Parse ProvenanceMinted event for token ID; fallback to standard Transfer
    event_sig_hash = "0x" + keccak(text="ProvenanceMinted(uint256,bytes32,string,string,uint256,bool)").hex()
    transfer_event_sig = "0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef"

    token_id: Optional[int] = None
    for log in receipt.logs:
        if len(log.topics) == 0:
            continue
        topic0 = log.topics[0].hex()
        if topic0 == event_sig_hash and len(log.topics) > 1:
            token_id = int(log.topics[1].hex(), 16)
            break
        elif topic0 == transfer_event_sig and len(log.topics) > 3:
            token_id = int(log.topics[3].hex(), 16)

    return tx_hash_hex, token_id


def get_provenance(token_id: int) -> Dict[str, Any]:
    """Fetch on-chain provenance metadata for a token."""
    w3 = _get_web3()
    contract = _get_contract()
    data = contract.functions.provenance(token_id).call()
    owner = contract.functions.ownerOf(token_id).call()
    return {
        "token_id": token_id,
        "owner": owner,
        "content_hash": w3.to_hex(data[0]),
        "community": data[1],
        "language": data[2],
        "recorded_at": data[3],
        "ai_training_allowed": data[4],
    }
