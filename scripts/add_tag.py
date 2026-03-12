#!/usr/bin/env python3
"""
scripts/add_tag.py

Interactively add a new tag to the vocabulary.
Reads from and writes to tags/tags.json (the single source of truth).

Usage: python3 scripts/add_tag.py
"""

import re
import sys
import subprocess
from pathlib import Path

# Protocol-driven imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from scripts.lib.protocol_loader import (
    get_facets, get_tag_pattern, get_tags_dir,
    load_vocab_json, save_vocab_json,
)

ABBREV_FILE = Path("tags/abbrev.yaml")


def load_abbrevs_from_json(vocab):
    """Load abbreviations from the JSON vocab."""
    return vocab.get("abbrevs", {})


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
    vocab = load_vocab_json()
    abbrevs = load_abbrevs_from_json(vocab)
    existing_tags = {entry["tag"] for entry in vocab.get("tags", []) if "tag" in entry}

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

    # Step 5: Write to JSON source of truth
    vocab["tags"].append({
        "tag": full_tag,
        "facet": facet,
        "source": "manual",
        "note": note,
        "deprecated": False,
    })

    # Re-sort deterministically
    vocab["tags"].sort(key=lambda x: (x.get("facet", ""), x.get("tag", "")))

    save_vocab_json(vocab)
    print(f"\n✅ Added '{full_tag}' to tags/tags.json")

    # Step 6: Derive YAML views
    print("Deriving facet files + compiling...")
    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "derive_facets.py")],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        print(result.stdout.strip())

    result = subprocess.run(
        [sys.executable, str(Path(__file__).parent / "compile_vocab.py")],
        capture_output=True, text=True
    )
    if result.stdout.strip():
        print(result.stdout.strip())


if __name__ == "__main__":
    main()
