## Context

The vocabulary has 278 tags in a single `tags.yaml` (1500+ lines). All management operations require an LLM agent. The user needs:
1. Per-facet file organization for readability
2. Self-service CLI tools to reduce agent dependency

Current scripts: `validate.py` (checker), `compile_vocab.py` (decision compiler).

## Goals / Non-Goals

**Goals:**
- Split tags into 8 per-facet YAML files, keeping a compiled `tags.yaml` as output
- Create 4 new CLI scripts: `add_tag.py`, `search_tags.py`, `stats.py`, `export_tags.py`
- Update `validate.py` and `compile_vocab.py` to work with per-facet files
- All scripts runnable without LLM agent — pure interactive CLI

**Non-Goals:**
- No web UI or GUI
- No Zotero API integration (that's a separate future change)
- No changes to tag content or governance rules

## Decisions

### 1. Per-facet file layout

Each facet gets its own file at `tags/<facet>.yaml` (e.g. `tags/field.yaml`, `tags/topic.yaml`). Each file is a plain YAML list with the same entry schema as before (`tag`, `facet`, `source`, `note`, `deprecated`).

`tags/tags.yaml` becomes a **generated file** produced by `compile_vocab.py`. It will have a header comment marking it as auto-generated.

**Why not a `tags/` subdirectory?** The files are already in `tags/`. Using `tags/facets/` would add unnecessary depth. Direct `tags/<facet>.yaml` is flat and discoverable.

### 2. Compile workflow

`compile_vocab.py` reads all 8 per-facet files, merges, sorts deterministically (by facet then tag), and writes `tags.yaml`. This is the single source of truth for downstream consumers.

**Why keep compiled tags.yaml?** Backward compatibility — any tool expecting a single file still works. Also useful for diff/review of the full vocabulary.

### 3. Interactive CLI design

All scripts use Python `argparse` + `input()` for interactivity. No external TUI libraries — keeps dependencies at `pyyaml` only.

- `add_tag.py`: Prompts for facet (with numbered menu), value, note. Validates format + duplicates before appending to the correct facet file. Runs compile after.
- `search_tags.py`: Takes a query string, does case-insensitive substring match across all facet files. Shows matching tags with facet and note.
- `stats.py`: Reads all facet files, prints counts per facet, total, and optionally the N most recent additions.
- `export_tags.py`: Outputs tag strings only (no metadata) in chosen format. Supports `--format {yaml,json,md,txt}` and `--facet` filter.

### 4. Validation extension

`validate.py` gains a `--per-facet` mode that validates each `tags/<facet>.yaml` individually, plus cross-file duplicate checks. Default mode still validates the compiled `tags.yaml`.

## Risks / Trade-offs

- **Migration risk**: Splitting the file could cause data loss if done incorrectly. → Mitigation: validate before and after split, keep compiled tags.yaml for comparison.
- **Compile step required**: After `add_tag.py`, users must remember to compile (or script auto-compiles). → Mitigation: `add_tag.py` auto-runs compile after adding.
- **No fuzzy search library**: Substring match is simple but misses typos. → Acceptable for now; can add `rapidfuzz` later if needed.
