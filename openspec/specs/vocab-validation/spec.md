## MODIFIED Requirements

### Requirement: Validate tag format
The validator SHALL check that every tag matches the regex pattern `^[a-z_]+:[a-zA-Z0-9/_.-]+$` and reject tags that do not conform. **Additionally**, it SHALL support a `--per-facet` flag to validate individual per-facet files.

#### Scenario: Valid tag passes
- **WHEN** `validate.py` checks `topic:face-stability`
- **THEN** it SHALL pass the format check

#### Scenario: Invalid tag fails
- **WHEN** `validate.py` checks a tag containing spaces
- **THEN** it SHALL report a format error with the tag name and index

#### Scenario: Per-facet mode validates individual files
- **WHEN** `validate.py --per-facet` is run
- **THEN** it SHALL validate each `tags/<facet>.yaml` file individually

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
