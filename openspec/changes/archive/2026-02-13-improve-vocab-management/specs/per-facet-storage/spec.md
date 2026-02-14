## ADDED Requirements

### Requirement: Per-facet file structure
Each of the 8 facets SHALL have its own YAML file at `tags/<facet>.yaml` (e.g. `tags/field.yaml`, `tags/topic.yaml`). Each file SHALL be a YAML list with entries containing: `tag`, `facet`, `source`, `note`, `deprecated`.

#### Scenario: Facet file exists for each facet
- **WHEN** the vocabulary is initialized
- **THEN** there SHALL be exactly 8 facet files: `field.yaml`, `topic.yaml`, `method.yaml`, `model.yaml`, `ai_task.yaml`, `data.yaml`, `tool.yaml`, `status.yaml`

#### Scenario: Entry schema consistency
- **WHEN** a tag entry is read from any per-facet file
- **THEN** it SHALL have the same schema as the compiled `tags.yaml` entries (tag, facet, source, note, deprecated)

### Requirement: Facet field matches filename
Every entry in `tags/<facet>.yaml` SHALL have its `facet` field equal to `<facet>`. A tag in `topic.yaml` with `facet: method` is invalid.

#### Scenario: Mismatched facet detected
- **WHEN** `tags/topic.yaml` contains an entry with `facet: method`
- **THEN** validation SHALL report a facet mismatch error

### Requirement: Compile to single file
`compile_vocab.py` SHALL read all 8 per-facet files, merge them, sort deterministically (by facet then tag), and write `tags/tags.yaml` with a header comment marking it as auto-generated.

#### Scenario: Successful compile
- **WHEN** `compile_vocab.py` is run
- **THEN** it SHALL produce `tags/tags.yaml` containing all tags from all facet files, sorted by facet then tag

#### Scenario: Auto-generated header
- **WHEN** `tags/tags.yaml` is produced by compile
- **THEN** the first line SHALL be a comment indicating the file is auto-generated

### Requirement: Tags.yaml is generated output
`tags/tags.yaml` SHALL be treated as a generated file. Direct edits to it will be overwritten on next compile.

#### Scenario: Manual edit overwritten
- **WHEN** a user manually edits `tags/tags.yaml` and then runs `compile_vocab.py`
- **THEN** the manual edit SHALL be overwritten by the compiled output
