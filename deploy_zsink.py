"""Deploy ExecutionLayer contract to zkSync using standardized secret loading."""

import json
import logging

from web3 import Web3

from utils.env_validator import _get_decimal_secret, _load_secret

logger = logging.getLogger(__name__)


RPC_URL = _load_secret("ZKSYNC_RPCURL") or _load_secret("ZKSYNC_RPC_URL")
PRIVATE_KEY = _load_secret("ZKSYNC_PRIVATE_KEY")
WALLET = _load_secret("ZKSYNC_WALLET")

MAX_FEE_GWEI = _get_decimal_secret("ZKSYNC_MAX_FEE_GWEI", "0.25")
PRIORITY_FEE_GWEI = _get_decimal_secret("ZKSYNC_PRIORITY_FEE_GWEI", "0.1")

if not RPC_URL:
    raise RuntimeError("ZKSYNC_RPCURL is required for deployment")
if not PRIVATE_KEY:
    raise RuntimeError("ZKSYNC_PRIVATE_KEY is required for deployment")
if not WALLET:
    raise ValueError("ZKSYNC_WALLET configuration is not set")

WALLET_ADDRESS = Web3.to_checksum_address(WALLET)

# === Load compiled contract ===
with open("ExecutionLayer_compData.json", "r") as f:
    compiled = json.load(f)

abi = compiled["abi"]
bytecode = "0x" + compiled["bytecode"]["object"]  # Ensure it starts with 0x

# === Connect to zkSync Era ===
w3 = Web3(Web3.HTTPProvider(RPC_URL))
assert w3.is_connected(), "❌ Could not connect to zkSync RPC"

# === Prepare contract instance ===
contract = w3.eth.contract(abi=abi, bytecode=bytecode)

# === Build transaction ===
nonce = w3.eth.get_transaction_count(WALLET_ADDRESS)

transaction = contract.constructor().build_transaction({
    "from": WALLET_ADDRESS,
    "nonce": nonce,
    "gas": 3_000_000,
    "maxFeePerGas": w3.to_wei(MAX_FEE_GWEI, "gwei"),
    "maxPriorityFeePerGas": w3.to_wei(PRIORITY_FEE_GWEI, "gwei"),
    "chainId": 324,  # zkSync mainnet
})

# === Sign and send transaction ===
signed_tx = w3.eth.account.sign_transaction(transaction, PRIVATE_KEY)
tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
receipt = w3.eth.wait_for_transaction_receipt(tx_hash)

print(f"✅ Contract deployed to: {receipt['contractAddress']}")
