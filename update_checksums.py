import json
import hashlib
import os

# List of your seed files
seed_files = [
    "seeds/strategist.seed.json",
    "seeds/scribe.seed.json",
    "seeds/steward.seed.json"
]

def compute_checksum(content: str) -> str:
    """Compute SHA256 checksum of a string."""
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def update_checksum(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Temporarily remove old checksum before computing new one
    if "checksum" in data.get("metadata", {}):
        data["metadata"]["checksum"] = ""

    # Re-dump JSON (sorted keys for consistency)
    content_str = json.dumps(data, sort_keys=True, separators=(",", ":"))
    checksum = compute_checksum(content_str)

    # Update JSON with new checksum
    data["metadata"]["checksum"] = checksum

    # Save back to file (pretty printed for readability)
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Updated {file_path} with checksum {checksum}")

def main():
    for seed in seed_files:
        if os.path.exists(seed):
            update_checksum(seed)
        else:
            print(f"⚠️ File not found: {seed}")

if __name__ == "__main__":
    main()
