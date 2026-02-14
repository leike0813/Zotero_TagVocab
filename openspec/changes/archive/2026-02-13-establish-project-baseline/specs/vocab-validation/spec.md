## ADDED Requirements

### Requirement: Validate tag format
The validator SHALL check that every tag matches the regex pattern `^[a-z_]+:[a-zA-Z0-9/_.-]+$` and reject tags that do not conform.

#### Scenario: Valid tag passes
- **WHEN** `validate.py` checks `topic:face-stability`
- **THEN** it SHALL pass the format check

#### Scenario: Invalid tag fails
- **WHEN** `validate.py` checks a tag containing spaces
- **THEN** it SHALL report a format error with the tag name and index

### Requirement: Validate facet membership
The validator SHALL check that every tag's facet prefix is in the allowed set `{field, topic, method, model, ai_task, data, tool, status}`.

#### Scenario: Valid facet passes
- **WHEN** a tag with prefix `ai_task` is checked
- **THEN** it SHALL pass the facet membership check

#### Scenario: Invalid facet fails
- **WHEN** a tag with prefix `lithology` is checked
- **THEN** it SHALL report the facet as not in the allowed set

### Requirement: Validate abbreviation casing
The validator SHALL check that any path segment matching a key in `abbrev.yaml` uses the registered UPPERCASE form.

#### Scenario: Correct casing passes
- **WHEN** `model:DL/CNN` is checked and `dl→DL`, `cnn→CNN` are in `abbrev.yaml`
- **THEN** it SHALL pass the abbreviation check

#### Scenario: Incorrect casing fails
- **WHEN** `model:dl/cnn` is checked
- **THEN** it SHALL report that `dl` should be `DL` and `cnn` should be `CNN`

### Requirement: Validate no duplicates
The validator SHALL detect both exact-match and case-insensitive duplicate tags.

#### Scenario: Exact duplicate detected
- **WHEN** the same tag string appears twice
- **THEN** it SHALL report a duplicate error

### Requirement: Validate deprecated field type
The validator SHALL check that the `deprecated` field, if present, is a boolean value.

#### Scenario: Boolean deprecated passes
- **WHEN** a tag has `deprecated: false`
- **THEN** it SHALL pass

#### Scenario: Non-boolean deprecated fails
- **WHEN** a tag has `deprecated: "yes"`
- **THEN** it SHALL report a type error

### Requirement: Strict mode exit code
When run with `--strict`, the validator SHALL exit with code 1 if any issues are found, and code 0 if all checks pass.

#### Scenario: Strict mode with issues
- **WHEN** `validate.py --strict` finds issues
- **THEN** it SHALL exit with code 1

#### Scenario: Strict mode clean
- **WHEN** `validate.py --strict` finds no issues
- **THEN** it SHALL exit with code 0
