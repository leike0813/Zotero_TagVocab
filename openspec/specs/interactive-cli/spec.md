## ADDED Requirements

### Requirement: Add tag interactively
`add_tag.py` SHALL prompt the user to select a facet (numbered menu), enter a tag value, and enter a note. It SHALL validate the tag format and check for duplicates before appending to the correct per-facet file. It SHALL auto-run compile after adding.

#### Scenario: Successful tag addition
- **WHEN** the user runs `add_tag.py` and enters facet=topic, value=karst, note=岩溶
- **THEN** the entry SHALL be appended to `tags/topic.yaml` and `compile_vocab.py` SHALL be triggered

#### Scenario: Duplicate rejected
- **WHEN** the user tries to add a tag that already exists
- **THEN** the script SHALL display an error and NOT write the duplicate

#### Scenario: Invalid format rejected
- **WHEN** the user enters a value with spaces (e.g. "rock bolt")
- **THEN** the script SHALL display a format error and prompt to retry

### Requirement: Search tags
`search_tags.py` SHALL accept a query string and perform case-insensitive substring matching across all per-facet files. It SHALL display matching tags with their facet and note.

#### Scenario: Substring match
- **WHEN** the user searches for "tunnel"
- **THEN** all tags containing "tunnel" (case-insensitive) SHALL be listed with facet and note

#### Scenario: No results
- **WHEN** the user searches for a term with no matches
- **THEN** the script SHALL display "No matching tags found"

### Requirement: Vocabulary statistics
`stats.py` SHALL read all per-facet files and display: tag count per facet, total count, and optionally the N most recent additions.

#### Scenario: Basic stats
- **WHEN** the user runs `stats.py`
- **THEN** it SHALL show a table with facet names and tag counts, plus the total

#### Scenario: Recent additions
- **WHEN** the user runs `stats.py --recent 5`
- **THEN** it SHALL also show the 5 most recently added tags (from file order, last entries)

### Requirement: Export tags
`export_tags.py` SHALL output tag strings only (no metadata) in the chosen format. It SHALL support `--format {yaml,json,md,txt}` and optional `--facet` filter.

#### Scenario: Export all as JSON
- **WHEN** the user runs `export_tags.py --format json`
- **THEN** it SHALL output a JSON array of all tag strings

#### Scenario: Export filtered by facet as Markdown
- **WHEN** the user runs `export_tags.py --format md --facet topic`
- **THEN** it SHALL output only topic tags as a Markdown list

#### Scenario: Export as plain text
- **WHEN** the user runs `export_tags.py --format txt`
- **THEN** it SHALL output one tag per line, no formatting

#### Scenario: Export as YAML
- **WHEN** the user runs `export_tags.py --format yaml`
- **THEN** it SHALL output a YAML list of tag strings

#### Scenario: Export to file
- **WHEN** the user runs `export_tags.py --format json -o output.json`
- **THEN** it SHALL write the output to `output.json` instead of stdout
