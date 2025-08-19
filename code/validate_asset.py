import sys, json, yaml, jsonschema
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schema" / "metadata-schema.yaml"

def validate(doc):
    with open(SCHEMA, "r", encoding="utf-8") as fh:
        schema = yaml.safe_load(fh)
    jsonschema.validate(instance=doc, schema=schema)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python code/validate_asset.py <path-to-yaml-or-json>")
        sys.exit(1)
    p = Path(sys.argv[1])
    data = yaml.safe_load(p.read_text(encoding="utf-8")) if p.suffix in [".yml",".yaml"] else json.loads(p.read_text(encoding="utf-8"))
    validate(data)
    print("OK:", p.name)
