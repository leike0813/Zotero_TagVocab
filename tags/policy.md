# Governance Policy

## Faceted Tag Format
- `facet:value` or `facet:path/leaf`
- Facet is **always lowercase**
- Hierarchy uses `/`
- Multiword uses `-`
- No spaces anywhere

## Core Facets
- `field:`  (discipline / domain)
- `topic:`  (problem/object)
- `method:` (approach / workflow)
- `model:`  (model/algorithm/constitutive/solver family)
- `tool:`   (software/platform)
- `status:` (workflow state)

## Abbreviations
- Defined in `abbrev.yaml`.
- Must be UPPERCASE in canonical tags.

## Vocabulary Building
- Tags are built through **interactive LLM sessions**.
- Every tag must be explicitly confirmed by the user before inclusion.
- No external data fetches; the LLM uses general knowledge to propose candidates.

## LTS Rules
- Within an LTS window: no breaking renames of canonical tags.
- Allowed: additive new tags, new aliases, deprecation.
- Deprecated tags are retained (not deleted) until next LTS cycle.
