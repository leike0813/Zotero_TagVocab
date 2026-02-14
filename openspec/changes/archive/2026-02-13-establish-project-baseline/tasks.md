# Tasks — Establish Project Baseline

All tasks are verification-only (no code changes).

## Verify Vocabulary Schema
- [x] 278 tags across 8 facets (field, topic, method, model, ai_task, data, tool, status)
- [x] All tags follow canonical `facet:value` format
- [x] Abbreviation registry (`abbrev.yaml`) contains all used abbreviations
- [x] `validate.py --strict` passes with zero issues

## Verify Validation Script
- [x] `validate.py` checks: format regex, facet membership, abbreviation casing, duplicates, deprecated type
- [x] `--strict` flag returns exit code 1 on failure, 0 on success
- [x] Case-insensitive duplicate detection works

## Verify LLM Workflow
- [x] AGENTS.md documents the interactive session workflow (propose → review → write → validate)
- [x] 文献Tag维护说明.md defines governance tiers, naming rules, and maintenance procedures
- [x] tags/policy.md captures governance rules
- [x] tags/sources.yaml lists `llm-interactive` as primary source

## Verify Repo Structure
- [x] Only 2 scripts: `validate.py`, `compile_vocab.py`
- [x] No leftover fetcher infrastructure (authority/, data/, proposals/, runs/)
- [x] `.gitignore` in place
- [x] `requirements.txt` contains only `pyyaml`
