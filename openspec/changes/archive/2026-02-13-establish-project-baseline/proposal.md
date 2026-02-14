## Why

The Zotero TagVocab project has undergone a complete architectural redesign — shifting from an external-fetcher pipeline to an LLM-driven interactive vocabulary management system. This change establishes the **project baseline**: documenting the current state of all capabilities as specs so future changes can be tracked against a known-good reference point.

## What Changes

- No code changes — this is a **documentation-only baseline**.
- Captures the current architecture, vocabulary schema, validation logic, and governance rules as formal specs.
- All existing files remain unchanged; this change only creates spec documents.

## Capabilities

### New Capabilities
- `faceted-vocab-schema`: Defines the 8-facet tag system, canonical format rules, abbreviation governance, and the `tags.yaml` data model (278 tags across field/topic/method/model/ai_task/data/tool/status).
- `vocab-validation`: Defines the validation contract — what `scripts/validate.py` checks (duplicates, facet membership, abbreviation casing, format regex, deprecated field type).
- `llm-interactive-workflow`: Defines the interactive vocabulary-building protocol — session workflow, LLM rules, batch sizes, and governance tiers for adding tags.

### Modified Capabilities
_(none — this is the initial baseline)_

## Impact

- No code impact — specs only.
- Future changes will reference these baseline specs.
