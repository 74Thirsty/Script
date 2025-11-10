import { ethers } from "ethers";

// Hardcoded RPC URL and Safe Address
const RPC_URL = "https://eth-mainnet.g.alchemy.com/v2/RBCHdCUROomscVSMZQeNX9H2MXBknXkQ";
const safeAddress = "0xC6139506fa54c450948D9D2d8cCf269453A54f17";

// ABI to get the threshold
const abi = [
  "function getThreshold() view returns (uint256)"
];

// Set up the provider
const provider = new ethers.JsonRpcProvider(RPC_URL);

// Create the contract instance
const safeContract = new ethers.Contract(safeAddress, abi, provider);

// Get threshold
async function getThreshold() {
  try {
    const threshold = await safeContract.getThreshold();
    console.log("Safe Threshold:", threshold);
  } catch (error) {
    console.error("Error:", error);
  }
}

getThreshold();
