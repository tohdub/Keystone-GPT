import json
import hashlib
import os

seed_folder = "seeds"
seed_files = [
    os.path.join(seed_folder, f)
    for f in os.listdir(seed_folder)
    if f.endswith(".seed.json")
]

def compute_checksum(content: str) -> str:
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def update_checksum(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if "checksum" in data.get("metadata", {}):
        data["metadata"]["checksum"] = ""

    content_str = json.dumps(data, sort_keys=True, separators=(",", ":"))
    checksum = compute_checksum(content_str)
    data["metadata"]["checksum"] = checksum

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"✅ Updated {file_path} with checksum {checksum}")

def main():
    if not seed_files:
        print("⚠️ No .seed.json files found in seeds/")
    for seed in seed_files:
        update_checksum(seed)

if __name__ == "__main__":
    main()
