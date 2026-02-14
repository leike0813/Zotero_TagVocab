# Tasks — Define Vocab Protocol

## Protocol Definition
- [ ] Create `protocol/protocol.yaml` (root manifest: version, facets, tag_pattern, file refs)
- [ ] Create `protocol/schema/tag.schema.yaml` (JSON Schema for tag entries)
- [ ] Create `protocol/schema/facet.schema.yaml` (facet enum, per-facet rules)
- [ ] Create `protocol/schema/abbrev.schema.yaml` (abbreviation registry model)
- [ ] Create `protocol/operations/create_tag.yaml`
- [ ] Create `protocol/operations/read_tags.yaml`
- [ ] Create `protocol/operations/search_tags.yaml`
- [ ] Create `protocol/operations/update_tag.yaml`
- [ ] Create `protocol/operations/delete_tag.yaml`
- [ ] Create `protocol/operations/export_tags.yaml`
- [ ] Create `protocol/operations/validate.yaml`
- [ ] Create `protocol/operations/compile.yaml`
- [ ] Create `protocol/operations/stats.yaml`

## Script Refactoring (Reference Implementation)
- [ ] Create `scripts/lib/protocol_loader.py` (loads + caches protocol schemas)
- [ ] Refactor `validate.py` to load rules from protocol
- [ ] Refactor `add_tag.py` to load rules from protocol
- [ ] Refactor `search_tags.py` to load facets from protocol
- [ ] Refactor `stats.py` to load facets from protocol
- [ ] Refactor `export_tags.py` to load facets from protocol
- [ ] Refactor `compile_vocab.py` to load facets from protocol

## Verification
- [ ] `validate.py --strict` passes (278 tags)
- [ ] `validate.py --per-facet --strict` passes
- [ ] All scripts work with protocol-loaded rules
- [ ] Protocol YAML files are syntactically valid
- [ ] No hardcoded ALLOWED_FACETS or TAG_PATTERN remain in scripts
