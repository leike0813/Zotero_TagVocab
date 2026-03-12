#!/usr/bin/env python3
"""
scripts/publish.py

Generates tags/tags.json from per-facet YAML files and abbrev.yaml.
This JSON file is the single source of truth for external consumers
(e.g., Zotero plugins via GitHub raw URL).

Usage: python3 scripts/publish.py
"""

import sys
import json
import yaml
from pathlib import Path
from datetime import datetime, timezone

# Protocol-driven imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib.protocol_loader import get_facets, get_tags_dir, load_protocol


def load_yaml(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def main():
    protocol = load_protocol()
    facets = get_facets()
    tags_dir = get_tags_dir()
    version = protocol.get("version", "1.0.0")

    # Collect all tags from per-facet files
    all_tags = []
    missing = []
    for facet in facets:
        path = tags_dir / f"{facet}.yaml"
        if not path.exists():
            missing.append(facet)
            continue
        data = load_yaml(path)
        if isinstance(data, list):
            all_tags.extend(data)

    if not all_tags:
        print("❌ No tags found. Nothing to publish.")
        sys.exit(1)

    if missing:
        print(f"⚠️  Missing facet files: {missing}")

    # Deterministic sort
    all_tags.sort(key=lambda x: (x.get("facet", ""), x.get("tag", "")))

    # Load abbreviations
    abbrev_path = tags_dir / "abbrev.yaml"
    abbrevs = {}
    if abbrev_path.exists():
        data = load_yaml(abbrev_path)
        if isinstance(data, dict):
            abbrevs = {k: v for k, v in data.items() if isinstance(v, str)}

    # Build the JSON structure
    vocab = {
        "version": version,
        "updated_at": datetime.now(timezone.utc).isoformat(),
        "facets": facets,
        "tags": all_tags,
        "abbrevs": abbrevs,
        "tag_count": len(all_tags),
    }

    # Write tags/tags.json
    output = tags_dir / "tags.json"
    with open(output, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)
        f.write("\n")  # trailing newline

    print(f"✅ Published {len(all_tags)} tags → {output}")
    print(f"   version: {version}")
    print(f"   updated_at: {vocab['updated_at']}")
    print(f"   abbrevs: {len(abbrevs)} entries")


if __name__ == "__main__":
    main()
