#!/usr/bin/env python3
"""
scripts/add_tag.py

Interactively add a new tag to the vocabulary.
Loads facet list, tag pattern, and abbreviation rules from protocol/.

Usage: python3 scripts/add_tag.py
"""

import re
import sys
import yaml
import subprocess
from pathlib import Path

# Protocol-driven imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib.protocol_loader import get_facets, get_tag_pattern, get_tags_dir

ABBREV_FILE = Path("tags/abbrev.yaml")


def load_yaml(path):
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or []


def load_abbrevs():
    data = load_yaml(ABBREV_FILE)
    if not isinstance(data, dict):
        return {}
    return {k: v for k, v in data.items() if isinstance(v, str)}


def load_all_tags():
    """Load all existing tags from per-facet files."""
    all_tags = set()
    tags_dir = get_tags_dir()
    for facet in get_facets():
        path = tags_dir / f"{facet}.yaml"
        data = load_yaml(path)
        if isinstance(data, list):
            for entry in data:
                if isinstance(entry, dict) and "tag" in entry:
                    all_tags.add(entry["tag"])
    return all_tags


def validate_value(value, facet, abbrevs):
    """Validate the tag value format and abbreviation casing."""
    tag_pattern = get_tag_pattern()
    full_tag = f"{facet}:{value}"
    if not tag_pattern.match(full_tag):
        return "Value contains invalid characters. Use only a-z, A-Z, 0-9, /, _, ., -"
    if " " in value:
        return "Value must not contain spaces."

    segments = re.split(r"[/-]", value)
    for seg in segments:
        seg_lower = seg.lower()
        if seg_lower in abbrevs:
            expected = abbrevs[seg_lower]
            if seg != expected:
                return f"Segment '{seg}' should be '{expected}' per abbrev.yaml"

    return None


def main():
    facets = get_facets()
    abbrevs = load_abbrevs()
    existing_tags = load_all_tags()

    print("=" * 50)
    print("  Add Tag — Interactive")
    print("=" * 50)
    print()

    # Step 1: Select facet (from protocol)
    print("Select facet:")
    for i, facet in enumerate(facets, 1):
        print(f"  {i}. {facet}")
    print()

    while True:
        choice = input(f"Facet number (1-{len(facets)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(facets):
            facet = facets[int(choice) - 1]
            break
        print(f"Invalid choice. Enter 1-{len(facets)}.")

    print(f"\n→ Facet: {facet}")

    # Step 2: Enter value
    while True:
        value = input(f"\nTag value (without '{facet}:' prefix): ").strip()
        if not value:
            print("Value cannot be empty.")
            continue

        error = validate_value(value, facet, abbrevs)
        if error:
            print(f"❌ {error}")
            continue

        full_tag = f"{facet}:{value}"

        if full_tag in existing_tags:
            print(f"❌ Tag '{full_tag}' already exists.")
            continue

        for t in existing_tags:
            if t.lower() == full_tag.lower():
                print(f"❌ Case-insensitive duplicate: '{full_tag}' vs existing '{t}'")
                break
        else:
            break

    print(f"→ Tag: {full_tag}")

    # Step 3: Enter note
    note = input("\nNote (description, 可为中文): ").strip()
    if not note:
        note = ""

    # Step 4: Confirm
    print()
    print("─" * 40)
    print(f"  tag:    {full_tag}")
    print(f"  facet:  {facet}")
    print(f"  note:   {note}")
    print("─" * 40)

    confirm = input("\nConfirm? (y/n): ").strip().lower()
    if confirm != "y":
        print("Cancelled.")
        return

    # Step 5: Append to facet file
    tags_dir = get_tags_dir()
    facet_file = tags_dir / f"{facet}.yaml"
    entries = load_yaml(facet_file)
    if not isinstance(entries, list):
        entries = []

    entries.append({
        "tag": full_tag,
        "facet": facet,
        "source": "manual",
        "note": note,
        "deprecated": False,
    })

    with open(facet_file, "w", encoding="utf-8") as f:
        f.write(f"# {facet} tags\n")
        yaml.dump(entries, f, sort_keys=False, allow_unicode=True, default_flow_style=False)

    print(f"\n✅ Added '{full_tag}' to {facet_file}")

    # Step 6: Auto-compile
    print("Compiling vocabulary...")
    result = subprocess.run(
        [sys.executable, "scripts/compile_vocab.py"],
        capture_output=True, text=True
    )
    print(result.stdout.strip())
    if result.returncode != 0:
        print(f"⚠️  Compile warning: {result.stderr.strip()}")


if __name__ == "__main__":
    main()
