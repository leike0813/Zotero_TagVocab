#!/usr/bin/env python3
"""
scripts/validate.py

Validates tags.yaml, aliases.yaml, and abbrev.yaml for format consistency.
Loads all rules (facet enum, tag pattern, abbreviation casing) from
protocol/ — see scripts/lib/protocol_loader.py.

Usage:
  python3 scripts/validate.py [--strict]
  python3 scripts/validate.py --per-facet [--strict]
"""

import sys
import re
import yaml
import argparse
from pathlib import Path

# Protocol-driven imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib.protocol_loader import get_facets, get_facet_set, get_tag_pattern, get_tags_dir

TAGS_FILE = Path("tags/tags.yaml")
ALIASES_FILE = Path("tags/aliases.yaml")
ABBREV_FILE = Path("tags/abbrev.yaml")


def load_yaml(path):
    if not path.exists():
        return None
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_abbrevs():
    data = load_yaml(ABBREV_FILE)
    if not isinstance(data, dict):
        return {}
    return {k: v for k, v in data.items() if isinstance(v, str)}


def validate_tags(tags, abbrevs):
    """Validate tag entries. Returns list of issue strings."""
    issues = []
    allowed_facets = get_facet_set()
    tag_pattern = get_tag_pattern()

    if not isinstance(tags, list):
        if tags is None:
            return []
        issues.append("root must be a list")
        return issues

    seen = set()
    seen_lower = {}

    for i, entry in enumerate(tags):
        loc = f"tags[{i}]"

        if not isinstance(entry, dict):
            issues.append(f"{loc}: entry is not a mapping")
            continue

        tag = entry.get("tag")
        if not tag:
            issues.append(f"{loc}: missing 'tag' field")
            continue

        # Duplicate check (exact)
        if tag in seen:
            issues.append(f"{loc}: duplicate tag '{tag}'")
        seen.add(tag)

        # Case-insensitive duplicate check
        tag_lower = tag.lower()
        if tag_lower in seen_lower and seen_lower[tag_lower] != tag:
            issues.append(
                f"{loc}: case-insensitive duplicate '{tag}' vs '{seen_lower[tag_lower]}'"
            )
        seen_lower[tag_lower] = tag

        # Format check (from protocol)
        if not tag_pattern.match(tag):
            issues.append(f"{loc}: tag '{tag}' does not match facet:value format")

        # Spaces check
        if " " in tag:
            issues.append(f"{loc}: tag '{tag}' contains spaces")

        # Facet check (from protocol)
        if ":" in tag:
            facet = tag.split(":")[0]
            entry_facet = entry.get("facet", "")
            if facet not in allowed_facets:
                issues.append(
                    f"{loc}: facet '{facet}' not in allowed set {sorted(allowed_facets)}"
                )
            if entry_facet and entry_facet != facet:
                issues.append(
                    f"{loc}: facet field '{entry_facet}' doesn't match tag prefix '{facet}'"
                )
        else:
            issues.append(f"{loc}: tag '{tag}' missing facet prefix (no ':')")

        # Abbreviation check
        if ":" in tag:
            value = tag.split(":", 1)[1]
            segments = re.split(r"[/-]", value)
            for seg in segments:
                seg_lower = seg.lower()
                if seg_lower in abbrevs:
                    expected = abbrevs[seg_lower]
                    if seg != expected:
                        issues.append(
                            f"{loc}: '{seg}' in tag '{tag}' should be '{expected}' per abbrev.yaml"
                        )

        # Deprecated field check
        dep = entry.get("deprecated")
        if dep is not None and not isinstance(dep, bool):
            issues.append(
                f"{loc}: 'deprecated' should be boolean, got {type(dep).__name__}"
            )

    return issues


def validate_aliases(aliases):
    """Validate aliases.yaml entries."""
    issues = []

    if aliases is None:
        return []

    if not isinstance(aliases, list):
        return []

    for i, entry in enumerate(aliases):
        loc = f"aliases[{i}]"
        if not isinstance(entry, dict):
            issues.append(f"{loc}: entry is not a mapping")
            continue
        if "alias" not in entry:
            issues.append(f"{loc}: missing 'alias' field")
        if "canonical" not in entry:
            issues.append(f"{loc}: missing 'canonical' field")

    return issues


def main():
    parser = argparse.ArgumentParser(
        description="Validate vocabulary files for format consistency."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit with error code on any issue",
    )
    parser.add_argument(
        "--per-facet",
        action="store_true",
        help="Validate per-facet files (tags/<facet>.yaml) instead of compiled tags.yaml",
    )
    args = parser.parse_args()

    all_issues = []
    abbrevs = load_abbrevs()
    allowed_facets = get_facet_set()
    facets = get_facets()

    if args.per_facet:
        # Per-facet validation mode
        tags_dir = get_tags_dir()
        all_tags_cross = set()
        all_tags_cross_lower = {}
        total_tags = 0
        facets_found = set()

        for facet in sorted(facets):
            facet_file = tags_dir / f"{facet}.yaml"
            if not facet_file.exists():
                all_issues.append(f"{facet}.yaml: file not found")
                continue

            data = load_yaml(facet_file)
            if not isinstance(data, list):
                if data is None:
                    continue
                all_issues.append(f"{facet}.yaml: root is not a list")
                continue

            count = len(data)
            total_tags += count
            facets_found.add(facet)

            tag_issues = validate_tags(data, abbrevs)
            for issue in tag_issues:
                all_issues.append(f"{facet}.yaml: {issue}")

            for entry in data:
                if not isinstance(entry, dict):
                    continue
                tag = entry.get("tag", "")
                entry_facet = entry.get("facet", "")

                # Facet-filename consistency
                if entry_facet and entry_facet != facet:
                    all_issues.append(
                        f"{facet}.yaml: entry '{tag}' has facet '{entry_facet}' but is in {facet}.yaml"
                    )

                # Cross-file duplicate check
                if tag in all_tags_cross:
                    all_issues.append(f"{facet}.yaml: cross-file duplicate '{tag}'")
                all_tags_cross.add(tag)

                tag_lower = tag.lower()
                if tag_lower in all_tags_cross_lower:
                    prev_tag, prev_file = all_tags_cross_lower[tag_lower]
                    if prev_tag != tag:
                        all_issues.append(
                            f"{facet}.yaml: cross-file case-insensitive duplicate '{tag}' vs '{prev_tag}' in {prev_file}.yaml"
                        )
                else:
                    all_tags_cross_lower[tag_lower] = (tag, facet)

        print(f"Tags: {total_tags} (per-facet mode)")
        print(f"Facets validated: {sorted(facets_found) if facets_found else 'none'}")

    else:
        # Standard compiled-file validation
        tags = load_yaml(TAGS_FILE)
        tag_issues = validate_tags(tags, abbrevs)
        all_issues.extend(tag_issues)

        aliases = load_yaml(ALIASES_FILE)
        alias_issues = validate_aliases(aliases)
        all_issues.extend(alias_issues)

        tag_count = len(tags) if isinstance(tags, list) else 0

        facets_in_use = set()
        if isinstance(tags, list):
            for t in tags:
                if isinstance(t, dict) and "facet" in t:
                    facets_in_use.add(t["facet"])

        print(f"Tags: {tag_count}")
        print(f"Facets in use: {sorted(facets_in_use) if facets_in_use else 'none'}")

    # Common reporting
    if all_issues:
        print(f"\n❌ {len(all_issues)} issue(s) found:")
        for issue in all_issues:
            print(f"  - {issue}")
        if args.strict:
            sys.exit(1)
    else:
        print("\n✅ All checks passed.")


if __name__ == "__main__":
    main()
