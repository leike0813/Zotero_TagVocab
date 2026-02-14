## MODIFIED Requirements

### Requirement: tags.yaml data model
Each entry in `tags.yaml` SHALL contain: `tag` (string, required), `facet` (string, required), `source` (string), `note` (string), `deprecated` (boolean). **Additionally**, `tags.yaml` is now a generated file produced by `compile_vocab.py` from per-facet source files. The authoritative source of truth is the per-facet files.

#### Scenario: Complete tag entry
- **WHEN** a tag entry has all fields including `tag`, `facet`, `source`, `note`, `deprecated`
- **THEN** the system SHALL accept it as a valid entry

#### Scenario: Missing tag field
- **WHEN** a tag entry is missing the `tag` field
- **THEN** the system SHALL report a validation error

#### Scenario: Tags.yaml is auto-generated
- **WHEN** `tags/tags.yaml` is read
- **THEN** it SHALL contain a header comment indicating it is auto-generated from per-facet files
