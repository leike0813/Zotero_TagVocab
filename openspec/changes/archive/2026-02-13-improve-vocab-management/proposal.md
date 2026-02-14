## Why

The vocabulary has grown to 278 tags across 8 facets. Two pain points have emerged:

1. **Single-file bottleneck**: All tags live in one `tags.yaml` (1500+ lines), making browsing and editing by facet difficult.
2. **Agent dependency**: Every vocabulary operation (add, search, review) requires an LLM agent session. The user needs lightweight CLI tools for self-service management.

## What Changes

- **Split `tags.yaml` into per-facet files** (`tags/field.yaml`, `tags/topic.yaml`, etc.) with a merge/compile step that produces a combined `tags.yaml` for downstream consumers.
- **Add interactive CLI tools**:
  - `scripts/add_tag.py` — interactively add a new tag (prompts for facet, value, note; validates before writing)
  - `scripts/search_tags.py` — fuzzy search across all facet files
  - `scripts/stats.py` — show vocabulary stats (counts per facet, recent additions, etc.)
  - `scripts/export_tags.py` — export tag list in multiple formats (YAML, JSON, Markdown, plain text), with optional facet filtering
  - `scripts/compile_vocab.py` — updated to merge per-facet files into a single `tags.yaml`
- **Update `validate.py`** to validate both per-facet files and the compiled output.

## Capabilities

### New Capabilities
- `per-facet-storage`: Splitting the monolithic `tags.yaml` into per-facet files with a compile/merge workflow.
- `interactive-cli`: Interactive command-line tools for self-service vocabulary management (add, search, stats, export).

### Modified Capabilities
- `vocab-validation`: Extend validation to cover per-facet files in addition to the compiled `tags.yaml`.
- `faceted-vocab-schema`: Update schema to define per-facet file structure and the compile contract.

## Impact

- `tags/tags.yaml` becomes a **compiled output** (generated, not hand-edited).
- New files: `tags/field.yaml`, `tags/topic.yaml`, `tags/method.yaml`, `tags/model.yaml`, `tags/ai_task.yaml`, `tags/data.yaml`, `tags/tool.yaml`, `tags/status.yaml`.
- New scripts: `add_tag.py`, `search_tags.py`, `stats.py`, `export_tags.py`.
- Modified scripts: `validate.py`, `compile_vocab.py`.
- No external dependencies added (uses only `pyyaml` + stdlib).
