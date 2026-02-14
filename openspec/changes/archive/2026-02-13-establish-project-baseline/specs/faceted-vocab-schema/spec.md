## ADDED Requirements

### Requirement: Canonical tag format
All tags SHALL follow the format `facet:value` where:
- `facet` is always lowercase
- `value` uses `/` for hierarchy and `-` for multiword
- No spaces are permitted anywhere in the tag string

#### Scenario: Valid hierarchical tag
- **WHEN** a tag `field:CE/UG/Tunnel` is proposed
- **THEN** the system SHALL accept it as a valid canonical tag

#### Scenario: Invalid tag with spaces
- **WHEN** a tag `field:civil engineering` is proposed
- **THEN** the system SHALL reject it as non-canonical

### Requirement: Eight core facets
The system SHALL support exactly eight facets: `field`, `topic`, `method`, `model`, `ai_task`, `data`, `tool`, `status`. Tags using any other facet prefix SHALL be rejected.

#### Scenario: Known facet accepted
- **WHEN** a tag with facet `ai_task` is submitted
- **THEN** the system SHALL accept the facet as valid

#### Scenario: Unknown facet rejected
- **WHEN** a tag with facet `lithology` is submitted
- **THEN** the system SHALL reject the facet as not in the allowed set

### Requirement: Abbreviation governance
Abbreviations registered in `abbrev.yaml` SHALL appear in UPPERCASE within canonical tags. Non-abbreviation parts SHALL be lowercase.

#### Scenario: Registered abbreviation in uppercase
- **WHEN** a tag `model:DL/CNN` contains segments `DL` and `CNN` which are in `abbrev.yaml`
- **THEN** the system SHALL accept them as correctly cased

#### Scenario: Registered abbreviation in lowercase
- **WHEN** a tag `model:dl/cnn` uses lowercase for registered abbreviations
- **THEN** the system SHALL flag a casing violation

### Requirement: Field three-segment hierarchy
The `field:` facet SHALL use the structure `field:<L1>/<L2>/<direction>` where L1 is a top-level discipline abbreviation, L2 is a sub-discipline, and direction (optional) is a specialization.

#### Scenario: Three-segment field tag
- **WHEN** `field:CE/UG/Tunnel` is proposed
- **THEN** the system SHALL accept it as a valid field tag with L1=CE, L2=UG, direction=Tunnel

### Requirement: tags.yaml data model
Each entry in `tags.yaml` SHALL contain: `tag` (string, required), `facet` (string, required), `source` (string), `note` (string), `deprecated` (boolean).

#### Scenario: Complete tag entry
- **WHEN** a tag entry has all fields including `tag`, `facet`, `source`, `note`, `deprecated`
- **THEN** the system SHALL accept it as a valid entry

#### Scenario: Missing tag field
- **WHEN** a tag entry is missing the `tag` field
- **THEN** the system SHALL report a validation error

### Requirement: No duplicate tags
The vocabulary SHALL NOT contain duplicate tag strings. Both exact-match and case-insensitive duplicates SHALL be rejected.

#### Scenario: Exact duplicate detected
- **WHEN** `topic:tunnel` appears twice in `tags.yaml`
- **THEN** the system SHALL report a duplicate error

#### Scenario: Case-insensitive duplicate detected
- **WHEN** both `model:DL/CNN` and `model:DL/Cnn` exist
- **THEN** the system SHALL report a case-insensitive duplicate error
