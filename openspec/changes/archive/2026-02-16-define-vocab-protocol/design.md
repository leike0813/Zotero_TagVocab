## Context

Current state: 278 tags across 8 per-facet YAML files, 6 Python scripts, rules hardcoded in source code. The user wants a formal, language-agnostic protocol layer that any implementation can target.

## Goals / Non-Goals

**Goals:**
- Define data schemas in JSON Schema (written as YAML for consistency)
- Define all CRUD + derived operations as YAML contracts with typed inputs/outputs, preconditions, postconditions, and error codes
- Refactor Python scripts to read rules from protocol files (reference implementation)
- Protocol files are the **single source of truth** for all vocabulary rules

**Non-Goals:**
- No REST API or HTTP layer — this is a local protocol
- No code generation tooling — protocol is consumed directly
- No migration tools for other languages — just the protocol definition

## Decisions

### 1. JSON Schema for data models, YAML for operations

Data schemas use JSON Schema draft-07 (written in YAML syntax). This gives us:
- Precise type definitions with constraints (pattern, enum, minLength)
- Tooling ecosystem (validators in every language)
- IDE support for auto-completion

Operations use a custom YAML format (not OpenAPI) because the system is not HTTP-based. Each operation defines: name, description, input parameters, output, preconditions, postconditions, errors, side_effects.

### 2. Operation granularity: 10 operations

| Operation | Description |
|:---|:---|
| `create_tag` | Add a new tag to a facet file |
| `read_tags` | List/filter tags by facet, pattern, deprecated status |
| `search_tags` | Substring/fuzzy search across tags and notes |
| `update_tag` | Modify tag metadata (note, deprecated, rename) |
| `delete_tag` | Remove a tag (hard delete) or deprecate (soft) |
| `export_tags` | Export tag list in yaml/json/md/txt format |
| `validate` | Check consistency of all vocabulary files |
| `compile` | Merge per-facet files into single tags.yaml |
| `stats` | Aggregate counts and recent additions |
| `import_tags` | Batch-import external tags with conflict resolution |

`stats` is kept separate from `read_tags` because it returns aggregated data, not individual entries.
`import_tags` is kept separate from `create_tag` because it handles batch input, multiple formats, and conflict-resolution strategies.

### 3. Protocol loads at runtime via a `protocol_loader` module

A small Python module (`scripts/lib/protocol_loader.py`) loads and caches protocol schemas. All scripts import from this module instead of hardcoding constants. This module is the **only** place where `protocol/` is read.

### 4. Backward compatibility

Old hardcoded constants (`ALLOWED_FACETS`, `TAG_PATTERN`) are replaced by protocol loads. Scripts maintain the same CLI interface — only the internal rule source changes.

## Risks / Trade-offs

- **Indirection cost**: Loading rules from YAML adds a small startup overhead. → Acceptable for CLI tools.
- **Schema drift**: Protocol and scripts could desync. → Mitigated by scripts loading protocol at runtime.
- **Custom operation format**: Not a standard like OpenAPI. → Acceptable since this isn't an HTTP API; the format is simpler and more readable.
