#!/usr/bin/env python3
"""
scripts/stats.py

Display vocabulary statistics: tag counts per facet, total, and recent additions.
Loads facet list from protocol/.

Usage: python3 scripts/stats.py [--recent N]
"""

import sys
import yaml
import argparse
from pathlib import Path

# Protocol-driven imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib.protocol_loader import get_facets, get_tags_dir


def load_yaml(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def main():
    facets = get_facets()
    tags_dir = get_tags_dir()

    parser = argparse.ArgumentParser(description="Show vocabulary statistics.")
    parser.add_argument("--recent", type=int, metavar="N", default=0,
                        help="Show the N most recently added tags (last entries in each file)")
    args = parser.parse_args()

    total = 0
    facet_counts = {}
    all_entries = []

    for facet in facets:
        path = tags_dir / f"{facet}.yaml"
        data = load_yaml(path)
        count = len(data) if isinstance(data, list) else 0
        facet_counts[facet] = count
        total += count
        if isinstance(data, list):
            all_entries.extend(data)

    # Header
    print("=" * 40)
    print("  Vocabulary Statistics")
    print("=" * 40)
    print()

    # Per-facet counts
    max_name = max(len(f) for f in facets)
    for facet in facets:
        count = facet_counts[facet]
        bar = "█" * (count // 3)
        print(f"  {facet:<{max_name}}  {count:>4}  {bar}")

    print(f"\n  {'TOTAL':<{max_name}}  {total:>4}")
    print()

    # Recent additions
    if args.recent > 0:
        recent = all_entries[-args.recent:] if len(all_entries) >= args.recent else all_entries
        print(f"  Last {len(recent)} additions:")
        print("  " + "─" * 50)
        for entry in reversed(recent):
            tag = entry.get("tag", "?")
            note = entry.get("note", "")
            print(f"    {tag}  ({note})" if note else f"    {tag}")
        print()


if __name__ == "__main__":
    main()
