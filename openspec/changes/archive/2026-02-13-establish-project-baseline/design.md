## Context

This project underwent a complete architectural redesign from an external-fetcher pipeline to an LLM-driven interactive vocabulary management system. The current state:

- **278 tags** across 8 facets (field, topic, method, model, ai_task, data, tool, status)
- **2 scripts**: `validate.py` (format checker) + `compile_vocab.py` (decision compiler)
- **6 vocabulary files** in `tags/`: tags.yaml, aliases.yaml, abbrev.yaml, sources.yaml, changelog.md, policy.md
- **Governance**: `AGENTS.md` + `文献Tag维护说明.md` define all rules

This baseline change captures the current architecture as formal specs — no code changes.

## Goals / Non-Goals

**Goals:**
- Document the 8-facet tag schema, canonical format rules, and data model as a spec
- Document the validation contract (what `validate.py` checks) as a spec
- Document the LLM interactive workflow protocol as a spec
- Provide a known-good baseline for tracking future changes

**Non-Goals:**
- No code modifications
- No vocabulary changes (tags are frozen at 278)
- No new features or capabilities

## Decisions

**1. Three specs, not one monolithic doc**

Splitting into `faceted-vocab-schema`, `vocab-validation`, and `llm-interactive-workflow` keeps each spec focused and independently modifiable. Alternative: a single mega-spec would be harder to maintain and review.

**2. Baseline-only, no implementation tasks**

Since all code already exists and is validated, this change produces specs only. The tasks artifact will confirm spec accuracy against the running system.

## Risks / Trade-offs

- **Specs may drift from reality**: If code changes without updating specs, they become stale. → Mitigation: validation script ensures format invariants hold.
- **Over-documentation**: For a small project, formal specs may be overhead. → Mitigation: keeping specs concise (requirements only, no implementation details).
