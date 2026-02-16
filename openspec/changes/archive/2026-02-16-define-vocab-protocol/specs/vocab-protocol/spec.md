## Purpose
Define a language-agnostic vocabulary management protocol.

## ADDED Requirements

### Requirement: Protocol root manifest
`protocol/protocol.yaml` SHALL define: protocol version, list of facets, global constraints (tag pattern regex, max tag length), and references to all schema and operation files.

#### Scenario: Agent reads protocol manifest
- **WHEN** an agent or implementation reads `protocol/protocol.yaml`
- **THEN** it SHALL find the protocol version, facet enum, tag format regex, and paths to all schema/operation files

### Requirement: Tag data schema
`protocol/schema/tag.schema.yaml` SHALL be a valid JSON Schema (draft-07, YAML syntax) defining the Tag entry structure: `tag` (string, required, pattern-constrained), `facet` (string, required, enum), `source` (string), `note` (string), `deprecated` (boolean).

#### Scenario: Validate a tag entry against schema
- **WHEN** a tag entry `{tag: "topic:tunnel", facet: "topic", source: "llm-interactive", note: "隧道", deprecated: false}` is validated against the schema
- **THEN** it SHALL pass validation

#### Scenario: Invalid tag entry rejected by schema
- **WHEN** a tag entry missing the `tag` field is validated
- **THEN** the schema SHALL reject it as invalid

### Requirement: Facet schema
`protocol/schema/facet.schema.yaml` SHALL define the facet enum, per-facet rules (e.g., field uses 3-segment hierarchy), and the facet-to-filename mapping.

#### Scenario: Facet enum is authoritative
- **WHEN** any implementation checks whether a facet is allowed
- **THEN** it SHALL read the enum from `protocol/schema/facet.schema.yaml` as the single source of truth

### Requirement: Abbreviation schema
`protocol/schema/abbrev.schema.yaml` SHALL define the abbreviation registry structure: a mapping of lowercase keys to uppercase display forms.

#### Scenario: Abbreviation lookup
- **WHEN** an implementation checks if "cnn" is a registered abbreviation
- **THEN** it SHALL consult the schema-defined structure in `tags/abbrev.yaml`

### Requirement: Operation contract format
Each operation file in `protocol/operations/` SHALL define: `name`, `description`, `input` (typed parameters), `output` (typed return), `preconditions` (list of rules), `postconditions` (list of state changes), `errors` (code + message pairs), and `side_effects` (optional triggered actions).

#### Scenario: Implementation reads create_tag contract
- **WHEN** a developer reads `protocol/operations/create_tag.yaml`
- **THEN** they SHALL find all input parameters with types, all validation rules as preconditions, the expected output, and possible error codes

### Requirement: Ten operations defined
The protocol SHALL define exactly these operations: `create_tag`, `read_tags`, `search_tags`, `update_tag`, `delete_tag`, `export_tags`, `validate`, `compile`, `stats`, `import_tags`.

#### Scenario: Complete operation coverage
- **WHEN** listing all files in `protocol/operations/`
- **THEN** there SHALL be exactly 10 operation YAML files

### Requirement: Protocol is language-agnostic
The protocol SHALL NOT reference any programming language, library, or runtime. All type definitions SHALL use JSON Schema types (string, integer, boolean, array, object).

#### Scenario: No language-specific types
- **WHEN** scanning all protocol files for language-specific references
- **THEN** no references to Python, JavaScript, or any other language SHALL appear
