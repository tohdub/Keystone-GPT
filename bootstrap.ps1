# bootstrap.ps1 — creates scaffold, starter files, and a venv
$ErrorActionPreference = "Stop"

# 1. Create folders
$dirs = @(
  "personas","manuals","resources","inputs","code",
  "seeds","logs","schema",".venv"
)
$dirs | ForEach-Object { if (-not (Test-Path $_)) { New-Item -Type Directory $_ | Out-Null } }

# 2. .gitignore
@"
# Python
.venv/
__pycache__/
*.pyc
*.pyo
*.pyd
.env
.env.*
# Logs/Seeds
logs/*
!logs/.keep
seeds/*.json
# OS
.DS_Store
Thumbs.db
"@ | Set-Content .gitignore -Encoding UTF8

# 3. README (Charter)
@"
# Keystone GPT

**Single source of truth** for modular GPT assets. Triad of stewardship:

- **The Steward** — coherence & alignment
- **The Scribe** — indexing & metadata
- **The Strategist** — toolstack & optimization

See \`schema/metadata-schema.yaml\` for frontmatter rules.
"@ | Set-Content README.md -Encoding UTF8

# 4. Schema: metadata-schema.yaml
@"
# schema/metadata-schema.yaml
type: object
required: [id, title, type, version, created, updated]
properties:
  id: {type: string}
  title: {type: string}
  type: {enum: [persona, manual, reference, input, resource, code, log]}
  author: {type: string}
  version: {type: string}
  created: {type: string}
  updated: {type: string}
  tags: {type: array, items: {type: string}}
  links: {type: array, items: {type: string}}
  category: {type: string}
  visibility: {enum: [public, internal, restricted]}
  size_bytes: {type: number}
  chunk_size: {type: number}
  preferred_refresh:
    type: object
    properties:
      action: {enum: [ChatGPT, GitHubApp]}
      interval: {enum: [on-demand, scheduled, none]}
  cache_strategy: {enum: [local, remote, hybrid]}
  source: {type: string}
  checksum: {type: string}
  license: {type: string}
  persona_role: {enum: [steward, scribe, strategist, none]}
  function: {type: string}
  priority: {enum: [low, medium, high]}
  alignment: {enum: [mission, neutral, deprecated]}
  notes: {type: string}
"@ | Set-Content schema/metadata-schema.yaml -Encoding UTF8

# 5. Starter persona cards (YAML)
@"
id: steward-seed-v1
title: Steward Seed
type: persona
author: user
version: v1.0.0
created: 2025-08-19
updated: 2025-08-19
tags: [coherence, alignment, reflection]
links: []
category: governance
visibility: internal
size_bytes: 0
chunk_size: 1024
preferred_refresh:
  action: ChatGPT
  interval: on-demand
cache_strategy: local
source: "repo://personas/steward.yaml"
checksum: ""
license: proprietary
persona_role: steward
function: alignment
priority: high
alignment: mission
notes: >
  The Steward ensures conceptual coherence and mission alignment.
core_prompt: |
  You are the Steward. Ensure coherence, reflect goals back to the user,
  and keep assets aligned with mission and success criteria.
"@ | Set-Content personas/steward.yaml -Encoding UTF8

@"
id: scribe-seed-v1
title: Scribe Seed
type: persona
author: user
version: v1.0.0
created: 2025-08-19
updated: 2025-08-19
tags: [indexing, metadata, retrieval]
links: []
category: catalog
visibility: internal
size_bytes: 0
chunk_size: 2048
preferred_refresh:
  action: GitHubApp
  interval: scheduled
cache_strategy: hybrid
source: "repo://personas/scribe.yaml"
checksum: ""
license: proprietary
persona_role: scribe
function: indexing
priority: high
alignment: neutral
notes: >
  The Scribe enforces schema discipline and prevents index drift.
core_prompt: |
  You are the Scribe. Maintain metadata, tagging, and retrieval integrity.
  Validate frontmatter and fix inconsistencies proactively.
"@ | Set-Content personas/scribe.yaml -Encoding UTF8

@"
id: strategist-seed-v1
title: Strategist Seed
type: persona
author: user
version: v1.0.0
created: 2025-08-19
updated: 2025-08-19
tags: [optimization, costs, performance]
links: []
category: systems
visibility: internal
size_bytes: 0
chunk_size: 2048
preferred_refresh:
  action: GitHubApp
  interval: on-demand
cache_strategy: hybrid
source: "repo://personas/strategist.yaml"
checksum: ""
license: proprietary
persona_role: strategist
function: optimization
priority: high
alignment: mission
notes: >
  The Strategist balances performance, cost, and maintainability.
core_prompt: |
  You are the Strategist. Design and optimize toolchains, schemas,
  and API integrations with explicit cost/performance tradeoffs.
"@ | Set-Content personas/strategist.yaml -Encoding UTF8

# 6. Python utility: seed_packager.py
@"
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
"@ | Set-Content code/seed_packager.py -Encoding UTF8

# 7. requirements.txt (for the packager)
@"
pyyaml==6.0.2
jsonschema==4.23.0
"@ | Set-Content requirements.txt -Encoding UTF8

# 8. Keep placeholder for logs
"placeholder" | Set-Content logs/.keep -Encoding UTF8

Write-Host "`nScaffold created. Next steps:"
Write-Host "  python -m venv .venv"
Write-Host "  .\.venv\Scripts\Activate.ps1"
Write-Host "  pip install -r requirements.txt"
Write-Host "  python .\code\seed_packager.py"
