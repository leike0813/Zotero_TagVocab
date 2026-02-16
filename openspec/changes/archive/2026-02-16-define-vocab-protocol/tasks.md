# Tasks — Define Vocab Protocol

## Protocol Definition
- [x] Create `protocol/protocol.yaml` (root manifest: version, facets, tag_pattern, file refs)
- [x] Create `protocol/schema/tag.schema.yaml` (JSON Schema for tag entries)
- [x] Create `protocol/schema/facet.schema.yaml` (facet enum, per-facet rules)
- [x] Create `protocol/schema/abbrev.schema.yaml` (abbreviation registry model)
- [x] Create `protocol/operations/create_tag.yaml`
- [x] Create `protocol/operations/read_tags.yaml`
- [x] Create `protocol/operations/search_tags.yaml`
- [x] Create `protocol/operations/update_tag.yaml`
- [x] Create `protocol/operations/delete_tag.yaml`
- [x] Create `protocol/operations/export_tags.yaml`
- [x] Create `protocol/operations/validate.yaml`
- [x] Create `protocol/operations/compile.yaml`
- [x] Create `protocol/operations/stats.yaml`
- [x] Create `protocol/operations/import_tags.yaml`

## Script Refactoring (Reference Implementation)
- [x] Create `scripts/lib/protocol_loader.py` (loads + caches protocol schemas)
- [x] Refactor `validate.py` to load rules from protocol
- [x] Refactor `add_tag.py` to load rules from protocol
- [x] Refactor `search_tags.py` to load facets from protocol
- [x] Refactor `stats.py` to load facets from protocol
- [x] Refactor `export_tags.py` to load facets from protocol
- [x] Refactor `compile_vocab.py` to load facets from protocol

## Verification
- [x] `validate.py --strict` passes (278 tags)
- [x] `validate.py --per-facet --strict` passes
- [x] All scripts work with protocol-loaded rules
- [x] Protocol YAML files are syntactically valid
- [x] No hardcoded ALLOWED_FACETS or TAG_PATTERN remain in scripts
