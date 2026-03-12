#!/usr/bin/env python3
"""
scripts/stats.py

Display vocabulary statistics: tag counts per facet, total, and recent additions.
Reads from tags/tags.json (the single source of truth).

Usage: python3 scripts/stats.py [--recent N]
"""

import sys
import argparse
from pathlib import Path

# Protocol-driven imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib.protocol_loader import get_facets, load_vocab_json


def main():
    facets = get_facets()

    parser = argparse.ArgumentParser(description="Show vocabulary statistics.")
    parser.add_argument("--recent", type=int, metavar="N", default=0,
                        help="Show the N most recently added tags (last entries)")
    args = parser.parse_args()

    vocab = load_vocab_json()
    all_tags = vocab.get("tags", [])

    # Count per facet
    facet_counts = {f: 0 for f in facets}
    for entry in all_tags:
        f = entry.get("facet", "")
        if f in facet_counts:
            facet_counts[f] += 1

    total = len(all_tags)

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
        recent = all_tags[-args.recent:] if len(all_tags) >= args.recent else all_tags
        print(f"  Last {len(recent)} additions:")
        print("  " + "─" * 50)
        for entry in reversed(recent):
            tag = entry.get("tag", "?")
            note = entry.get("note", "")
            print(f"    {tag}  ({note})" if note else f"    {tag}")
        print()


if __name__ == "__main__":
    main()
