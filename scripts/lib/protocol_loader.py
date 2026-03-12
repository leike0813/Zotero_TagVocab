#!/usr/bin/env python3
"""
scripts/lib/protocol_loader.py

Loads and caches the vocabulary protocol from protocol/ directory.
All scripts import from this module instead of hardcoding rules.

This module is the ONLY place where protocol/ files are read.
"""

import re
import yaml
from pathlib import Path
from functools import lru_cache

# Resolve protocol directory relative to project root
_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_PROTOCOL_DIR = _PROJECT_ROOT / "protocol"


@lru_cache(maxsize=1)
def load_protocol():
    """Load the root protocol manifest."""
    path = _PROTOCOL_DIR / "protocol.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


@lru_cache(maxsize=1)
def get_facets():
    """Return the ordered list of allowed facet names."""
    return list(load_protocol()["facets"])


@lru_cache(maxsize=1)
def get_facet_set():
    """Return the set of allowed facet names (for fast membership checks)."""
    return set(get_facets())


@lru_cache(maxsize=1)
def get_tag_pattern():
    """Return the compiled tag format regex."""
    return re.compile(load_protocol()["tag_pattern"])


@lru_cache(maxsize=1)
def get_tag_pattern_string():
    """Return the raw tag pattern string."""
    return load_protocol()["tag_pattern"]


@lru_cache(maxsize=1)
def get_paths():
    """Return the file layout paths from the protocol."""
    return load_protocol()["paths"]


@lru_cache(maxsize=1)
def get_tags_dir():
    """Return the tags directory path."""
    return _PROJECT_ROOT / load_protocol()["paths"]["tags_dir"]


@lru_cache(maxsize=1)
def get_facet_definitions():
    """Load per-facet definitions from the facet schema."""
    path = _PROTOCOL_DIR / "schema" / "facet.schema.yaml"
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("definitions", [])


@lru_cache(maxsize=1)
def load_operation(name):
    """Load a specific operation contract."""
    path = _PROTOCOL_DIR / "operations" / f"{name}.yaml"
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def get_json_source_path():
    """Return the path to the JSON source of truth (tags/tags.json)."""
    return _PROJECT_ROOT / load_protocol()["paths"]["json_source"]


def load_vocab_json():
    """Load the JSON source of truth. Returns the full vocab dict."""
    import json
    path = get_json_source_path()
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_vocab_json(vocab):
    """Write updated vocab dict back to the JSON source of truth."""
    import json
    from datetime import datetime, timezone
    path = get_json_source_path()
    vocab["updated_at"] = datetime.now(timezone.utc).isoformat()
    vocab["tag_count"] = len(vocab.get("tags", []))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(vocab, f, ensure_ascii=False, indent=2)
        f.write("\n")
