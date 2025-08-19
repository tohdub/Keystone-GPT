import argparse, json, hashlib, os, sys, datetime
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Missing dependency: pyyaml. Install with: pip install pyyaml", file=sys.stderr)
    sys.exit(1)

try:
    import jsonschema
except ImportError:
    print("Missing dependency: jsonschema. Install with: pip install jsonschema", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parent.parent if (Path(__file__).name == "seed_packager.py") else Path.cwd()
SCHEMA = ROOT / "schema" / "metadata-schema.yaml"
PERSONAS = ROOT / "personas"
SEEDS = ROOT / "seeds"

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def estimate_size_bytes(text: str) -> int:
    return len(text.encode("utf-8"))

def load_yaml(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)

def validate(doc: dict):
    with open(SCHEMA, "r", encoding="utf-8") as fh:
        schema = yaml.safe_load(fh)
    jsonschema.validate(instance=doc, schema=schema)

def normalize(doc: dict) -> dict:
    # Ensure minimal fields + checksum + sizes
    core_prompt = doc.get("core_prompt", "")
    if "size_bytes" not in doc or not doc["size_bytes"]:
        doc["size_bytes"] = estimate_size_bytes(core_prompt)
    # stamp updated
    doc["updated"] = datetime.date.today().isoformat()
    # derive checksum from core_prompt
    doc["checksum"] = sha256_bytes(core_prompt.encode("utf-8")) if core_prompt else ""
    return doc

def main():
    ap = argparse.ArgumentParser(description="Package persona YAML into flat seed JSON.")
    ap.add_argument("--in", dest="inp", required=False, help="Path to persona YAML (default: all in personas/).")
    ap.add_argument("--outdir", dest="outdir", default=str(SEEDS), help="Output folder (default: seeds/).")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    targets = []
    if args.inp:
        targets = [Path(args.inp)]
    else:
        targets = list(PERSONAS.glob("*.yaml"))

    if not targets:
        print("No persona YAML files found.", file=sys.stderr)
        sys.exit(1)

    for yml in targets:
        doc = load_yaml(yml)
        doc = normalize(doc)
        try:
            validate(doc)
        except Exception as e:
            print(f"Schema validation failed for {yml.name}: {e}", file=sys.stderr)
            sys.exit(1)

        seed_name = f"{doc['persona_role']}.seed.json" if doc.get("persona_role") else (yml.stem + ".seed.json")
        seed_path = outdir / seed_name

        # Build a minimal flat seed for embedding
        seed = {
            "id": doc["id"],
            "title": doc["title"],
            "type": doc["type"],
            "version": doc["version"],
            "persona_role": doc.get("persona_role","none"),
            "function": doc.get("function",""),
            "priority": doc.get("priority","medium"),
            "alignment": doc.get("alignment","neutral"),
            "core_prompt": doc.get("core_prompt",""),
            "metadata": {
                "chunk_size": doc.get("chunk_size", 1024),
                "size_bytes": doc.get("size_bytes", 0),
                "preferred_refresh": doc.get("preferred_refresh", {"action":"ChatGPT","interval":"on-demand"}),
                "cache_strategy": doc.get("cache_strategy", "local"),
                "tags": doc.get("tags", []),
                "category": doc.get("category", ""),
                "updated": doc.get("updated",""),
                "checksum": doc.get("checksum","")
            }
        }

        with seed_path.open("w", encoding="utf-8") as fh:
            json.dump(seed, fh, ensure_ascii=False, indent=2)

        print(f"Wrote {seed_path}")

if __name__ == "__main__":
    main()
