## MODIFIED Requirements

### Requirement: Validate tag format
The validator SHALL load the tag format regex from `protocol/protocol.yaml` and the facet enum from `protocol/schema/facet.schema.yaml` instead of hardcoding. All validation logic remains the same.

#### Scenario: Tag pattern from protocol
- **WHEN** `validate.py` checks tag format
- **THEN** the regex SHALL be loaded from `protocol/protocol.yaml` field `tag_pattern`

#### Scenario: Facet enum from protocol
- **WHEN** `validate.py` checks facet membership
- **THEN** the allowed set SHALL be loaded from `protocol/schema/facet.schema.yaml`

### Requirement: Validate abbreviation casing
The validator SHALL still check abbreviation casing, but the behavior contract is now defined in `protocol/operations/validate.yaml`.

#### Scenario: Behavior matches protocol contract
- **WHEN** `validate.py` runs abbreviation checks
- **THEN** the checks SHALL match the preconditions defined in `protocol/operations/validate.yaml`
