## Why

The vocabulary management system currently works through ad-hoc Python scripts with rules hardcoded in source code, scattered across `AGENTS.md`, `policy.md`, and `validate.py`. This creates three problems:

1. **No single source of truth** — validation rules, facet lists, format patterns exist in multiple places
2. **Language lock-in** — rules can't be consumed by non-Python implementations (e.g., a future Zotero plugin in TypeScript)
3. **Agent opacity** — LLM agents must reverse-engineer behavior from Python source code rather than reading a machine-consumable contract

A **language-agnostic protocol** solves all three: one canonical definition of data models, operations, and behaviors, stored as YAML + JSON Schema, consumable by humans, agents, and any language runtime.

## What Changes

- **New `protocol/` directory** containing:
  - `protocol.yaml` — root manifest (version, facet enum, global constraints)
  - `schema/tag.schema.yaml` — Tag entry data model (JSON Schema in YAML)
  - `schema/facet.schema.yaml` — Facet rules and enum
  - `schema/abbrev.schema.yaml` — Abbreviation registry model
  - `operations/create_tag.yaml` — Create operation contract
  - `operations/read_tags.yaml` — Query/list/filter contract
  - `operations/search_tags.yaml` — Fuzzy/substring search contract
  - `operations/update_tag.yaml` — Modify metadata / rename contract
  - `operations/delete_tag.yaml` — Deprecate/remove contract
  - `operations/export_tags.yaml` — Format conversion export contract
  - `operations/validate.yaml` — Validation operation contract
  - `operations/compile.yaml` — Merge/compile operation contract
  - `operations/stats.yaml` — Aggregation/statistics contract
- **Refactor existing scripts** to load rules (facet enum, tag pattern, abbreviations) from protocol schemas instead of hardcoding, serving as a **reference implementation**

## Capabilities

### New Capabilities
- `vocab-protocol`: Language-agnostic protocol defining data schemas (JSON Schema) and operation contracts (YAML) for the entire vocabulary CRUD lifecycle.

### Modified Capabilities
- `interactive-cli`: Refactor scripts to load validation rules from protocol schemas, making them a reference implementation of the protocol.
- `vocab-validation`: Validation rules extracted from hardcoded constants into `protocol/schema/` as the single source of truth.

## Impact

- New directory: `protocol/` (13 YAML files)
- Modified scripts: `validate.py`, `add_tag.py`, `search_tags.py`, `export_tags.py`, `stats.py`, `compile_vocab.py` — all load rules from `protocol/` instead of hardcoding
- No new Python dependencies
- **BREAKING** for consumers of hardcoded constants (e.g., `ALLOWED_FACETS` moves to `protocol/schema/facet.schema.yaml`)
