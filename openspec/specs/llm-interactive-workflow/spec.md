## ADDED Requirements

### Requirement: Session workflow
The LLM interactive workflow SHALL follow this sequence: (1) user describes facet area, (2) LLM proposes candidates, (3) user reviews accept/reject/modify, (4) LLM writes accepted tags to `tags.yaml`, (5) LLM runs `validate.py` to confirm consistency.

#### Scenario: Complete session
- **WHEN** a user requests tags for a new topic area
- **THEN** the LLM SHALL propose candidates, wait for approval, write accepted tags, and validate

### Requirement: Present before write
The LLM SHALL present all candidate tags to the user before writing any tag to `tags.yaml`. No tag SHALL be written without explicit user confirmation.

#### Scenario: User rejects a tag
- **WHEN** the user rejects a proposed tag
- **THEN** that tag SHALL NOT be written to `tags.yaml`

#### Scenario: User modifies a tag
- **WHEN** the user requests a modification to a proposed tag
- **THEN** the modified version SHALL be written instead of the original

### Requirement: Canonical format enforcement
The LLM SHALL propose all tags in canonical `facet:slug` format, respecting abbreviation rules from `abbrev.yaml`.

#### Scenario: Abbreviation in proposal
- **WHEN** the LLM proposes a tag containing a registered abbreviation
- **THEN** the abbreviation SHALL appear in UPPERCASE

### Requirement: Duplicate checking
The LLM SHALL check proposed tags against existing `tags.yaml` content before presenting them to the user. Duplicates and near-synonyms SHALL be flagged.

#### Scenario: Existing tag proposed
- **WHEN** the LLM would propose a tag that already exists in `tags.yaml`
- **THEN** it SHALL omit the duplicate from the proposal

### Requirement: Batch size
The LLM SHOULD propose tags in batches of 10–30 for manageable review.

#### Scenario: Large proposal
- **WHEN** the LLM has 50+ candidate tags
- **THEN** it SHOULD split them into batches of 10–30

### Requirement: Facet restriction
The LLM SHALL NOT create tags outside the 8 defined facets without explicit user approval to add a new facet.

#### Scenario: New facet requested
- **WHEN** the LLM identifies a need for a new facet (e.g., `material:`)
- **THEN** it SHALL ask the user for approval before proposing tags in that facet

### Requirement: Governance tiers
Tag addition SHALL follow governance tiers: `topic:` (easiest to add) → `tool:` → `model:` → `method:` → `status:` and `field:` (strictest, requires explicit justification).

#### Scenario: Adding a field tag
- **WHEN** the LLM proposes a new `field:` tag
- **THEN** it SHALL include justification for why the discipline truly expands the schema
