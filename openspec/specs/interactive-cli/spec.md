## Purpose
Provide interactive CLI tools for managing the vocabulary.
## Requirements
### Requirement: Add tag interactively
`add_tag.py` SHALL load validation rules (facet enum, tag pattern, abbreviation rules) from `protocol/` at runtime instead of hardcoding them. It SHALL still prompt the user interactively and auto-compile after adding.

#### Scenario: Facet list comes from protocol
- **WHEN** `add_tag.py` displays the facet selection menu
- **THEN** the facet list SHALL be loaded from `protocol/schema/facet.schema.yaml`

#### Scenario: Tag pattern comes from protocol
- **WHEN** `add_tag.py` validates a tag value
- **THEN** the regex pattern SHALL be loaded from `protocol/protocol.yaml`

### Requirement: Search tags
`search_tags.py` SHALL load the facet list from `protocol/schema/facet.schema.yaml` instead of hardcoding. Behavior otherwise unchanged.

#### Scenario: Facet filter options from protocol
- **WHEN** the user uses `--facet` argument
- **THEN** the valid choices SHALL match the facet enum from the protocol

### Requirement: Vocabulary statistics
`stats.py` SHALL load the facet list from `protocol/schema/facet.schema.yaml`. Behavior otherwise unchanged.

#### Scenario: Stats facet iteration from protocol
- **WHEN** `stats.py` iterates over facets
- **THEN** the facet list SHALL come from the protocol

### Requirement: Export tags
`export_tags.py` SHALL load the facet list from `protocol/schema/facet.schema.yaml`. Behavior otherwise unchanged.

#### Scenario: Export facet filter from protocol
- **WHEN** the user uses `--facet` to filter export
- **THEN** valid facet values SHALL come from the protocol

