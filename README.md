# Zotero TagVocab

A **controlled vocabulary management system** for Zotero literature tags — featuring a language-agnostic protocol, per-facet storage, and interactive CLI tools.

## ✨ Highlights

- **8 faceted tag categories** (`field`, `topic`, `method`, `model`, `ai_task`, `data`, `tool`, `status`) — 278+ curated tags
- **Language-agnostic protocol** — YAML + JSON Schema contracts for all CRUD operations, consumable by any language or LLM agent
- **Per-facet file storage** — one YAML file per facet for easy browsing and maintenance
- **Interactive CLI tools** — add, search, export, and inspect tags without touching code
- **LLM-interactive workflow** — vocabulary built and refined through structured LLM sessions

---

## 📁 Repository Structure

```
Zotero_TagVocab/
├── protocol/                  # Language-agnostic protocol (the contract layer)
│   ├── protocol.yaml          # Root manifest: version, facets, tag pattern
│   ├── schema/                # JSON Schema data models (YAML syntax)
│   │   ├── tag.schema.yaml    # Tag entry schema
│   │   ├── facet.schema.yaml  # Facet enum + governance rules
│   │   └── abbrev.schema.yaml # Abbreviation registry model
│   └── operations/            # CRUD + derived operation contracts
│       ├── create_tag.yaml    ├── update_tag.yaml
│       ├── read_tags.yaml     ├── delete_tag.yaml
│       ├── search_tags.yaml   ├── export_tags.yaml
│       ├── validate.yaml      ├── compile.yaml
│       └── stats.yaml
│
├── tags/                      # Vocabulary data (per-facet YAML files)
│   ├── field.yaml             # field: discipline / domain
│   ├── topic.yaml             # topic: problem / object
│   ├── method.yaml            # method: approach / workflow
│   ├── model.yaml             # model: algorithm / solver
│   ├── ai_task.yaml           # ai_task: ML task type
│   ├── data.yaml              # data: data modality
│   ├── tool.yaml              # tool: software / platform
│   ├── status.yaml            # status: workflow state
│   ├── tags.yaml              # ← compiled output (auto-generated)
│   ├── abbrev.yaml            # Abbreviation registry
│   └── aliases.yaml           # Alias mappings
│
├── scripts/                   # Python reference implementation
│   ├── add_tag.py             # Interactive tag addition
│   ├── search_tags.py         # Substring search
│   ├── stats.py               # Vocabulary statistics
│   ├── export_tags.py         # Multi-format export
│   ├── validate.py            # Format & consistency validation
│   ├── compile_vocab.py       # Merge facet files → tags.yaml
│   └── lib/
│       └── protocol_loader.py # Loads rules from protocol/ at runtime
│
└── AGENTS.md                  # LLM agent guidelines & governance rules
```

---

## 🔧 Protocol

The `protocol/` directory defines a **language-agnostic contract** for all vocabulary operations. It serves as the single source of truth — no rules are hardcoded in scripts.

### Data Schemas (JSON Schema draft-07)

| Schema | Purpose |
|:---|:---|
| `tag.schema.yaml` | Tag entry structure: `tag`, `facet`, `source`, `note`, `deprecated` |
| `facet.schema.yaml` | Facet definitions with hierarchy support and governance tiers |
| `abbrev.schema.yaml` | Abbreviation registry (lowercase → UPPERCASE mapping) |

### Operation Contracts

Each operation YAML defines: **input** (typed params), **output**, **preconditions**, **postconditions**, **errors**, and **side_effects**.

| Operation | Description | Mutates? |
|:---|:---|:---:|
| `create_tag` | Add a new tag with format/duplicate validation | ✓ |
| `read_tags` | List & filter tags by facet | ✗ |
| `search_tags` | Case-insensitive substring search | ✗ |
| `update_tag` | Modify metadata or rename a tag | ✓ |
| `delete_tag` | Soft-delete (deprecate) or hard-delete | ✓ |
| `export_tags` | Export in YAML / JSON / Markdown / Text | ✗ |
| `validate` | Check format, duplicates, abbreviation casing | ✗ |
| `compile` | Merge per-facet files → `tags.yaml` | ✓ |
| `stats` | Per-facet counts and recent additions | ✗ |

### Who Consumes the Protocol?

- **Humans** — read the YAML contracts to understand rules at a glance
- **Python scripts** — load schemas at runtime via `protocol_loader.py`
- **LLM agents** — read operation contracts to know what they can do and how
- **Future implementations** — target the same protocol in TypeScript, Rust, etc.

---

## 🏷️ Tag Format

```
facet:value          # e.g. topic:tunnel
facet:path/leaf      # e.g. field:CE/UG/Tunnel, model:DL/CNN
```

**Rules:**
- Facet prefix is always **lowercase**
- Hierarchy uses `/`, multiword uses `-`, no spaces
- Registered abbreviations must be **UPPERCASE** (e.g., `DL`, `CNN`, `FEM`)
- Pattern: `^[a-z_]+:[a-zA-Z0-9/_.-]+$`

### Facets

| Facet | Description | Example |
|:---|:---|:---|
| `field:` | Discipline / domain | `field:CE/UG/Tunnel` |
| `topic:` | Problem / object | `topic:face-stability` |
| `method:` | Approach / technique | `method:transfer-learning` |
| `model:` | Algorithm / solver | `model:DL/CNN` |
| `ai_task:` | ML task type | `ai_task:segmentation` |
| `data:` | Data modality | `data:point-cloud` |
| `tool:` | Software / platform | `tool:PyTorch` |
| `status:` | Workflow state | `status:3-reading` |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- `pip install pyyaml`

### Common Operations

```bash
# Search for tags
python scripts/search_tags.py tunnel

# View statistics
python scripts/stats.py --recent 10

# Export all tags as JSON
python scripts/export_tags.py --format json -o all_tags.json

# Export one facet as Markdown
python scripts/export_tags.py --format md --facet model

# Add a new tag interactively
python scripts/add_tag.py

# Validate vocabulary
python scripts/validate.py --strict                # compiled file
python scripts/validate.py --per-facet --strict     # per-facet files

# Recompile after manual edits
python scripts/compile_vocab.py
```

---

## 📐 Architecture

```
┌─────────────────────────────────────────┐
│           protocol/ (Contract)          │
│  JSON Schema + Operation YAML           │
│  Language-agnostic · Single source of   │
│  truth for all rules                    │
└──────────────────┬──────────────────────┘
                   │ loads at runtime
┌──────────────────▼──────────────────────┐
│      scripts/lib/protocol_loader.py     │
│  Centralized accessor (lru_cache)       │
└──────────────────┬──────────────────────┘
                   │ used by
┌──────────────────▼──────────────────────┐
│         scripts/ (Reference Impl)       │
│  add_tag · search · stats · export      │
│  validate · compile                     │
└──────────────────┬──────────────────────┘
                   │ reads/writes
┌──────────────────▼──────────────────────┐
│           tags/ (Data Layer)            │
│  Per-facet YAML → compiled tags.yaml    │
└─────────────────────────────────────────┘
```

---

## 📄 License

This project is for personal academic use.
