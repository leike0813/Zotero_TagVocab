#!/usr/bin/env python3
"""
scripts/export_tags.py

Export tag strings (no metadata) in multiple formats.
Loads facet list from protocol/.

Usage:
  python3 scripts/export_tags.py --format yaml
  python3 scripts/export_tags.py --format json --facet topic
  python3 scripts/export_tags.py --format md -o tags_list.md
  python3 scripts/export_tags.py --format txt
"""

import sys
import json
import yaml
import argparse
from pathlib import Path

# Protocol-driven imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib.protocol_loader import get_facets, get_tags_dir


def load_yaml_file(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def collect_tags(facet_filter=None):
    """Collect tag strings from per-facet files."""
    facets = get_facets()
    tags_dir = get_tags_dir()
    tags = []
    facets_to_load = [facet_filter] if facet_filter else facets
    for facet in facets_to_load:
        path = tags_dir / f"{facet}.yaml"
        data = load_yaml_file(path)
        if isinstance(data, list):
            for entry in data:
                if isinstance(entry, dict) and "tag" in entry:
                    tags.append(entry["tag"])
    return sorted(tags)


def format_yaml(tags):
    return yaml.dump(tags, default_flow_style=False, allow_unicode=True)


def format_json(tags):
    return json.dumps(tags, indent=2, ensure_ascii=False)


def format_markdown(tags):
    lines = ["# Tag List", ""]
    by_facet = {}
    for tag in tags:
        facet = tag.split(":")[0] if ":" in tag else "other"
        by_facet.setdefault(facet, []).append(tag)

    for facet in sorted(by_facet.keys()):
        lines.append(f"## {facet}")
        lines.append("")
        for tag in by_facet[facet]:
            lines.append(f"- `{tag}`")
        lines.append("")

    return "\n".join(lines)


def format_text(tags):
    return "\n".join(tags) + "\n"


FORMATTERS = {
    "yaml": format_yaml,
    "json": format_json,
    "md": format_markdown,
    "txt": format_text,
}


def main():
    facets = get_facets()

    parser = argparse.ArgumentParser(description="Export tag list in various formats.")
    parser.add_argument("--format", "-f", required=True, choices=FORMATTERS.keys(),
                        help="Output format: yaml, json, md, txt")
    parser.add_argument("--facet", choices=facets,
                        help="Export only tags from this facet")
    parser.add_argument("-o", "--output", type=str, metavar="FILE",
                        help="Write to file instead of stdout")
    args = parser.parse_args()

    tags = collect_tags(args.facet)

    if not tags:
        print("No tags found.", file=sys.stderr)
        sys.exit(1)

    output = FORMATTERS[args.format](tags)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ Exported {len(tags)} tags to {args.output}")
    else:
        print(output, end="")


if __name__ == "__main__":
    main()
