#!/usr/bin/env python3
"""
scripts/split_tags.py

One-time migration: splits tags/tags.yaml into per-facet YAML files.
Creates tags/<facet>.yaml for each facet found in the data.

Usage: python3 scripts/split_tags.py [--dry-run]
"""

import sys
import yaml
import argparse
from pathlib import Path

TAGS_DIR = Path("tags")
TAGS_FILE = TAGS_DIR / "tags.yaml"

ALLOWED_FACETS = {"field", "topic", "method", "model", "ai_task", "data", "tool", "status"}


def main():
    parser = argparse.ArgumentParser(description="Split tags.yaml into per-facet files.")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created without writing")
    args = parser.parse_args()

    if not TAGS_FILE.exists():
        print(f"❌ {TAGS_FILE} not found.")
        sys.exit(1)

    with open(TAGS_FILE, "r", encoding="utf-8") as f:
        tags = yaml.safe_load(f)

    if not isinstance(tags, list):
        print("❌ tags.yaml root is not a list.")
        sys.exit(1)

    # Group by facet
    by_facet = {}
    for entry in tags:
        facet = entry.get("facet", "unknown")
        by_facet.setdefault(facet, []).append(entry)

    # Report
    print(f"Total tags: {len(tags)}")
    print(f"Facets found: {sorted(by_facet.keys())}")
    print()

    for facet in sorted(by_facet.keys()):
        entries = by_facet[facet]
        outpath = TAGS_DIR / f"{facet}.yaml"

        if facet not in ALLOWED_FACETS:
            print(f"  ⚠️  Skipping unknown facet '{facet}' ({len(entries)} tags)")
            continue

        print(f"  {facet}: {len(entries)} tags → {outpath}")

        if not args.dry_run:
            with open(outpath, "w", encoding="utf-8") as f:
                f.write(f"# {facet} tags — auto-split from tags.yaml\n")
                yaml.dump(entries, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

    if args.dry_run:
        print("\n(dry run — no files written)")
    else:
        total_written = sum(len(v) for k, v in by_facet.items() if k in ALLOWED_FACETS)
        print(f"\n✅ Split {total_written} tags into {len([k for k in by_facet if k in ALLOWED_FACETS])} facet files.")


if __name__ == "__main__":
    main()
