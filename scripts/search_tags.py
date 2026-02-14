#!/usr/bin/env python3
"""
scripts/search_tags.py

Search for tags across all per-facet files using case-insensitive substring matching.
Loads facet list from protocol/.

Usage: python3 scripts/search_tags.py <query> [--facet FACET]
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

    parser = argparse.ArgumentParser(description="Search tags by substring.")
    parser.add_argument("query", help="Search term (case-insensitive substring)")
    parser.add_argument("--facet", choices=facets, help="Restrict search to one facet")
    args = parser.parse_args()

    query = args.query.lower()
    facets_to_search = [args.facet] if args.facet else facets
    tags_dir = get_tags_dir()

    results = []
    for facet in facets_to_search:
        path = tags_dir / f"{facet}.yaml"
        data = load_yaml(path)
        if not isinstance(data, list):
            continue
        for entry in data:
            tag = entry.get("tag", "")
            note = entry.get("note", "")
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
