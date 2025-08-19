# Contributing to Keystone Expert Catalog

Thank you for helping build the Keystone Expert Catalog. This guide explains how to add new experts, extend domains, and update governance documents.

---

## 📂 Repository Structure

```
Keystone-GPT/
├── steward.seed.json
├── scribe.seed.json
├── strategist.seed.json
├── catalog/
│   └── experts/           # Expert persona JSON files
│       ├── exp-0001-name.json
│       ├── exp-0002-name.json
│   └── index.json         # Auto-generated index file
├── ROADMAP.md             # Project roadmap
├── CONTRIBUTING.md        # Contribution guide (this file)
```

---

## 👤 Adding a New Expert Persona

1. **Create a JSON file** in `/catalog/experts/` using the schema (spine + extensions).

   * Filename format: `exp-XXXX-slugified-name.json` (e.g. `exp-0004-jane-doe.json`).
2. **Required spine fields**: `id`, `name`, `domains`, `alignment`, `last_refreshed`.
3. **Optional but encouraged**: `tags`, `credibility`, `availability`, `contact`.
4. **Extensions**: Place domain-specific fields inside the `extensions` object.

   * Example: `ai_research`, `climate_policy`, `systems_engineering`.
5. **Commit changes** and open a Pull Request (PR).

---

## ✅ Validation

* GitHub Actions will automatically:

  * Validate schema compliance.
  * Rebuild `catalog/index.json`.
* PRs with malformed or incomplete personas will fail CI checks.

---

## 🧩 Adding or Updating Domain Extensions

1. Propose new extension fields in the PR description.
2. Update the **registry of extensions** (to be established under `/catalog/extensions/`).
3. Ensure new fields:

   * Have clear naming.
   * Do not duplicate existing fields.
   * Are generalizable within the domain.

---

## 📜 Updating the Roadmap

* `ROADMAP.md` is updated via Pull Requests.
* Include rationale for shifting goals or adding new ones.
* Major roadmap changes should be reviewed by maintainers for alignment.

---

## 🔒 Governance & Alignment Rules

* Every persona must include an `alignment` field describing why they fit mission goals.
* Entries older than **1 year** should be flagged for refresh.
* Sensitive data (private contact info, unpublished work) must not be included without consent.

---

## 🌐 Future-Proofing Guidelines

* Add multilingual tags where possible.
* Include provenance (`manual`, `auto-ingested`, `peer-verified`).
* Track verification levels and confidence scores when available.

---

## 🙌 How to Contribute

1. Fork the repo & create a feature branch.
2. Add or update personas, extensions, or roadmap items.
3. Run local validation (optional, but recommended).
4. Push changes and open a Pull Request.
5. Maintainers will review for schema alignment, mission fit, and governance rules.

Thank you for helping us grow a trustworthy, extensible expert catalog.
