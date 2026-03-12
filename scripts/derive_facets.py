#!/usr/bin/env python3
"""
scripts/derive_facets.py

Derives per-facet YAML files from tags/tags.json (the single source of truth).
Use after pulling changes that were contributed via GitHub API.

Usage: python3 scripts/derive_facets.py
"""

import sys
import json
import yaml
from pathlib import Path

# Protocol-driven imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib.protocol_loader import get_facets, get_tags_dir


def main():
    facets = get_facets()
    tags_dir = get_tags_dir()
    json_path = tags_dir / "tags.json"

    if not json_path.exists():
        print(f"❌ {json_path} not found. Run publish.py first.")
        sys.exit(1)

    with open(json_path, "r", encoding="utf-8") as f:
        vocab = json.load(f)

    tags = vocab.get("tags", [])
    if not tags:
        print("⚠️  No tags in JSON. Nothing to derive.")
        return

    # Group tags by facet
    by_facet = {}
    for entry in tags:
        facet = entry.get("facet", "")
        by_facet.setdefault(facet, []).append(entry)

    # Write per-facet files
    written = 0
    for facet in facets:
        entries = by_facet.get(facet, [])
        facet_path = tags_dir / f"{facet}.yaml"

        if not entries:
            # If no entries for this facet, skip (don't overwrite with empty)
            continue

        # Sort within facet by tag string
        entries.sort(key=lambda x: x.get("tag", ""))

        with open(facet_path, "w", encoding="utf-8") as f:
            f.write(f"# {facet} tags\n")
            yaml.dump(entries, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

        written += 1

    # Also update abbrev.yaml if present in JSON
    abbrevs = vocab.get("abbrevs", {})
    if abbrevs:
        abbrev_path = tags_dir / "abbrev.yaml"
        with open(abbrev_path, "w", encoding="utf-8") as f:
            f.write("# Abbreviation registry: lowercase key → UPPERCASE display form\n")
            yaml.dump(abbrevs, f, sort_keys=True, allow_unicode=True, default_flow_style=False)

    total = len(tags)
    print(f"✅ Derived {written} facet files from {json_path}")
    print(f"   {total} tags across {written} facets")
    if abbrevs:
        print(f"   {len(abbrevs)} abbreviations updated")


if __name__ == "__main__":
    main()
