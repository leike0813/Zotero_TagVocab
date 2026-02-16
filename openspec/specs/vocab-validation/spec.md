## Purpose
Ensure vocabulary data integrity through rigorous validation rules.
## Requirements
### Requirement: Validate tag format
The validator SHALL load the tag format regex from `protocol/protocol.yaml` and the facet enum from `protocol/schema/facet.schema.yaml` instead of hardcoding. All validation logic remains the same.

#### Scenario: Tag pattern from protocol
- **WHEN** `validate.py` checks tag format
- **THEN** the regex SHALL be loaded from `protocol/protocol.yaml` field `tag_pattern`

#### Scenario: Facet enum from protocol
- **WHEN** `validate.py` checks facet membership
- **THEN** the allowed set SHALL be loaded from `protocol/schema/facet.schema.yaml`

### Requirement: Validate no duplicates
The validator SHALL detect both exact-match and case-insensitive duplicate tags. **Additionally**, in `--per-facet` mode it SHALL check for cross-file duplicates.

#### Scenario: Exact duplicate detected
- **WHEN** the same tag string appears twice
- **THEN** it SHALL report a duplicate error

#### Scenario: Cross-file duplicate detected in per-facet mode
- **WHEN** `tags/topic.yaml` and `tags/method.yaml` both contain the same tag
- **THEN** `validate.py --per-facet` SHALL report a cross-file duplicate error

### Requirement: Validate facet-filename consistency
In `--per-facet` mode, the validator SHALL check that every entry's `facet` field matches the filename it resides in.

#### Scenario: Facet mismatch detected
- **WHEN** `tags/topic.yaml` contains an entry with `facet: method`
- **THEN** `validate.py --per-facet` SHALL report a facet-filename mismatch

### Requirement: Validate abbreviation casing
The validator SHALL still check abbreviation casing, but the behavior contract is now defined in `protocol/operations/validate.yaml`.

#### Scenario: Behavior matches protocol contract
- **WHEN** `validate.py` runs abbreviation checks
- **THEN** the checks SHALL match the preconditions defined in `protocol/operations/validate.yaml`

