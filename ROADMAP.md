# Keystone Expert Catalog – Roadmap

## 🎯 Mission

Build a curated, mission-aligned catalog of experts that is:

* **Searchable** across domains and tags.
* **Extensible** with domain-specific detail.
* **Governed** for trust, provenance, and alignment.
* **Scalable** from a handful of seed personas to thousands.

---

## 📍 Current State (2025-08)

* **Personas**: Spine + extensions schema drafted.
* **Catalog structure**: JSON files under `/catalog/experts/`.
* **Indexing**: Auto-generated `catalog/index.json` via GitHub Actions.
* **Retrieval**: Python script + FastAPI skeleton.
* **Governance**: Alignment check enforced via schema validation.

---

## 🚦 Near-Term Goals (Next 3–6 Months)

* [ ] Finalize **spine schema** as JSON Schema file.
* [ ] Draft **registry of domain extensions** (AI, Climate, Systems Eng).
* [ ] Automate index validation + rebuild with GitHub Actions (baseline done).
* [ ] Deploy **FastAPI retrieval service** (local/Docker).
* [ ] Add **provenance field** (manual vs. ingested, source links).
* [ ] Define **basic governance rules** (alignment required, stale > 1 yr flagged).
* [ ] Introduce **verification levels** (self-reported, peer-verified, auto-ingested).
* [ ] Add **confidence score** to entries based on validation checks.
* [ ] Add **changelog field** in persona JSONs for version tracking.

---

## 🛤 Mid-Term Goals (6–12 Months)

* [ ] Expand catalog to 50–100 experts (seed + ingestion).
* [ ] Integrate **ORCID & Google Scholar APIs** for researcher ingestion.
* [ ] Integrate **Patents DB** for engineering extensions.
* [ ] Add **policy document scraper** (IPCC, UN, EU).
* [ ] Support **faceted search** (filter by domain, availability, credibility).
* [ ] Add **multi-lingual tags/domains** with translations/synonyms.
* [ ] Introduce **Unicode-safe indexing** for non-English scripts.
* [ ] Logging & analytics: track queries + retrieval usage.
* [ ] Establish **roles & permissions** for persona contributions.

---

## 🌍 Long-Term Goals (1–2 Years)

* [ ] Migrate index backend to **SQLite or ElasticSearch**.
* [ ] Add **semantic search embeddings** for deeper retrieval.
* [ ] Implement **ranked results** (best match, not just first match).
* [ ] Establish **extension governance framework** (versioning, registry).
* [ ] Implement **trust scores** (verification level, credibility weighting).
* [ ] Build **API authentication & role-based permissions**.
* [ ] Consider **consent/privacy framework** for non-public experts.
* [ ] Publish **curated slices** of the catalog (public vs. private subsets).
* [ ] Add **expiration markers** for stale entries (>1 yr since refresh).
* [ ] Establish **analytics dashboards** for catalog usage.

---

## 🧭 Guiding Principles

1. **Spine first, extensions second** → core schema must remain stable.
2. **Metadata is governance** → provenance, freshness, alignment are as important as content.
3. **Automate the boring parts** → index rebuilds, stale checks, ingestion pipelines.
4. **Humans in the loop** → mission alignment requires reflection, not just automation.
5. **Future-proof by hooks** → leave room for semantic search, multilingual, and trust scoring.
