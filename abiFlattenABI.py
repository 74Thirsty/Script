import json
import sys
import os

def flatten_abi(input_path, output_path):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, 'r') as f:
        artifact = json.load(f)

    if not isinstance(artifact, dict) or 'abi' not in artifact:
        raise ValueError("Input must be a Hardhat-style artifact with an 'abi' field")

    abi = artifact['abi']
    if not isinstance(abi, list):
        raise TypeError("'abi' must be a list")

    flattened = json.dumps(abi, separators=(',', ':'))

    with open(output_path, 'w') as out:
        out.write(flattened)

    print(f"✅ Flattened ABI written to: {output_path}")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python flatten_abi.py <input_artifact.json> <output_abi.json>")
        sys.exit(1)

    flatten_abi(sys.argv[1], sys.argv[2])
