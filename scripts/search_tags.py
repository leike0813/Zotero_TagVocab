#!/usr/bin/env python3
"""
scripts/search_tags.py

Search for tags using case-insensitive substring matching.
Reads from tags/tags.json (the single source of truth).

Usage: python3 scripts/search_tags.py <query> [--facet FACET]
"""

import sys
import argparse
from pathlib import Path

# Protocol-driven imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib.protocol_loader import get_facets, load_vocab_json


def main():
    facets = get_facets()

    parser = argparse.ArgumentParser(description="Search tags by substring.")
    parser.add_argument("query", help="Search term (case-insensitive substring)")
    parser.add_argument("--facet", choices=facets, help="Restrict search to one facet")
    args = parser.parse_args()

    vocab = load_vocab_json()
    query = args.query.lower()

    results = []
    for entry in vocab.get("tags", []):
        tag = entry.get("tag", "")
        facet = entry.get("facet", "")
        note = entry.get("note", "")

        if args.facet and facet != args.facet:
            continue

        if query in tag.lower() or query in note.lower():
            results.append((tag, facet, note))

    if not results:
        print("No matching tags found.")
        return

    print(f"Found {len(results)} match(es) for '{args.query}':\n")

    max_tag = max(len(r[0]) for r in results)
    max_facet = max(len(r[1]) for r in results)

    header = f"  {'TAG':<{max_tag}}  {'FACET':<{max_facet}}  NOTE"
    print(header)
    print("  " + "─" * (max_tag + max_facet + 20))

    for tag, facet, note in sorted(results):
        print(f"  {tag:<{max_tag}}  {facet:<{max_facet}}  {note}")


if __name__ == "__main__":
    main()
