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

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "metadata-schema.yaml"
PERSONAS = ROOT / "personas"
SEEDS = ROOT / "seeds"

def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def estimate_size_bytes(text: str) -> int:
    return len(text.encode("utf-8"))

def to_iso_str(v):
    # Coerce datetime/date or other non-str into ISO string
    if isinstance(v, (datetime.date, datetime.datetime)):
        return v.date().isoformat() if isinstance(v, datetime.datetime) else v.isoformat()
    return str(v) if v is not None and not isinstance(v, str) else v

def load_yaml(p: Path) -> dict:
    with p.open("r", encoding="utf-8") as fh:
        doc = yaml.safe_load(fh)
    # Normalize created/updated if YAML parsed them as date objects
    for k in ("created", "updated"):
        if k in doc:
            doc[k] = to_iso_str(doc[k])
    return doc

def validate(doc: dict):
    with open(SCHEMA, "r", encoding="utf-8") as fh:
        schema = yaml.safe_load(fh)
    jsonschema.validate(instance=doc, schema=schema)

def normalize(doc: dict) -> dict:
    # Ensure minimal fields + checksum + sizes
    core_prompt = doc.get("core_prompt", "") or ""
    # default created/updated if missing
    if not doc.get("created"):
        doc["created"] = datetime.date.today().isoformat()
    doc["updated"] = datetime.date.today().isoformat()

    # coerce resource fields into schema-friendly forms
    doc["created"] = to_iso_str(doc["created"])
    doc["updated"] = to_iso_str(doc["updated"])

    if "size_bytes" not in doc or not doc["size_bytes"]:
        doc["size_bytes"] = estimate_size_bytes(core_prompt)
    doc["checksum"] = sha256_bytes(core_prompt.encode("utf-8")) if core_prompt else ""

    # sensible defaults for refresh/cache
    doc.setdefault("preferred_refresh", {"action": "ChatGPT", "interval": "on-demand"})
    doc.setdefault("cache_strategy", "local")
    doc.setdefault("chunk_size", 1024)
    doc.setdefault("tags", [])
    doc.setdefault("links", [])
    return doc

def main():
    ap = argparse.ArgumentParser(description="Package persona YAML into flat seed JSON.")
    ap.add_argument("--in", dest="inp", help="Path to persona YAML (default: all in personas/).")
    ap.add_argument("--outdir", dest="outdir", default=str(SEEDS), help="Output folder (default: seeds/).")
    args = ap.parse_args()

    outdir = Path(args.outdir); outdir.mkdir(parents=True, exist_ok=True)
    targets = [Path(args.inp)] if args.inp else list(PERSONAS.glob("*.yaml"))
    if not targets:
        print("No persona YAML files found.", file=sys.stderr); sys.exit(1)

    # load schema once
    with open(SCHEMA, "r", encoding="utf-8") as fh:
        schema = yaml.safe_load(fh)

    for yml in targets:
        doc = load_yaml(yml)
        doc = normalize(doc)
        try:
            jsonschema.validate(instance=doc, schema=schema)
        except Exception as e:
            print(f"Schema validation failed for {yml.name}: {e}", file=sys.stderr)
            sys.exit(1)

        seed_name = f"{doc.get('persona_role','none')}.seed.json"
        seed_path = Path(args.outdir) / seed_name

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
                "preferred_refresh": doc.get("preferred_refresh"),
                "cache_strategy": doc.get("cache_strategy"),
                "tags": doc.get("tags", []),
                "category": doc.get("category", ""),
                "updated": doc.get("updated",""),
                "checksum": doc.get("checksum","")
            }
        }

        seed_path.write_text(json.dumps(seed, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote {seed_path}")

if __name__ == "__main__":
    main()
